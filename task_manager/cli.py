"""
Task Manager CLI
----------------
A simple command-line tool to manage tasks with different statuses:
    - todo
    - in-progress
    - done

Features:
    ✅ Add new tasks
    ✅ Update existing tasks
    ✅ Delete tasks
    ✅ Mark tasks as in-progress or done
    ✅ List tasks (all or by status)

Example usage:
    $ task-cli add "Buy groceries"
    $ task-cli update 1 "Buy groceries and cook dinner"
    $ task-cli mark-in-progress 1
    $ task-cli mark-done 1
    $ task-cli list done
"""

import os
import sys
import io
import json
import argparse

# Force UTF-8 encoding for Windows console
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='ignore')

# Control whether emojis are shown
USE_EMOJI = os.getenv("USE_EMOJI", "1") == "1"

def safe_print(msg: str):
    """
    Print message safely:
    - Keep emojis if USE_EMOJI=True
    - Strip non-ASCII for tests/Windows subprocess
    """
    if not USE_EMOJI:
        msg = msg.encode("ascii", "ignore").decode()
    print(msg)

class TaskManager:
    """A simple task manager that stores tasks in a JSON file."""

    def __init__(self, filename="tasks.json"):
        """
        Initialize the task manager.

        Args:
            filename (str): Path to the JSON file used for storing tasks.
        """
        self.filename = filename
        self.tasks = self.load_tasks()

    # ----------------------------------------------------------------------
    # File Handling
    # ----------------------------------------------------------------------
    def load_tasks(self):
        """
        Load existing tasks from JSON file, or create a new one if missing.

        Returns:
            list: A list of task dictionaries.
        """
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
        """Save the current list of tasks back to the JSON file."""
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(self.tasks, f, indent=4)

    # ----------------------------------------------------------------------
    # CLI Runner
    # ----------------------------------------------------------------------
    def run(self):
        """Parse command-line arguments and execute the selected command."""
        parser = argparse.ArgumentParser(
            description="📌 Task Manager CLI - Manage your tasks directly from the terminal"
        )
        subparsers = parser.add_subparsers(dest="command")

        # --- START and HELP ---
        subparsers.add_parser("start", help="Show greeting and quickstart guide")
        subparsers.add_parser("help", help="Show available commands")

        # --- ADD ---
        add_parser = subparsers.add_parser("add", help="Add a new task")
        add_parser.add_argument("description", help="Description of the task")

        # --- UPDATE ---
        update_parser = subparsers.add_parser("update", help="Update a task's description")
        update_parser.add_argument("id", type=int, help="Task ID")
        update_parser.add_argument("description", help="New description")

        # --- DELETE ---
        delete_parser = subparsers.add_parser("delete", help="Delete a task by ID")
        delete_parser.add_argument("id", type=int, help="Task ID")

        # --- MARK STATUS ---
        mark_in_progress = subparsers.add_parser("mark-in-progress", help="Mark a task as in-progress")
        mark_in_progress.add_argument("id", type=int, help="Task ID")

        mark_done = subparsers.add_parser("mark-done", help="Mark a task as done")
        mark_done.add_argument("id", type=int, help="Task ID")

        # --- LIST ---
        list_parser = subparsers.add_parser("list", help="List tasks (optionally filter by status)")
        list_parser.add_argument(
            "status",
            nargs="?",
            choices=["todo", "in-progress", "done"],
            help="Optional filter by status",
        )

        args = parser.parse_args()

        # ------------------------------------------------------------------
        # Command Handlers
        # ------------------------------------------------------------------
        if args.command == "start":
            self.show_start()
        elif args.command == "help":
            self.show_help()
        elif args.command == "add":
            self.add_task(args.description)
        elif args.command == "update":
            self.update_task(args.id, args.description)
        elif args.command == "delete":
            self.delete_task(args.id)
        elif args.command == "mark-in-progress":
            self.mark_task(args.id, "in-progress")
        elif args.command == "mark-done":
            self.mark_task(args.id, "done")
        elif args.command == "list":
            self.list_tasks(args.status)
        else:
            parser.print_help()

    # ----------------------------------------------------------------------
    # Command Implementations
    # ----------------------------------------------------------------------
    def show_start(self):
        """Display a greeting and quickstart guide."""
        print("\n👋 Welcome to Task Manager CLI!")
        print("Easily track your tasks with statuses: todo, in-progress, and done.")
        print("\n👉 Quickstart:")
        print("   task-cli add \"Buy groceries\"")
        print("   task-cli list")
        print("\nFor full command reference, run:")
        print("   task-cli help\n")

    def show_help(self):
        """Show list of available commands with examples."""
        print("\n📖 Task Manager CLI - Commands Reference\n")
        print("General:")
        print("  start                   Show greeting and quickstart guide")
        print("  help                    Show this list of commands\n")
        print("Tasks:")
        print("  add \"description\"       Add a new task")
        print("  update ID \"description\" Update task description")
        print("  delete ID               Delete a task by ID\n")
        print("Status updates:")
        print("  mark-in-progress ID     Mark task as 'in-progress'")
        print("  mark-done ID            Mark task as 'done'\n")
        print("Listing:")
        print("  list                    Show all tasks")
        print("  list todo               Show only 'todo' tasks")
        print("  list in-progress        Show only 'in-progress' tasks")
        print("  list done               Show only 'done' tasks\n")
        print("💡 Example:")
        print("   task-cli add \"Read a book\"")
        print("   task-cli update 1 \"Read two books\"")
        print("   task-cli mark-done 1")
        print("   task-cli list done\n")

    def add_task(self, description):
        """Add a new task with a description."""
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
        """Update a task's description by its ID."""
        for task in self.tasks:
            if task["id"] == task_id:
                task["description"] = description
                task["updated_at"] = ""
                safe_print(f"✏️ Task {task_id} updated.")
                self.save_tasks()
                return
        safe_print(f"⚠️ No task found with ID={task_id}")

    def delete_task(self, task_id):
        """Delete a task by its ID."""
        before = len(self.tasks)
        self.tasks = [t for t in self.tasks if t["id"] != task_id]
        if len(self.tasks) < before:
            safe_print(f"🗑️ Task {task_id} deleted.")
            self.save_tasks()
        else:
            safe_print(f"⚠️ No task found with ID={task_id}")

    def mark_task(self, task_id, status):
        """Mark a task as 'in-progress' or 'done'."""
        for task in self.tasks:
            if task["id"] == task_id:
                task["status"] = status
                task["updated_at"] = ""
                safe_print(f"✅ Task {task_id} marked as {status}.")
                self.save_tasks()
                return
        safe_print(f"⚠️ No task found with ID={task_id}")

    def list_tasks(self, status=None):
        """List all tasks, optionally filtering by status."""
        filtered = self.tasks if not status else [t for t in self.tasks if t["status"] == status]
        if not filtered:
            safe_print("📂 No tasks found.")
            return
        for task in filtered:
            print(f"[{task['id']}] {task['description']} - {task['status']}")


# ----------------------------------------------------------------------
# Entry Point
# ----------------------------------------------------------------------
if __name__ == "__main__":
    cli = TaskManager()
    cli.run()
