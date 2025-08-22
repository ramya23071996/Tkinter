import tkinter as tk
from tkinter import ttk

# Create main window
root = tk.Tk()
root.title("Event Registration — Vetri Technology Solutions")
root.geometry("400x300")
root.resizable(False, False)


# Frame to group form fields
form_frame = ttk.Frame(root, padding="20")
form_frame.grid(row=0, column=0, sticky="nsew")

# Name Label and Entry
ttk.Label(form_frame, text="Name:").grid(row=0, column=0, sticky="w", pady=5)
name_entry = ttk.Entry(form_frame, width=30)
name_entry.grid(row=0, column=1, pady=5)

# Email Label and Entry
ttk.Label(form_frame, text="Email:").grid(row=1, column=0, sticky="w", pady=5)
email_entry = ttk.Entry(form_frame, width=30)
email_entry.grid(row=1, column=1, pady=5)

# Result Label
result_label = ttk.Label(root, text="", foreground="green", font=("Arial", 11))
result_label.grid(row=2, column=0, pady=10)

# Submit function
def register():
    name = name_entry.get().strip()
    email = email_entry.get().strip()
    if name and email:
        result_label.config(text=f"Registered: {name} ({email})")
    else:
        result_label.config(text="Please enter both name and email.", foreground="red")

# Bind <Return> key to register
root.bind("<Return>", lambda event: register())

# Register Button
button_frame = ttk.Frame(root, padding="10")
button_frame.grid(row=1, column=0)

ttk.Button(button_frame, text="Register", command=register).grid(row=0, column=0)

# Run the app
root.mainloop()