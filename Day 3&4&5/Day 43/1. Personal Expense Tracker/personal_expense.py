import tkinter as tk
from tkinter import ttk, messagebox, filedialog

# Sample data
categories = ["Food", "Transport", "Utilities"]
transactions = []

def add_transaction():
    category = category_var.get()
    amount = amount_entry.get()
    desc = desc_entry.get()

    if not category or not amount or not desc:
        messagebox.showwarning("Missing Info", "Please fill all fields.")
        return

    try:
        amount = float(amount)
    except ValueError:
        messagebox.showerror("Invalid Amount", "Amount must be a number.")
        return

    transactions.append((category, amount, desc))
    update_transaction_list()
    update_summary()

def delete_transaction():
    selected = transaction_listbox.curselection()
    if not selected:
        return
    confirm = messagebox.askyesno("Confirm Delete", "Delete selected transaction?")
    if confirm:
        transactions.pop(selected[0])
        update_transaction_list()
        update_summary()

def update_transaction_list():
    transaction_listbox.delete(0, tk.END)
    for cat, amt, desc in transactions:
        transaction_listbox.insert(tk.END, f"{cat}: ₹{amt:.2f} - {desc}")

def update_summary():
    total = sum(amt for _, amt, _ in transactions)
    summary_label.config(text=f"Total Expenses: ₹{total:.2f}")

def clear_all():
    if messagebox.askyesno("Clear All", "Clear all transactions?"):
        transactions.clear()
        update_transaction_list()
        update_summary()

def export_data():
    file_path = filedialog.asksaveasfilename(defaultextension=".csv",
        filetypes=[("CSV files", "*.csv"), ("Text files", "*.txt")])
    if file_path:
        with open(file_path, "w") as f:
            for cat, amt, desc in transactions:
                f.write(f"{cat},{amt},{desc}\n")
        messagebox.showinfo("Exported", f"Data saved to {file_path}")

def show_about():
    messagebox.showinfo("About", "Personal Expense Tracker\nBuilt with Tkinter")

def add_category_popup():
    def save_category():
        new_cat = new_cat_entry.get().strip()
        if new_cat:
            categories.append(new_cat)
            category_listbox.insert(tk.END, new_cat)
            category_var.set(new_cat)
            popup.destroy()

    popup = tk.Toplevel(root)
    popup.title("Add Category")
    tk.Label(popup, text="New Category:").pack(pady=5)
    new_cat_entry = tk.Entry(popup)
    new_cat_entry.pack(pady=5)
    tk.Button(popup, text="Add", command=save_category).pack(pady=5)

# Main window
root = tk.Tk()
root.title("Personal Expense Tracker")
root.geometry("700x500")

# Menu
menu = tk.Menu(root)
root.config(menu=menu)

file_menu = tk.Menu(menu, tearoff=0)
file_menu.add_command(label="Export", command=export_data)
menu.add_cascade(label="File", menu=file_menu)

edit_menu = tk.Menu(menu, tearoff=0)
edit_menu.add_command(label="Clear", command=clear_all)
menu.add_cascade(label="Edit", menu=edit_menu)

help_menu = tk.Menu(menu, tearoff=0)
help_menu.add_command(label="About", command=show_about)
menu.add_cascade(label="Help", menu=help_menu)

# Toolbar
toolbar = tk.Frame(root, bd=1, relief=tk.RAISED)
tk.Button(toolbar, text="Add", command=add_transaction).pack(side=tk.LEFT, padx=2, pady=2)
tk.Button(toolbar, text="Delete", command=delete_transaction).pack(side=tk.LEFT, padx=2, pady=2)
tk.Button(toolbar, text="New Category", command=add_category_popup).pack(side=tk.LEFT, padx=2, pady=2)
toolbar.pack(side=tk.TOP, fill=tk.X)

# Entry Form (Top Frame)
entry_frame = tk.Frame(root)
entry_frame.pack(fill=tk.X, padx=10, pady=5)

category_var = tk.StringVar()
tk.Label(entry_frame, text="Category:").grid(row=0, column=0)
category_dropdown = ttk.Combobox(entry_frame, textvariable=category_var, values=categories, state="readonly")
category_dropdown.grid(row=0, column=1)
category_dropdown.set(categories[0])

tk.Label(entry_frame, text="Amount:").grid(row=0, column=2)
amount_entry = tk.Entry(entry_frame)
amount_entry.grid(row=0, column=3)

tk.Label(entry_frame, text="Description:").grid(row=0, column=4)
desc_entry = tk.Entry(entry_frame, width=30)
desc_entry.grid(row=0, column=5)

# PanedWindow for Categories and Transactions
paned = tk.PanedWindow(root, sashrelief=tk.RAISED)
paned.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

# Left: Category List
left_frame = tk.Frame(paned)
tk.Label(left_frame, text="Categories").pack()
category_listbox = tk.Listbox(left_frame)
for cat in categories:
    category_listbox.insert(tk.END, cat)
category_listbox.pack(fill=tk.BOTH, expand=True)
paned.add(left_frame)

# Right: Transaction List with Scrollbar
right_frame = tk.Frame(paned)
tk.Label(right_frame, text="Transactions").pack()
scrollbar = tk.Scrollbar(right_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

transaction_listbox = tk.Listbox(right_frame, yscrollcommand=scrollbar.set)
transaction_listbox.pack(fill=tk.BOTH, expand=True)
scrollbar.config(command=transaction_listbox.yview)
paned.add(right_frame)

# Summary (Bottom Frame)
summary_frame = tk.Frame(root)
summary_frame.pack(fill=tk.X, padx=10, pady=5)
summary_label = tk.Label(summary_frame, text="Total Expenses: ₹0.00", font=("Arial", 12))
summary_label.pack()

root.mainloop()