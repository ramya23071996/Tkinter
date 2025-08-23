import tkinter as tk

def submit_form():
    name = name_entry.get().strip()
    email = email_entry.get().strip()
    message = message_text.get("1.0", tk.END).strip()

    if not name or not email or not message:
        result_label.config(text="All fields are required.", fg="red")
    elif "@" not in email:
        result_label.config(text="Invalid email address.", fg="red")
    else:
        result_label.config(
            text=f"Thank you, {name}!\nWe received your message:\n\"{message}\"",
            fg="green"
        )

def clear_form():
    name_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)
    message_text.delete("1.0", tk.END)
    result_label.config(text="")

# GUI setup
root = tk.Tk()
root.title("Contact Us Form")
root.geometry("400x350")
root.resizable(False, False)

# Labels and Entry widgets
tk.Label(root, text="Name:", font=("Arial", 10)).pack(pady=(10, 0))
name_entry = tk.Entry(root, width=40)
name_entry.pack()

tk.Label(root, text="Email:", font=("Arial", 10)).pack(pady=(10, 0))
email_entry = tk.Entry(root, width=40)
email_entry.pack()

tk.Label(root, text="Message:", font=("Arial", 10)).pack(pady=(10, 0))
message_text = tk.Text(root, width=40, height=5)
message_text.pack()

# Buttons
submit_btn = tk.Button(root, text="Submit", command=submit_form)
submit_btn.pack(pady=10)

clear_btn = tk.Button(root, text="Clear", command=clear_form)
clear_btn.pack()

# Dynamic result label
result_label = tk.Label(root, text="", font=("Arial", 10), wraplength=350)
result_label.pack(pady=10)

root.mainloop()