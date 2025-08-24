import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sqlite3, threading, csv

DB_NAME = 'support_tickets.db'

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS tickets (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    issue TEXT NOT NULL,
                    priority TEXT NOT NULL)''')
    conn.commit()
    conn.close()

class TicketSystem(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Customer Support Ticket System")
        self.geometry("600x400")
        self.resizable(False, False)

        self.tickets = []
        self.build_ui()
        self.load_tickets_threaded()

    def build_ui(self):
        form_frame = ttk.LabelFrame(self, text="Submit New Ticket")
        form_frame.pack(fill='x', padx=10, pady=10)

        self.name_var = tk.StringVar()
        self.issue_var = tk.StringVar()
        self.priority_var = tk.StringVar()

        ttk.Label(form_frame, text="Name:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
        ttk.Entry(form_frame, textvariable=self.name_var).grid(row=0, column=1, padx=5, pady=5, sticky='ew')

        ttk.Label(form_frame, text="Issue:").grid(row=1, column=0, padx=5, pady=5, sticky='e')
        ttk.Entry(form_frame, textvariable=self.issue_var).grid(row=1, column=1, padx=5, pady=5, sticky='ew')

        ttk.Label(form_frame, text="Priority:").grid(row=2, column=0, padx=5, pady=5, sticky='e')
        ttk.Combobox(form_frame, textvariable=self.priority_var, values=["Low", "Medium", "High"]).grid(row=2, column=1, padx=5, pady=5, sticky='ew')

        form_frame.columnconfigure(1, weight=1)
        ttk.Button(form_frame, text="Submit Ticket", command=self.submit_ticket).grid(row=3, column=0, columnspan=2, pady=10)

        self.tree = ttk.Treeview(self, columns=('Name', 'Issue', 'Priority'), show='headings')
        self.tree.heading('Name', text='Name')
        self.tree.heading('Issue', text='Issue')
        self.tree.heading('Priority', text='Priority')
        self.tree.pack(fill='both', expand=True, padx=10, pady=10)

        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=5)
        ttk.Button(btn_frame, text="Export CSV", command=self.export_csv).grid(row=0, column=0, padx=5)
        ttk.Button(btn_frame, text="Import CSV", command=self.import_csv).grid(row=0, column=1, padx=5)

    def submit_ticket(self):
        name = self.name_var.get().strip()
        issue = self.issue_var.get().strip()
        priority = self.priority_var.get().strip()

        if not name or not issue or not priority:
            messagebox.showerror("Validation Error", "All fields are required.")
            return

        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("INSERT INTO tickets (name, issue, priority) VALUES (?, ?, ?)", (name, issue, priority))
        conn.commit()
        conn.close()

        self.name_var.set('')
        self.issue_var.set('')
        self.priority_var.set('')
        messagebox.showinfo("Success", "Ticket submitted successfully.")
        self.load_tickets_threaded()

    def load_tickets_threaded(self):
        threading.Thread(target=self.load_tickets, daemon=True).start()

    def load_tickets(self):
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("SELECT name, issue, priority FROM tickets")
        rows = c.fetchall()
        conn.close()
        self.tickets = rows
        self.after(100, self.populate_tree)

    def populate_tree(self):
        self.tree.delete(*self.tree.get_children())
        for row in self.tickets:
            self.tree.insert('', 'end', values=row)

    def export_csv(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".csv",
                                                 filetypes=[("CSV files", "*.csv")])
        if not file_path:
            return
        try:
            conn = sqlite3.connect(DB_NAME)
            c = conn.cursor()
            c.execute("SELECT name, issue, priority FROM tickets")
            rows = c.fetchall()
            conn.close()
            with open(file_path, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['Name', 'Issue', 'Priority'])
                writer.writerows(rows)
            messagebox.showinfo("Exported", f"Tickets saved to {file_path}")
        except Exception as e:
            messagebox.showerror("Export Error", str(e))

    def import_csv(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if not file_path:
            return
        try:
            with open(file_path, 'r') as f:
                reader = csv.DictReader(f)
                rows = [(r['Name'], r['Issue'], r['Priority']) for r in reader]
            conn = sqlite3.connect(DB_NAME)
            c = conn.cursor()
            c.execute("DELETE FROM tickets")  # Clear existing
            c.executemany("INSERT INTO tickets (name, issue, priority) VALUES (?, ?, ?)", rows)
            conn.commit()
            conn.close()
            messagebox.showinfo("Imported", f"Tickets loaded from {file_path}")
            self.load_tickets_threaded()
        except Exception as e:
            messagebox.showerror("Import Error", str(e))

if __name__ == "__main__":
    init_db()
    app = TicketSystem()
    app.mainloop()