import tkinter as tk
from tkinter import ttk
import time

def draw_shape(event):
    shape = shape_selector.get()
    size = int(size_spinbox.get())
    x, y = event.x, event.y
    tag = f"{shape}_{x}_{y}"

    # Animate growth
    for i in range(1, size + 1, 2):
        canvas.delete(tag)
        if shape == "Rectangle":
            canvas.create_rectangle(x - i, y - i, x + i, y + i, fill="skyblue", tags=tag)
        elif shape == "Oval":
            canvas.create_oval(x - i, y - i, x + i, y + i, fill="lightgreen", tags=tag)
        elif shape == "Line":
            canvas.create_line(x - i, y - i, x + i, y + i, fill="orange", width=2, tags=tag)
        root.update()
        time.sleep(0.01)

    shape_list.insert(tk.END, f"{shape} at ({x},{y})")

def clear_canvas():
    canvas.delete("all")
    shape_list.delete(0, tk.END)

# GUI setup
root = tk.Tk()
root.title("Interactive Drawing Pad")
root.geometry("600x450")
root.resizable(False, False)

# Canvas
canvas = tk.Canvas(root, bg="white", width=400, height=400)
canvas.grid(row=0, column=0, rowspan=6, padx=10, pady=10)
canvas.bind("<Button-1>", draw_shape)

# Shape selector
tk.Label(root, text="Select Shape:").grid(row=0, column=1, sticky="w")
shape_selector = ttk.Combobox(root, values=["Rectangle", "Oval", "Line"], state="readonly")
shape_selector.grid(row=1, column=1, padx=5)
shape_selector.set("Rectangle")

# Size selector
tk.Label(root, text="Size:").grid(row=2, column=1, sticky="w")
size_spinbox = tk.Spinbox(root, from_=10, to=100, width=5)
size_spinbox.grid(row=3, column=1, padx=5)
size_spinbox.delete(0, tk.END)
size_spinbox.insert(0, "30")

# Shape list with scrollbar
tk.Label(root, text="Shapes Drawn:").grid(row=4, column=1, sticky="w")
list_frame = tk.Frame(root)
list_frame.grid(row=5, column=1, padx=5, pady=5)

scrollbar = tk.Scrollbar(list_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

shape_list = tk.Listbox(list_frame, height=10, width=25, yscrollcommand=scrollbar.set)
shape_list.pack(side=tk.LEFT)
scrollbar.config(command=shape_list.yview)

# Clear button
clear_btn = tk.Button(root, text="Clear Canvas", command=clear_canvas)
clear_btn.grid(row=6, column=0, columnspan=2, pady=10)

root.mainloop()