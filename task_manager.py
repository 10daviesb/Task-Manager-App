# task_manager_gui.py

import tkinter as tk
from tkinter import messagebox, filedialog
import json
import os

# --- Global Variables ---
tasks = []
next_id = 1
current_file = None  # Track which file we're working with

# --- Functions ---

def save_tasks():
    global current_file
    if current_file:
        with open(current_file, "w") as f:
            json.dump(tasks, f, indent=4)
        messagebox.showinfo("Save Successful", f"Tasks saved to {current_file}.")
    else:
        save_as_tasks()

def save_as_tasks():
    global current_file
    file_path = filedialog.asksaveasfilename(
        defaultextension=".json",
        filetypes=[("JSON Files", "*.json")],
        title="Save As"
    )
    if file_path:
        current_file = file_path
        save_tasks()

def load_tasks():
    global tasks, next_id, current_file
    file_path = filedialog.askopenfilename(
        defaultextension=".json",
        filetypes=[("JSON Files", "*.json")],
        title="Load Task File"
    )
    if file_path:
        with open(file_path, "r") as f:
            tasks = json.load(f)
        if tasks:
            next_id = max(task["id"] for task in tasks) + 1
        else:
            next_id = 1
        current_file = file_path
        refresh_task_list()

def refresh_task_list():
    tasks.sort(key=lambda x: x["completed"])  # Incomplete first
    task_listbox.delete(0, tk.END)
    for task in tasks:
        status = "✅" if task["completed"] else "❌"
        task_listbox.insert(tk.END, f"{task['id']}. {task['description']} [{status}]")

def add_task(event=None):
    global next_id
    description = task_entry.get().strip()
    if description:
        task = {
            "id": next_id,
            "description": description,
            "completed": False
        }
        tasks.append(task)
        next_id += 1
        task_entry.delete(0, tk.END)
        refresh_task_list()
    else:
        messagebox.showwarning("Input Error", "Task description cannot be empty.")

def complete_task():
    try:
        selected = task_listbox.curselection()
        if not selected:
            messagebox.showinfo("Selection Error", "No task selected.")
            return
        index = selected[0]
        task = tasks[index]
        task["completed"] = not task["completed"]  # Toggle complete/incomplete
        refresh_task_list()
    except IndexError:
        messagebox.showerror("Error", "Invalid selection.")

def delete_task(event=None):
    try:
        selected = task_listbox.curselection()
        if not selected:
            messagebox.showinfo("Selection Error", "No task selected.")
            return
        index = selected[0]
        del tasks[index]
        refresh_task_list()
    except IndexError:
        messagebox.showerror("Error", "Invalid selection.")

def update_complete_button_text(event=None):
    selected = task_listbox.curselection()
    if not selected:
        complete_button.config(text="Complete Task")
        return
    index = selected[0]
    task = tasks[index]
    if task["completed"]:
        complete_button.config(text="Mark Incomplete")
    else:
        complete_button.config(text="Mark Complete")

def new_task_list():
    global tasks, next_id, current_file
    if messagebox.askyesno("New Task List", "Are you sure you want to start a new task list? Unsaved changes will be lost."):
        tasks = []
        next_id = 1
        current_file = None
        refresh_task_list()

def exit_app():
    if messagebox.askokcancel("Exit", "Are you sure you want to exit?"):
        root.destroy()

# --- GUI Setup ---

root = tk.Tk()
root.title("Task Manager")

# --- Menu Bar ---
menu_bar = tk.Menu(root)

file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Save", command=save_tasks)
file_menu.add_command(label="Save As...", command=save_as_tasks)
file_menu.add_command(label="Load", command=load_tasks)
file_menu.add_separator()
file_menu.add_command(label="New", command=new_task_list)
file_menu.add_command(label="Exit", command=exit_app)
menu_bar.add_cascade(label="File", menu=file_menu)

root.config(menu=menu_bar)

# --- Top Frame for Adding Tasks ---
top_frame = tk.Frame(root)
top_frame.pack(pady=10)

task_entry = tk.Entry(top_frame, width=40)
task_entry.pack(side=tk.LEFT, padx=(0, 10))
task_entry.bind("<Return>", add_task)

add_button = tk.Button(top_frame, text="Add Task", command=add_task)
add_button.pack(side=tk.LEFT)

# --- Listbox to Show Tasks ---
task_listbox = tk.Listbox(root, width=50, height=10)
task_listbox.pack(pady=10)
task_listbox.bind("<Delete>", delete_task)
task_listbox.bind("<<ListboxSelect>>", update_complete_button_text)

# --- Bottom Frame for Actions ---
bottom_frame = tk.Frame(root)
bottom_frame.pack(pady=10)

complete_button = tk.Button(bottom_frame, text="Complete Task", command=complete_task)
complete_button.pack(side=tk.LEFT, padx=5)

delete_button = tk.Button(bottom_frame, text="Delete Task", command=delete_task)
delete_button.pack(side=tk.LEFT, padx=5)

# --- Start the App ---

refresh_task_list()
root.mainloop()
