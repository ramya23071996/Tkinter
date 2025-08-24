import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import sqlite3, threading, json, os

DB_NAME = 'tasks.db'

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    status TEXT NOT NULL)''')
    conn.commit()
    conn.close()

class TaskManager(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Personal Task Manager")
        self.geometry("500x400")
        self.resizable(False, False)

        self.status_var = tk.StringVar(value="Ready")
        self.tasks = []

        self.build_ui()
        self.load_tasks_threaded()

    def build_ui(self):
        self.tree = ttk.Treeview(self, columns=('Title', 'Status'), show='headings')
        self.tree.heading('Title', text='Task')
        self.tree.heading('Status', text='Status')
        self.tree.pack(fill='both', expand=True, padx=10, pady=10)

        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=5)

        ttk.Button(btn_frame, text="Add Task", command=self.add_task).grid(row=0, column=0, padx=5)
        ttk.Button(btn_frame, text="Edit Task", command=self.edit_task).grid(row=0, column=1, padx=5)
        ttk.Button(btn_frame, text="Delete Task", command=self.delete_task).grid(row=0, column=2, padx=5)
        ttk.Button(btn_frame, text="Import", command=self.import_tasks).grid(row=0, column=3, padx=5)
        ttk.Button(btn_frame, text="Export", command=self.export_tasks).grid(row=0, column=4, padx=5)

        self.status_label = ttk.Label(self, textvariable=self.status_var, anchor='w')
        self.status_label.pack(fill='x', padx=10)

    def update_status(self, msg):
        self.status_var.set(msg)

    def load_tasks_threaded(self):
        threading.Thread(target=self.load_tasks, daemon=True).start()

    def load_tasks(self):
        self.update_status("Loading tasks...")
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("SELECT id, title, status FROM tasks")
        rows = c.fetchall()
        conn.close()
        self.tasks = rows
        self.after(100, self.populate_tree)

    def populate_tree(self):
        self.tree.delete(*self.tree.get_children())
        for task in self.tasks:
            self.tree.insert('', 'end', iid=task[0], values=(task[1], task[2]))
        self.update_status("Tasks loaded.")

    def add_task(self):
        self.task_dialog("Add Task")

    def edit_task(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Select", "Select a task to edit.")
            return
        task_id = selected[0]
        title, status = self.tree.item(task_id)['values']
        self.task_dialog("Edit Task", task_id, title, status)

    def delete_task(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Select", "Select a task to delete.")
            return
        task_id = selected[0]
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("DELETE FROM tasks WHERE id=?", (task_id,))
        conn.commit()
        conn.close()
        self.load_tasks_threaded()

    def task_dialog(self, title, task_id=None, init_title="", init_status="Pending"):
        dialog = tk.Toplevel(self)
        dialog.title(title)
        dialog.geometry("300x150")
        dialog.transient(self)

        title_var = tk.StringVar(value=init_title)
        status_var = tk.StringVar(value=init_status)

        ttk.Label(dialog, text="Task Title:").pack(pady=5)
        title_entry = ttk.Entry(dialog, textvariable=title_var)
        title_entry.pack(fill='x', padx=10)

        ttk.Label(dialog, text="Status:").pack(pady=5)
        status_combo = ttk.Combobox(dialog, textvariable=status_var, values=["Pending", "Done"])
        status_combo.pack(fill='x', padx=10)

        def save():
            title = title_var.get().strip()
            status = status_var.get().strip()
            if not title or not status:
                messagebox.showerror("Invalid", "All fields required.")
                return
            conn = sqlite3.connect(DB_NAME)
            c = conn.cursor()
            if task_id:
                c.execute("UPDATE tasks SET title=?, status=? WHERE id=?", (title, status, task_id))
            else:
                c.execute("INSERT INTO tasks (title, status) VALUES (?, ?)", (title, status))
            conn.commit()
            conn.close()
            dialog.destroy()
            self.load_tasks_threaded()

        ttk.Button(dialog, text="Save", command=save).pack(pady=10)

    def import_tasks(self):
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json"), ("Text files", "*.txt")])
        if not file_path:
            return
        try:
            with open(file_path, 'r') as f:
                data = json.load(f) if file_path.endswith('.json') else [line.strip().split('|') for line in f]
            conn = sqlite3.connect(DB_NAME)
            c = conn.cursor()
            c.execute("DELETE FROM tasks")  # Clear existing
            for item in data:
                title, status = item if isinstance(item, list) else (item['title'], item['status'])
                c.execute("INSERT INTO tasks (title, status) VALUES (?, ?)", (title, status))
            conn.commit()
            conn.close()
            self.load_tasks_threaded()
        except Exception as e:
            messagebox.showerror("Import Error", str(e))

    def export_tasks(self):
        dir_path = filedialog.askdirectory()
        if not dir_path:
            return
        file_path = filedialog.asksaveasfilename(initialdir=dir_path,
                                                 defaultextension=".json",
                                                 filetypes=[("JSON files", "*.json"), ("Text files", "*.txt")])
        if not file_path:
            return
        try:
            conn = sqlite3.connect(DB_NAME)
            c = conn.cursor()
            c.execute("SELECT title, status FROM tasks")
            rows = c.fetchall()
            conn.close()
            if file_path.endswith('.json'):
                with open(file_path, 'w') as f:
                    json.dump([{'title': r[0], 'status': r[1]} for r in rows], f, indent=2)
            else:
                with open(file_path, 'w') as f:
                    for r in rows:
                        f.write(f"{r[0]}|{r[1]}\n")
            messagebox.showinfo("Exported", f"Tasks saved to {file_path}")
        except Exception as e:
            messagebox.showerror("Export Error", str(e))

if __name__ == "__main__":
    init_db()
    app = TaskManager()
    app.mainloop()