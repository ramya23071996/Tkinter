import tkinter as tk

# Dummy credentials for validation
VALID_USERNAME = "admin"
VALID_PASSWORD = "password123"

def validate_login():
    username = username_entry.get()
    password = password_entry.get()

    if not username or not password:
        message_label.config(text="Please enter both username and password", fg="red")
    elif username == VALID_USERNAME and password == VALID_PASSWORD:
        message_label.config(text="Login Successful", fg="green")
    else:
        message_label.config(text="Invalid Credentials", fg="red")

def clear_fields():
    username_entry.delete(0, tk.END)
    password_entry.delete(0, tk.END)
    message_label.config(text="")

# GUI setup
root = tk.Tk()
root.title("Login Form")
root.geometry("300x200")
root.resizable(False, False)

# Instruction label
instruction_label = tk.Label(root, text="Enter your login credentials", font=("Arial", 12))
instruction_label.pack(pady=10)

# Username entry
username_entry = tk.Entry(root, width=30)
username_entry.pack(pady=5)
username_entry.insert(0, "Username")

# Password entry (masked)
password_entry = tk.Entry(root, width=30, show="*")
password_entry.pack(pady=5)
password_entry.insert(0, "password123")

# Message label
message_label = tk.Label(root, text="", font=("Arial", 10))
message_label.pack(pady=5)

# Buttons
login_button = tk.Button(root, text="Login", command=validate_login)
login_button.pack(pady=5)

clear_button = tk.Button(root, text="Clear", command=clear_fields)
clear_button.pack()

root.mainloop()