# task_manager/__init__.py

__app_name__ = "task-manager"
__version__ = "1.0.0"
__author__ = "Arshiya Bagheri"
__author_email__ = "arshiyabagheri7@gmail.com"
__description__ = "A simple command-line task manager to track tasks with statuses."
__license__ = "MIT"

# Exit codes
(
    SUCCESS,
    DIR_ERROR,
    FILE_ERROR,
    DB_READ_ERROR,
    DB_WRITE_ERROR,
    JSON_ERROR,
    ID_ERROR,
) = range(7)

ERRORS = {
    DIR_ERROR: "Configuration directory error",
    FILE_ERROR: "Configuration file error",
    DB_READ_ERROR: "Database read error",
    DB_WRITE_ERROR: "Database write error",
    JSON_ERROR: "Invalid JSON format",
    ID_ERROR: "Task ID not found",
}
