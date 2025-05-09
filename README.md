# Task Manager GUI

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Completed-blueviolet)
![Last Commit](https://img.shields.io/github/last-commit/10daviesb/task-manager-app)

A simple, stylish Task Manager desktop app built with **Python** and **Tkinter**.

Manage your daily tasks easily:
- Add, complete, edit, and delete tasks
- Save and load task lists
- Light and dark theme toggle
- Task stats tracker (Total / Completed)
- Celebration popup when all tasks are completed
- Right-click quick actions
- Clean, polished UI with custom icons

---

## 📸 Screenshots

### Light Mode

![Light Mode](screenshots/Lightmode.png)

### Dark Mode

![Dark Mode](screenshots/Darkmode.png)

---

## 🚀 Features

- **Task Management:** Add, complete/incomplete, edit, delete tasks
- **Saving and Loading:** Save your task list to `.json` files and load them back later
- **Themes:** Switch between Light and Dark modes from the View menu
- **Statistics:** Track the total number of tasks and completed tasks
- **Celebrate Progress:** Get a congratulatory popup when all tasks are complete
- **Context Menu:** Right-click on tasks to quickly complete, edit, or delete them
- **Custom Icon:** Beautiful custom app icon (`icon.ico`)

---

## 🛠 Installation

1. Make sure you have **Python 3.x** installed.
2. Clone or download this repository:
    ```bash
    git clone https://github.com/10daviesb/task-manager-gui.git
    cd task-manager-gui
    ```
3. Install required packages (all standard libraries, no external requirements).
4. Make sure an `icon.ico` file is in the same folder as the script.
5. Run the app:
    ```bash
    python task_manager_gui.py
    ```

---

## 📄 File Structure

```
task-manager-gui/ 
├── screenshots/                            # Folder containing app screenshots 
│ ├── Lightmode.png 
│ └── Darkmode.png 
├── task_manager_gui.py                     # Main Python GUI application 
├── icon.ico                                # Custom icon for the app window 
├── README.md                               # Project overview and usage guide 
└── LICENSE                                 # MIT License for open-source use
```