import tkinter as tk
from tkinter import ttk

# Create main window
root = tk.Tk()
root.title("Feedback Collector")
root.geometry("500x400")
root.resizable(False, False)

# Frame to group form fields
form_frame = ttk.Frame(root, padding="20")
form_frame.grid(row=0, column=0, sticky="nsew")

# Name Label and Entry
ttk.Label(form_frame, text="Name:").grid(row=0, column=0, sticky="w", pady=5)
name_entry = ttk.Entry(form_frame, width=40)
name_entry.grid(row=0, column=1, pady=5)

# Email Label and Entry
ttk.Label(form_frame, text="Email:").grid(row=1, column=0, sticky="w", pady=5)
email_entry = ttk.Entry(form_frame, width=40)
email_entry.grid(row=1, column=1, pady=5)

# Feedback Label
ttk.Label(form_frame, text="Feedback:").grid(row=2, column=0, sticky="nw", pady=5)

# Text widget with Scrollbar
feedback_frame = ttk.Frame(form_frame)
feedback_frame.grid(row=2, column=1, pady=5)

feedback_text = tk.Text(feedback_frame, width=40, height=10, wrap="word")
feedback_text.grid(row=0, column=0)

scrollbar = ttk.Scrollbar(feedback_frame, orient="vertical", command=feedback_text.yview)
scrollbar.grid(row=0, column=1, sticky="ns")
feedback_text.config(yscrollcommand=scrollbar.set)

# Thank-you message Label
thank_you_label = ttk.Label(root, text="", foreground="green", font=("Arial", 11))
thank_you_label.grid(row=2, column=0, pady=10)

# Submit and Reset functions
def submit_feedback():
    name = name_entry.get().strip()
    email = email_entry.get().strip()
    feedback = feedback_text.get("1.0", tk.END).strip()

    if not name or not email or not feedback:
        thank_you_label.config(text="Please fill in all fields.", foreground="red")
    else:
        thank_you_label.config(text=f"Thank you, {name}, for your feedback!", foreground="green")
        # You can add logic here to save feedback to a file or database

def reset_form():
    name_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)
    feedback_text.delete("1.0", tk.END)
    thank_you_label.config(text="")

# Buttons
button_frame = ttk.Frame(root, padding="10")
button_frame.grid(row=1, column=0)

ttk.Button(button_frame, text="Submit", command=submit_feedback).grid(row=0, column=0, padx=10)
ttk.Button(button_frame, text="Reset", command=reset_form).grid(row=0, column=1, padx=10)

# Run the app
root.mainloop()