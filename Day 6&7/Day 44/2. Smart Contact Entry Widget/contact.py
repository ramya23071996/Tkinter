import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class ContactField(ttk.Frame):
    def __init__(self, master, label_text, **kwargs):
        super().__init__(master)
        self.var = tk.StringVar()
        self.label = ttk.Label(self, text=label_text, width=12)
        self.entry = ttk.Entry(self, textvariable=self.var, **kwargs)
        self.clear_btn = ttk.Button(self, text='✖', width=2, command=self.clear)

        self.label.grid(row=0, column=0, padx=(0, 5))
        self.entry.grid(row=0, column=1, sticky='ew')
        self.clear_btn.grid(row=0, column=2, padx=(5, 0))

        self.columnconfigure(1, weight=1)

        # Hover effect
        self.entry.bind('<Enter>', lambda e: self.entry.config(background='#e0f7fa'))
        self.entry.bind('<Leave>', lambda e: self.entry.config(background='white'))

        # Live validation
        self.var.trace_add('write', lambda *args: master.validate_form())

    def get(self):
        return self.var.get().strip()

    def clear(self):
        self.var.set('')

    def is_valid(self):
        return bool(self.get())

class ContactForm(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.fields = []
        self.build_form()
        self.save_btn = ttk.Button(self, text="Save Contact", command=self.save_contact, state='disabled')
        self.save_btn.pack(pady=10)

        # Ctrl+S binding
        master.bind('<Control-s>', lambda e: self.save_contact())

    def build_form(self):
        field_names = ['Name', 'Email', 'Phone']
        for name in field_names:
            field = ContactField(self, name)
            field.pack(fill='x', pady=5, padx=10)
            self.fields.append(field)

    def validate_form(self):
        all_valid = all(field.is_valid() for field in self.fields)
        self.save_btn.config(state='normal' if all_valid else 'disabled')

    def save_contact(self):
        if all(field.is_valid() for field in self.fields):
            data = {field.label.cget('text'): field.get() for field in self.fields}
            messagebox.showinfo("Saved", f"Contact saved:\n{data}")
        else:
            messagebox.showwarning("Incomplete", "Please fill all fields.")

root = tk.Tk()
root.title("Smart Contact Entry")
root.geometry("350x200")
root.resizable(False, False)

form = ContactForm(root)
form.pack(fill='both', expand=True)

root.mainloop()