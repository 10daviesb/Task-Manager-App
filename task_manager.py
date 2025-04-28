# task_manager_gui.py

import tkinter as tk
from tkinter import messagebox, filedialog, simpledialog
import json
import os

# --- Themes ---
themes = {
    "light": {
        "bg": "#f0f0f0",
        "fg": "#000000",
        "entry_bg": "#ffffff",
        "entry_fg": "#000000",
        "button_bg": "#e0e0e0",
        "button_fg": "#000000",
        "listbox_bg": "#ffffff",
        "listbox_fg": "#000000",
        "select_bg": "#c0c0ff",
        "select_fg": "#000000"
    },
    "dark": {
        "bg": "#2e2e2e",
        "fg": "#ffffff",
        "entry_bg": "#3e3e3e",
        "entry_fg": "#ffffff",
        "button_bg": "#4e4e4e",
        "button_fg": "#ffffff",
        "listbox_bg": "#3e3e3e",
        "listbox_fg": "#ffffff",
        "select_bg": "#6060a0",
        "select_fg": "#ffffff"
    }
}
current_theme = "light"  # Default

# --- Global Variables ---
tasks = []
next_id = 1
current_file = None

# --- File Operations ---
def silent_save_tasks():
    global current_file, tasks
    if current_file:
        with open(current_file, "w") as f:
            json.dump(tasks, f, indent=4)

def save_tasks():
    global current_file
    if current_file and os.path.exists(current_file):
        if messagebox.askyesno("Confirm Save", f"Overwrite {current_file}?"):
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
        with open(current_file, "w") as f:
            json.dump(tasks, f, indent=4)
        messagebox.showinfo("Save Successful", f"Tasks saved to {current_file}.")

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
        next_id = max((task["id"] for task in tasks), default=0) + 1
        current_file = file_path
        refresh_task_list()

def create_new_task_list():
    global tasks, next_id, current_file
    if messagebox.askyesno("New Task List", "Start a new task list? Unsaved changes will be lost."):
        tasks = []
        next_id = 1
        current_file = None
        refresh_task_list()

# --- Task Operations ---
def refresh_task_list():
    tasks.sort(key=lambda x: x["completed"])
    task_listbox.delete(0, tk.END)
    for task in tasks:
        status = "✅" if task["completed"] else "❌"
        task_listbox.insert(tk.END, f"{task['id']}. {task['description']} [{status}]")
    update_stats()
    check_all_completed()

def add_task(event=None):
    global next_id
    description = task_entry.get().strip()
    if description:
        task = {"id": next_id, "description": description, "completed": False}
        tasks.append(task)
        next_id += 1
        task_entry.delete(0, tk.END)
        silent_save_tasks()
        refresh_task_list()
    else:
        messagebox.showwarning("Input Error", "Task description cannot be empty.")

def complete_task():
    selected = task_listbox.curselection()
    if not selected:
        messagebox.showinfo("Selection Error", "No task selected.")
        return
    index = selected[0]
    tasks[index]["completed"] = not tasks[index]["completed"]
    silent_save_tasks()
    refresh_task_list()

def delete_task(event=None):
    selected = task_listbox.curselection()
    if not selected:
        messagebox.showinfo("Selection Error", "No task selected.")
        return
    index = selected[0]
    del tasks[index]
    silent_save_tasks()
    refresh_task_list()

def edit_task():
    selected = task_listbox.curselection()
    if not selected:
        messagebox.showinfo("Selection Error", "No task selected.")
        return
    index = selected[0]
    task = tasks[index]
    new_desc = simpledialog.askstring("Edit Task", "Enter new description:", initialvalue=task["description"])
    if new_desc and new_desc.strip():
        tasks[index]["description"] = new_desc.strip()
        silent_save_tasks()
        refresh_task_list()

def update_complete_button_text(event=None):
    selected = task_listbox.curselection()
    if not selected:
        complete_button.config(text="Complete Task")
        return
    index = selected[0]
    if tasks[index]["completed"]:
        complete_button.config(text="Mark Incomplete")
    else:
        complete_button.config(text="Mark Complete")

