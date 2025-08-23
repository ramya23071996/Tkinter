import tkinter as tk
from tkinter import ttk
import random

# Global flags
paused = False
race_running = False

def start_race():
    global paused, race_running
    paused = False
    race_running = True
    car1_x, car2_x = 10, 40
    canvas.delete("car")
    canvas.create_rectangle(car1_x, 100, car1_x + 30, 130, fill="red", tags="car1")
    canvas.create_rectangle(car2_x, 200, car2_x + 30, 230, fill="blue", tags="car2")

    mode = mode_selector.get()
    interval = int(speed_spinbox.get())

    def move():
        nonlocal car1_x, car2_x
        if not race_running or paused:
            return

        if mode == "Slow":
            car1_x += 2
            car2_x += 2
        elif mode == "Fast":
            car1_x += 6
            car2_x += 6
        elif mode == "Random":
            car1_x += random.randint(2, 6)
            car2_x += random.randint(2, 6)

        canvas.coords("car1", car1_x, 100, car1_x + 30, 130)
        canvas.coords("car2", car2_x, 200, car2_x + 30, 230)

        if car1_x >= 350 or car2_x >= 350:
            winner = "Red Car" if car1_x > car2_x else "Blue Car"
            race_history.insert(tk.END, f"{winner} won ({mode} mode)")
            return
        root.after(interval, move)

    move()

def toggle_pause(event):
    global paused
    paused = not paused
    if not paused and race_running:
        start_race()

def clear_history():
    race_history.delete(0, tk.END)

# GUI setup
root = tk.Tk()
root.title("Race Car Animation")
root.geometry("600x400")
root.resizable(False, False)

# Canvas with road background
canvas = tk.Canvas(root, bg="gray", width=400, height=300)
canvas.grid(row=0, column=0, rowspan=6, padx=10, pady=10)
canvas.bind("<Button-1>", toggle_pause)

# Combobox for race mode
tk.Label(root, text="Race Mode:").grid(row=0, column=1, sticky="w")
mode_selector = ttk.Combobox(root, values=["Slow", "Fast", "Random"], state="readonly")
mode_selector.grid(row=1, column=1, padx=5)
mode_selector.set("Slow")

# Spinbox for speed control
tk.Label(root, text="Speed (ms):").grid(row=2, column=1, sticky="w")
speed_spinbox = tk.Spinbox(root, from_=10, to=200, width=5)
speed_spinbox.grid(row=3, column=1, padx=5)
speed_spinbox.delete(0, tk.END)
speed_spinbox.insert(0, "50")

# Start button
start_btn = tk.Button(root, text="Start Race", command=start_race)
start_btn.grid(row=4, column=1, pady=5)

# Race history listbox with scrollbar
tk.Label(root, text="Race History:").grid(row=5, column=1, sticky="w")
history_frame = tk.Frame(root)
history_frame.grid(row=6, column=1, padx=5, pady=5)

scrollbar = tk.Scrollbar(history_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

race_history = tk.Listbox(history_frame, height=8, width=25, yscrollcommand=scrollbar.set)
race_history.pack(side=tk.LEFT)
scrollbar.config(command=race_history.yview)

# Clear history button
clear_btn = tk.Button(root, text="Clear History", command=clear_history)
clear_btn.grid(row=7, column=1, pady=5)

root.mainloop()