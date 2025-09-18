"""
Task Manager CLI - Interactive Version
--------------------------------------
Manage your tasks directly from the terminal with statuses:
    - todo
    - in-progress
    - done

Features:
    ✅ Add new tasks
    ✅ Update existing tasks
    ✅ Delete tasks
    ✅ Mark tasks as in-progress or done
    ✅ List tasks (all or by status)
    ✅ Interactive mode with multiple commands
"""

import os
import sys
import io
import json

# Force UTF-8 encoding for Windows console
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='ignore')

# Control whether emojis are shown
USE_EMOJI = os.getenv("USE_EMOJI", "1") == "1"

def safe_print(msg: str):
    """Print message safely with optional emoji support."""
    if not USE_EMOJI:
        msg = msg.encode("ascii", "ignore").decode()
    print(msg)

class TaskManager:
    """A simple task manager that stores tasks in a JSON file."""

    def __init__(self, filename="tasks.json"):
        self.filename = filename
        self.tasks = self.load_tasks()

    # ------------------------------------------------------------------
    # File Handling
    # ------------------------------------------------------------------
    def load_tasks(self):
        if not os.path.exists(self.filename):
            print(f"[INFO] {self.filename} not found. Creating a new one.")
            with open(self.filename, "w", encoding="utf-8") as f:
                json.dump([], f, indent=4)
            return []

        with open(self.filename, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                print(f"[WARN] {self.filename} is corrupted. Resetting.")
                with open(self.filename, "w", encoding="utf-8") as f:
                    json.dump([], f, indent=4)
                return []

    def save_tasks(self):
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(self.tasks, f, indent=4)

    # ------------------------------------------------------------------
    # Command Implementations
    # ------------------------------------------------------------------
    def show_start(self):
        print("\n👋 Welcome to Task Manager CLI!")
        print("Easily track your tasks with statuses: todo, in-progress, and done.")
        print("\n👉 Quickstart examples:")
        print("   add Buy groceries")
        print("   list")
        print("Type 'help' to see available commands, 'exit' to quit.\n")

    def show_help(self):
        print("\n📖 Task Manager CLI - Commands Reference\n")
        print("General:")
        print("  start                   Show greeting and quickstart guide")
        print("  help                    Show this list of commands")
        print("  exit, quit              Exit the application\n")
        print("Tasks:")
        print("  add <description>       Add a new task")
        print("  update <id> <desc>      Update task description")
        print("  delete <id>             Delete a task by ID\n")
        print("Status updates:")
        print("  mark-in-progress <id>   Mark task as 'in-progress'")
        print("  mark-done <id>          Mark task as 'done'\n")
        print("Listing:")
        print("  list                    Show all tasks")
        print("  list todo               Show only 'todo' tasks")
        print("  list in-progress        Show only 'in-progress' tasks")
        print("  list done               Show only 'done' tasks\n")

    def add_task(self, description):
        new_task = {
            "id": len(self.tasks) + 1,
            "description": description,
            "status": "todo",
            "created_at": "",
            "updated_at": "",
        }
        self.tasks.append(new_task)
        self.save_tasks()
        safe_print(f"✅ Task added successfully (ID: {new_task['id']})")

    def update_task(self, task_id, description):
        for task in self.tasks:
            if task["id"] == task_id:
                task["description"] = description
                task["updated_at"] = ""
                safe_print(f"✏️ Task {task_id} updated.")
                self.save_tasks()
                return
        safe_print(f"⚠️ No task found with ID={task_id}")

    def delete_task(self, task_id):
        before = len(self.tasks)
        self.tasks = [t for t in self.tasks if t["id"] != task_id]
        if len(self.tasks) < before:
            safe_print(f"🗑️ Task {task_id} deleted.")
            self.save_tasks()
        else:
            safe_print(f"⚠️ No task found with ID={task_id}")

    def mark_task(self, task_id, status):
        for task in self.tasks:
            if task["id"] == task_id:
                task["status"] = status
                task["updated_at"] = ""
                safe_print(f"✅ Task {task_id} marked as {status}.")
                self.save_tasks()
                return
        safe_print(f"⚠️ No task found with ID={task_id}")

    def list_tasks(self, status=None):
        filtered = self.tasks if not status else [t for t in self.tasks if t["status"] == status]
        if not filtered:
            safe_print("📂 No tasks found.")
            return
        for task in filtered:
            print(f"[{task['id']}] {task['description']} - {task['status']}")

    # ------------------------------------------------------------------
    # Interactive CLI Loop
    # ------------------------------------------------------------------
    def run(self):
        self.show_start()

        while True:
            try:
                user_input = input("task-manager> ").strip()
            except (KeyboardInterrupt, EOFError):
                print("\nExiting Task Manager CLI. Bye! 👋")
                break

            if not user_input:
                continue
            if user_input.lower() in ("exit", "quit"):
                print("Goodbye! 👋")
                break

            parts = user_input.split()
            cmd = parts[0]
            args = parts[1:]

            if cmd == "help":
                self.show_help()
            elif cmd == "start":
                self.show_start()
            elif cmd == "add":
                if args:
                    self.add_task(" ".join(args))
                else:
                    print("⚠️ Usage: add <description>")
            elif cmd == "update":
                if len(args) >= 2 and args[0].isdigit():
                    self.update_task(int(args[0]), " ".join(args[1:]))
                else:
                    print("⚠️ Usage: update <id> <description>")
            elif cmd == "delete":
                if args and args[0].isdigit():
                    self.delete_task(int(args[0]))
                else:
                    print("⚠️ Usage: delete <id>")
            elif cmd == "mark-in-progress":
                if args and args[0].isdigit():
                    self.mark_task(int(args[0]), "in-progress")
                else:
                    print("⚠️ Usage: mark-in-progress <id>")
            elif cmd == "mark-done":
                if args and args[0].isdigit():
                    self.mark_task(int(args[0]), "done")
                else:
                    print("⚠️ Usage: mark-done <id>")
            elif cmd == "list":
                if args:
                    if args[0] in ["todo", "in-progress", "done"]:
                        self.list_tasks(args[0])
                    else:
                        print("⚠️ Invalid status. Use: todo, in-progress, done")
                else:
                    self.list_tasks()
            else:
                print(f"⚠️ Unknown command: {cmd}. Type 'help' to see commands.")


# ----------------------------------------------------------------------
# Entry Point
# ----------------------------------------------------------------------
if __name__ == "__main__":
    cli = TaskManager()
    cli.run()