def update_stats():
    total = len(tasks)
    completed = sum(1 for t in tasks if t["completed"])
    stats_label.config(text=f"Tasks: {total} | Completed: {completed}")

def check_all_completed():
    if tasks and all(task["completed"] for task in tasks):
        messagebox.showinfo("Congratulations!", "All tasks completed! Great job!")

# --- GUI Setup ---
root = tk.Tk()
root.title("Task Manager")
root.minsize(500, 450)
root.iconbitmap('icon.ico')

# Context Menu
context_menu = tk.Menu(root, tearoff=0)

# Menu Bar
menu_bar = tk.Menu(root)

# File Menu
file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="New", command=create_new_task_list)
file_menu.add_command(label="Save", command=save_tasks)
file_menu.add_command(label="Save As...", command=save_as_tasks)
file_menu.add_command(label="Load", command=load_tasks)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)
menu_bar.add_cascade(label="File", menu=file_menu)

# View Menu
view_menu = tk.Menu(menu_bar, tearoff=0)
view_menu.add_command(label="Toggle Light/Dark Mode", command=lambda: toggle_theme())
menu_bar.add_cascade(label="View", menu=view_menu)

# Help Menu
help_menu = tk.Menu(menu_bar, tearoff=0)
help_menu.add_command(label="About Task Manager", command=lambda: messagebox.showinfo(
    "About Task Manager", "Task Manager v1.0\nA simple task manager built with Python and Tkinter.\n\n© 2025 Bradley Davies"
))
menu_bar.add_cascade(label="Help", menu=help_menu)

root.config(menu=menu_bar)

# Top Frame
top_frame = tk.Frame(root)
top_frame.pack(fill='x', pady=10)

task_entry = tk.Entry(top_frame, width=40)
task_entry.pack(side=tk.LEFT, padx=(0, 10))
task_entry.bind("<Return>", add_task)

add_button = tk.Button(top_frame, text="Add Task", command=add_task)
add_button.pack(side=tk.LEFT)

# Listbox
task_listbox = tk.Listbox(root, height=10)
task_listbox.pack(fill='both', expand=True, pady=10)
task_listbox.bind("<Delete>", delete_task)
task_listbox.bind("<<ListboxSelect>>", update_complete_button_text)
task_listbox.bind("<Button-3>", context_menu)

# Bottom Frame
bottom_frame = tk.Frame(root)
bottom_frame.pack(fill='x', pady=10)

complete_button = tk.Button(bottom_frame, text="Complete Task", command=complete_task)
complete_button.pack(side=tk.LEFT, padx=5)

delete_button = tk.Button(bottom_frame, text="Delete Task", command=delete_task)
delete_button.pack(side=tk.LEFT, padx=5)

stats_label = tk.Label(root, text="Tasks: 0 | Completed: 0")
stats_label.pack(pady=5)

# Theme Functions
def apply_theme():
    colors = themes[current_theme]
    root.config(bg=colors["bg"], padx=20, pady=20)
    top_frame.config(bg=colors["bg"])
    bottom_frame.config(bg=colors["bg"])
    task_entry.config(
        bg=colors["entry_bg"], fg=colors["entry_fg"], insertbackground=colors["fg"]
    )
    for btn in (add_button, complete_button, delete_button):
        btn.config(
            bg=colors["button_bg"], fg=colors["button_fg"], activebackground=colors["select_bg"], activeforeground=colors["select_fg"]
        )
    task_listbox.config(
        bg=colors["listbox_bg"], fg=colors["listbox_fg"],
        selectbackground=colors["select_bg"], selectforeground=colors["select_fg"]
    )
    stats_label.config(bg=colors["bg"], fg=colors["fg"])

def toggle_theme():
    global current_theme
    current_theme = "dark" if current_theme == "light" else "light"
    apply_theme()

# Initialize
apply_theme()
refresh_task_list()
root.mainloop()