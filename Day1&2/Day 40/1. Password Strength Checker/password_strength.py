import tkinter as tk
from tkinter import ttk

# Create main window
root = tk.Tk()
root.title("Password Strength Checker")
root.geometry("400x250")
root.resizable(False, False)

# Top Frame for grouping
top_frame = ttk.Frame(root, padding="20")
top_frame.grid(row=0, column=0, sticky="nsew")

# Password Label and Entry
ttk.Label(top_frame, text="Enter Password:").grid(row=0, column=0, sticky="w", pady=5)
password_entry = ttk.Entry(top_frame, show="*", width=30)
password_entry.grid(row=0, column=1, pady=5)

# Strength Label
strength_label = ttk.Label(top_frame, text="Strength: ", font=("Arial", 10))
strength_label.grid(row=1, column=0, columnspan=2, pady=10)

# Function to check password strength
def check_strength(event=None):
    pwd = password_entry.get()
    root.title("Checking password...")
    strength = "Weak"

    if len(pwd) >= 8:
        if any(c.isdigit() for c in pwd) and any(c.isalpha() for c in pwd):
            if any(c in "!@#$%^&*()-_=+[]{}|;:'\",.<>?/`~" for c in pwd):
                strength = "Strong"
            else:
                strength = "Medium"
    elif len(pwd) >= 5:
        strength = "Medium"

    strength_label.config(text=f"Strength: {strength}")
    root.title("Password Strength Checker")

# Bind KeyRelease to password entry
password_entry.bind("<KeyRelease>", check_strength)

# Submit and Clear functions
def submit():
    check_strength()
    tk.messagebox.showinfo("Submitted", "Password submitted successfully!")

def clear():
    password_entry.delete(0, tk.END)
    strength_label.config(text="Strength: ")
    root.title("Password Strength Checker")

# Buttons
button_frame = ttk.Frame(root, padding="10")
button_frame.grid(row=1, column=0)

ttk.Button(button_frame, text="Submit", command=submit).grid(row=0, column=0, padx=10)
ttk.Button(button_frame, text="Clear", command=clear).grid(row=0, column=1, padx=10)

# Run the app
root.mainloop()