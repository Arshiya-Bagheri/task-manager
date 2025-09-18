"""
Tests for task_tracker CLI.

⚠️ NOTE FOR WINDOWS USERS / EMOJI ISSUES:
- Some CLI outputs contain emojis which can cause Unicode errors on Windows consoles.
- To run tests safely, disable emojis by setting the environment variable USE_EMOJI=0.
  
Example:

    # On Linux / macOS / git bash
    USE_EMOJI=0 pytest -v

    # On Windows (PowerShell)
    $env:USE_EMOJI="0"
    pytest -v

- This ensures all test assertions work correctly.
"""

import os
import json
import subprocess
import sys
from pathlib import Path
import pytest

SCRIPT = Path(__file__).resolve().parent.parent / "task_manager" / "cli.py"
PYTHON = sys.executable  # use current Python interpreter


def run_cli(args, cwd=None):
    return subprocess.run(
        [sys.executable, str(SCRIPT)] + args,
        cwd=cwd,
        text=True,
        capture_output=True
    )

@pytest.fixture
def temp_tasks(tmp_path, monkeypatch):
    # force CLI to use a temporary tasks.json
    test_file = tmp_path / "tasks.json"
    monkeypatch.chdir(tmp_path)
    return test_file

def test_add_task(temp_tasks):
    result = run_cli(["add", "Buy groceries"], cwd=temp_tasks.parent)
    assert "Task added successfully" in result.stdout

    with open(temp_tasks, "r", encoding="utf-8") as f:
        tasks = json.load(f)

    assert len(tasks) == 1
    assert tasks[0]["description"] == "Buy groceries"
    assert tasks[0]["status"] == "todo"


def test_update_task(temp_tasks):
    run_cli(["add", "Old task"], cwd=temp_tasks.parent)
    result = run_cli(["update", "1", "New task"], cwd=temp_tasks.parent)

    assert "updated" in result.stdout

    with open(temp_tasks, "r", encoding="utf-8") as f:
        tasks = json.load(f)

    assert tasks[0]["description"] == "New task"


def test_delete_task(temp_tasks):
    run_cli(["add", "Task to delete"], cwd=temp_tasks.parent)
    result = run_cli(["delete", "1"], cwd=temp_tasks.parent)

    assert "deleted" in result.stdout

    with open(temp_tasks, "r", encoding="utf-8") as f:
        tasks = json.load(f)

    assert len(tasks) == 0


def test_mark_in_progress(temp_tasks):
    run_cli(["add", "Task in progress"], cwd=temp_tasks.parent)
    result = run_cli(["mark-in-progress", "1"], cwd=temp_tasks.parent)

    assert "in-progress" in result.stdout

    with open(temp_tasks, "r", encoding="utf-8") as f:
        tasks = json.load(f)

    assert tasks[0]["status"] == "in-progress"


def test_mark_done(temp_tasks):
    run_cli(["add", "Task done"], cwd=temp_tasks.parent)
    result = run_cli(["mark-done", "1"], cwd=temp_tasks.parent)

    assert "done" in result.stdout

    with open(temp_tasks, "r", encoding="utf-8") as f:
        tasks = json.load(f)

    assert tasks[0]["status"] == "done"


def test_list_tasks(temp_tasks):
    run_cli(["add", "Task A"], cwd=temp_tasks.parent)
    run_cli(["add", "Task B"], cwd=temp_tasks.parent)
    run_cli(["mark-done", "2"], cwd=temp_tasks.parent)

    # List all
    result_all = run_cli(["list"], cwd=temp_tasks.parent)
    assert "Task A" in result_all.stdout
    assert "Task B" in result_all.stdout

    # List done
    result_done = run_cli(["list", "done"], cwd=temp_tasks.parent)
    assert "Task B" in result_done.stdout
    assert "Task A" not in result_done.stdout

    # List todo
    result_todo = run_cli(["list", "todo"], cwd=temp_tasks.parent)
    assert "Task A" in result_todo.stdout
    assert "Task B" not in result_todo.stdout
