import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import time

class PasswordEntry(ttk.Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master)
        self.var = tk.StringVar()
        self.entry = ttk.Entry(self, textvariable=self.var, show='*', **kwargs)
        self.entry.pack(side='left', fill='x', expand=True)

        self.showing = False
        self.eye_icon = tk.Label(self, text='👁️', cursor='hand2', foreground='gray')
        self.eye_icon.pack(side='right', padx=5)
        self.eye_icon.bind('<Button-1>', self.toggle_password)
        self.eye_icon.bind('<Enter>', lambda e: self.eye_icon.config(foreground='black'))
        self.eye_icon.bind('<Leave>', lambda e: self.eye_icon.config(foreground='gray'))

    def toggle_password(self, event=None):
        self.showing = not self.showing
        self.entry.config(show='' if self.showing else '*')

    def get(self):
        return self.var.get()

    def clear(self):
        self.var.set('')

def validate_fields(*args):
    username = username_var.get().strip()
    password = password_entry.get().strip()
    login_btn.config(state='normal' if username and password else 'disabled')

def trigger_login(event=None):
    login()

def login():
    username = username_var.get().strip()
    password = password_entry.get().strip()

    if username == "admin" and password == "secret":
        messagebox.showinfo("Login", "Login successful!")
    else:
        messagebox.showerror("Login", "Wrong credentials. Try again in 5 seconds.")
        disable_widgets()
        root.after(5000, enable_widgets)

def disable_widgets():
    username_entry.config(state='disabled')
    password_entry.entry.config(state='disabled')
    login_btn.config(state='disabled')

def enable_widgets():
    username_entry.config(state='normal')
    password_entry.entry.config(state='normal')
    validate_fields()

root = tk.Tk()
root.title("Secure Login")
root.geometry("300x150")
root.resizable(False, False)

username_var = tk.StringVar()
username_var.trace_add('write', validate_fields)

username_label = ttk.Label(root, text="Username:")
username_label.pack(pady=(10, 0))
username_entry = ttk.Entry(root, textvariable=username_var)
username_entry.pack(fill='x', padx=20)

password_label = ttk.Label(root, text="Password:")
password_label.pack(pady=(10, 0))
password_entry = PasswordEntry(root)
password_entry.pack(fill='x', padx=20)

login_btn = ttk.Button(root, text="Login", command=login, state='disabled')
login_btn.pack(pady=15)

# Bind events
username_entry.bind('<KeyRelease>', validate_fields)
password_entry.entry.bind('<KeyRelease>', validate_fields)
root.bind('<Return>', trigger_login)

root.mainloop()