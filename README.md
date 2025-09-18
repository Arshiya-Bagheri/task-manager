# Task Manager CLI 📝

A **Python CLI task manager** to efficiently track your tasks from the terminal.  
Supports **adding, updating, deleting, marking, and listing tasks** with **persistent JSON storage**.  

Designed with **cross-platform compatibility**, optional emoji support, and **fully tested** with `pytest`.  

---

## Features

- Add tasks with descriptions  
- Update or delete tasks by ID  
- Mark tasks as **in-progress** or **done**  
- List tasks filtered by status (all, done, in-progress)  
- Emoji support for task statuses (can be disabled for Windows)  
- Persistent storage in JSON (`tasks.json`)  
- Fully tested using `pytest`  

---

## Installation

1. Clone the repository:

```
git clone https://github.com/Arshiya-Bagheri/task-manager.git
cd task-tracker
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

---

## Usage

Run the CLI using:

```
python -m task_manager.cli <command> [arguments]
```

> Replace `<command>` with one of the available commands listed below.

---

## Commands & Examples

### 1. Add a task

Adds a new task with a description.

```
python -m task_manager.cli add "Buy groceries"
```

Output example:

```
✅ Task added successfully (ID: 1)
```

### 2. Update a task

Updates an existing task by its ID.

```
python -m task_manager.cli update 1 "Buy groceries and fruits"
```

Output example:

```
✏️ Task 1 updated.
```

### 3. Delete a task

Deletes a task by ID.

```
python -m task_manager.cli delete 1
```

Output example:

```
🗑️ Task 1 deleted.
```

### 4. Mark task as in-progress

```
python -m task_manager.cli mark-in-progress 1
```

Output example:

```
✅ Task 1 marked as in-progress.
```

### 5. Mark task as done

```
python -m task_manager.cli mark-done 1
```

Output example:

```
✅ Task 1 marked as done.
```

### 6. List tasks

List tasks with optional status filter (`all`, `done`, `in-progress`).

```
# List all tasks
python -m task_manager.cli list

# List only completed tasks
python -m task_manager.cli list done

# List only in-progress tasks
python -m task_manager.cli list in-progress
```

Example output:

```
1. Buy groceries - in-progress
2. Finish project - done
```

---

### Environment Variables

- **`USE_EMOJI=0`**  
  Disables emojis if your terminal cannot display them (common in Windows).  

```
USE_EMOJI=0 python -m task_manager.cli add "Test task"
```

---

## Testing

The project uses **pytest** for automated testing:

```
pytest -v
```

- Tests cover all CLI commands: add, update, delete, mark, and list tasks.  
- Temporary JSON files are used for testing so your real data is safe.  
- Emoji output is disabled in tests by setting:

```
USE_EMOJI=0 pytest -v
```

---

## Project Structure

```
task_tracker/
│
├─ task_manager/
│   └─ cli.py           # Main CLI application
│
├─ tests/
│   └─ test_cli.py      # Pytest test cases
│
├─ requirements.txt     # Python dependencies
└─ README.md
```

---

## Dependencies

- Python 3.13+  
- pytest >= 8.0.0  

> All dependencies are listed in `requirements.txt` for easy installation.

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

For future improvements, you can:

- Add **priority levels** for tasks  
- Integrate **search functionality**  
- Export tasks to **CSV or Excel**  
- Add **interactive CLI menus**  
- Maintain **separate documentation** in `documentation.md`
