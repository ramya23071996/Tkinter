import tkinter as tk
from tkinter import messagebox

# Create main window
root = tk.Tk()
root.title("Login — Cherii Bakery")
root.geometry("400x300")
root.resizable(False, False)

# Optional: Set window icon (requires .ico file)
# root.iconbitmap("icon.ico")

# Frame for login form
form_frame = tk.Frame(root, padx=20, pady=20)
form_frame.pack()

# Username Label and Entry
tk.Label(form_frame, text="Username:", font=("Arial", 12)).pack(anchor='w')
username_entry = tk.Entry(form_frame, width=30)
username_entry.pack(pady=5)

# Password Label and Entry
tk.Label(form_frame, text="Password:", font=("Arial", 12)).pack(anchor='w')
password_entry = tk.Entry(form_frame, show="*", width=30)
password_entry.pack(pady=5)

# Message Label for feedback
message_label = tk.Label(form_frame, text="", fg="red", font=("Arial", 10))
message_label.pack(pady=5)

# Welcome Frame (hidden initially)
welcome_frame = tk.Frame(root, padx=20, pady=20)

def login():
    username = username_entry.get()
    password = password_entry.get()
    if not username or not password:
        message_label.config(text="Please enter both username and password.")
    else:
        form_frame.pack_forget()
        welcome_frame.pack()
        tk.Label(welcome_frame, text=f"Welcome, {username}!", font=("Arial", 16), fg="green").pack()

def clear():
    username_entry.delete(0, tk.END)
    password_entry.delete(0, tk.END)
    message_label.config(text="")

# Buttons
btn_frame = tk.Frame(form_frame)
btn_frame.pack(pady=10)

tk.Button(btn_frame, text="Login", command=login, width=10).pack(side='left', padx=5)
tk.Button(btn_frame, text="Clear", command=clear, width=10).pack(side='left', padx=5)

# Run the app
root.mainloop()