# Task Manager CLI 📝

A **Python CLI task manager** to efficiently track your tasks from the terminal.  
Supports **adding, updating, deleting, marking, and listing tasks** with **persistent JSON storage**.  

Designed with **cross-platform compatibility**, optional emoji support, and **fully tested** with `pytest`.  

You can run it either via **Python source** or as a **prebuilt Windows `.exe`**.

---

## Features

- Add tasks with descriptions  
- Update or delete tasks by ID  
- Mark tasks as **in-progress** or **done**  
- List tasks filtered by status (all, done, in-progress)  
- Emoji support for task statuses (can be disabled for Windows)  
- Persistent storage in JSON (`tasks.json`)  
- Fully tested using `pytest`  
- Interactive CLI prompt for multiple commands in one session

---

## Installation

### Option 1: Using Python (source)

1. Clone the repository:

```
git clone https://github.com/Arshiya-Bagheri/task-manager.git
cd task-manager
```

2. Create a virtual environment (recommended):

```
python -m venv venv
# Activate:
source venv/bin/activate   # Linux/macOS
venv\Scripts\activate      # Windows
```

3. Install dependencies:

```
pip install -r requirements.txt
```

### Option 2: Using prebuilt Windows `.exe`

1. Navigate to the `dist/` folder.  
2. Use `task-cli.exe` directly without installing Python.

---

## Usage

### Interactive CLI (`.exe` or Python source)

Run the CLI:

```
# From Python source
python -m task_manager.cli

# From Windows .exe
task-cli.exe
```

You will see an interactive prompt:

```
👋 Welcome to Task Manager CLI!
Type 'help' to see available commands, 'exit' to quit.

task-cli>
```

Now you can type commands directly, e.g.:

```
task-cli> add Buy groceries
task-cli> list
task-cli> mark-done 1
task-cli> exit
```

> Each command executes immediately, and the prompt remains until you type `exit`.

---

## Commands & Examples

| Command | Description | Example |
|---------|-------------|---------|
| `add <description>` | Add a new task | `add Buy groceries` |
| `update <id> <desc>` | Update a task by ID | `update 1 Buy milk and eggs` |
| `delete <id>` | Delete a task by ID | `delete 1` |
| `mark-in-progress <id>` | Mark task as in-progress | `mark-in-progress 1` |
| `mark-done <id>` | Mark task as done | `mark-done 1` |
| `list [status]` | List tasks (`todo`, `in-progress`, `done`) | `list done` |
| `help` | Show commands reference | `help` |
| `exit` | Exit the CLI | `exit` |

Example output:

```
[1] Buy groceries - in-progress
[2] Finish project - done
```

---

### Environment Variables

- **`USE_EMOJI=0`**  
  Disable emojis if your terminal cannot display them (common in Windows).

```
# Example
USE_EMOJI=0 python -m task_manager.cli add "Test task"
```

---

## Testing

The project uses **pytest** for automated testing:

```
pytest -v
```

- Tests cover all CLI commands: add, update, delete, mark, and list tasks.  
- Temporary JSON files are used for testing, so real data is safe.  
- Emoji output is disabled in tests using:

```
USE_EMOJI=0 pytest -v
```

---

## Project Structure

```
task-manager/
│
├─ task_manager/
│   └─ cli.py           # Main CLI application
│
├─ tests/
│   └─ test_cli.py      # Pytest test cases
│
├─ dist/                # Compiled Windows .exe
│   └─ task-cli.exe
│
├─ requirements.txt     # Python dependencies
└─ README.md
```

---

## Dependencies

- Python 3.13+  
- pytest >= 8.0.0  

> All dependencies are listed in `requirements.txt`.

---

## Contributing

Open for contributions!  

- Suggest features  
- Fix bugs  
- Improve CLI usability  

Fork the repo, make changes, and submit a pull request.

---

## About the Author

**Arshiya Bagheri** – Python developer & CLI enthusiast.  

Skills demonstrated in this project:

- Python CLI development  
- File handling (JSON persistence)  
- Unit testing with pytest  
- Cross-platform terminal considerations

---

## Optional Enhancements

For future improvements:

- Add **priority levels** for tasks  
- Integrate **search functionality**  
- Export tasks to **CSV or Excel**  
- Add **interactive CLI menus**  
- Maintain **separate documentation** in `documentation.md`
