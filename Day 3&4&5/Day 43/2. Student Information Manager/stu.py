import tkinter as tk
from tkinter import ttk, messagebox, filedialog

students = []

def add_student():
    name = name_entry.get().strip()
    age = age_entry.get().strip()
    grade = grade_entry.get().strip()

    if not name or not age or not grade:
        messagebox.showwarning("Missing Info", "Please fill all fields.")
        return

    students.append({"name": name, "age": age, "grade": grade})
    update_student_list()

def remove_student():
    selected = student_listbox.curselection()
    if not selected:
        return
    confirm = messagebox.askyesno("Confirm Delete", "Remove selected student?")
    if confirm:
        students.pop(selected[0])
        update_student_list()
        clear_details()

def update_student_list():
    student_listbox.delete(0, tk.END)
    for student in students:
        student_listbox.insert(tk.END, student["name"])

def show_details(event):
    selected = student_listbox.curselection()
    if not selected:
        return
    student = students[selected[0]]
    details_text.set(f"Name: {student['name']}\nAge: {student['age']}\nGrade: {student['grade']}")

def clear_details():
    details_text.set("")

def open_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if file_path:
        with open(file_path, "r") as f:
            students.clear()
            for line in f:
                name, age, grade = line.strip().split(",")
                students.append({"name": name, "age": age, "grade": grade})
        update_student_list()
        clear_details()

def save_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt",
        filetypes=[("Text Files", "*.txt")])
    if file_path:
        with open(file_path, "w") as f:
            for student in students:
                f.write(f"{student['name']},{student['age']},{student['grade']}\n")
        messagebox.showinfo("Saved", f"Data saved to {file_path}")

def show_about():
    messagebox.showinfo("About", "Student Information Manager\nBuilt with Tkinter")

def edit_student_popup():
    selected = student_listbox.curselection()
    if not selected:
        return
    student = students[selected[0]]

    def save_changes():
        student["name"] = name_var.get()
        student["age"] = age_var.get()
        student["grade"] = grade_var.get()
        update_student_list()
        popup.destroy()

    popup = tk.Toplevel(root)
    popup.title("Edit Student")

    name_var = tk.StringVar(value=student["name"])
    age_var = tk.StringVar(value=student["age"])
    grade_var = tk.StringVar(value=student["grade"])

    tk.Label(popup, text="Name:").pack()
    tk.Entry(popup, textvariable=name_var).pack()
    tk.Label(popup, text="Age:").pack()
    tk.Entry(popup, textvariable=age_var).pack()
    tk.Label(popup, text="Grade:").pack()
    tk.Entry(popup, textvariable=grade_var).pack()
    tk.Button(popup, text="Save", command=save_changes).pack(pady=5)

# Main window
root = tk.Tk()
root.title("Student Information Manager")
root.geometry("700x500")

# Menu
menu = tk.Menu(root)
root.config(menu=menu)

file_menu = tk.Menu(menu, tearoff=0)
file_menu.add_command(label="Open", command=open_file)
file_menu.add_command(label="Save", command=save_file)
menu.add_cascade(label="File", menu=file_menu)

edit_menu = tk.Menu(menu, tearoff=0)
edit_menu.add_command(label="Add", command=add_student)
edit_menu.add_command(label="Delete", command=remove_student)
edit_menu.add_command(label="Edit", command=edit_student_popup)
menu.add_cascade(label="Edit", menu=edit_menu)

help_menu = tk.Menu(menu, tearoff=0)
help_menu.add_command(label="About", command=show_about)
menu.add_cascade(label="Help", menu=help_menu)

# Toolbar
toolbar = tk.Frame(root, bd=1, relief=tk.RAISED)
tk.Button(toolbar, text="Add Student", command=add_student).pack(side=tk.LEFT, padx=2, pady=2)
tk.Button(toolbar, text="Remove Student", command=remove_student).pack(side=tk.LEFT, padx=2, pady=2)
tk.Button(toolbar, text="Edit Info", command=edit_student_popup).pack(side=tk.LEFT, padx=2, pady=2)
toolbar.pack(side=tk.TOP, fill=tk.X)

# Entry Form
form_frame = tk.Frame(root)
form_frame.pack(fill=tk.X, padx=10, pady=5)

tk.Label(form_frame, text="Name:").grid(row=0, column=0)
name_entry = tk.Entry(form_frame)
name_entry.grid(row=0, column=1)

tk.Label(form_frame, text="Age:").grid(row=0, column=2)
age_entry = tk.Entry(form_frame)
age_entry.grid(row=0, column=3)

tk.Label(form_frame, text="Grade:").grid(row=0, column=4)
grade_entry = tk.Entry(form_frame)
grade_entry.grid(row=0, column=5)

# PanedWindow for List and Details
paned = tk.PanedWindow(root, sashrelief=tk.RAISED)
paned.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

# Left: Student List
left_frame = tk.Frame(paned)
tk.Label(left_frame, text="Student List").pack()
student_listbox = tk.Listbox(left_frame)
student_listbox.pack(fill=tk.BOTH, expand=True)
student_listbox.bind("<<ListboxSelect>>", show_details)
paned.add(left_frame)

# Right: Details View
right_frame = tk.Frame(paned)
tk.Label(right_frame, text="Details").pack()
details_text = tk.StringVar()
details_label = tk.Label(right_frame, textvariable=details_text, justify=tk.LEFT, font=("Arial", 12))
details_label.pack(anchor="nw", padx=10, pady=10)
paned.add(right_frame)

root.mainloop()