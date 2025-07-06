# planetary_scientist_assistant/experiment_support/logbook.py
import os
from datetime import datetime

# Define a directory for experiment logs, relative to project base
LOG_FILES_SUBDIR = "experiment_logs"

def get_log_files_dir(project_base_path):
    """Returns the path to the log files directory."""
    return os.path.join(project_base_path, LOG_FILES_SUBDIR)

def _ensure_log_files_dir_exists(project_base_path):
    """Ensures the log files directory exists."""
    log_dir = get_log_files_dir(project_base_path)
    os.makedirs(log_dir, exist_ok=True)
    return log_dir

def get_daily_log_filename():
    """Generates a filename for the current day's log."""
    return f"log_{datetime.now().strftime('%Y%m%d')}.txt"

def add_log_entry(entry_text, project_base_path, experiment_id=None, level="INFO"):
    """
    Adds a new entry to the daily log file.
    Each entry is timestamped.

    Args:
        entry_text (str): The text of the log entry.
        project_base_path (str): The base path of the project.
        experiment_id (str, optional): An optional identifier for the experiment
                                       this log entry pertains to.
        level (str, optional): Log level (e.g., INFO, WARNING, ERROR, DEBUG). Defaults to "INFO".

    Returns:
        bool: True if successful, False otherwise.
        str: Message indicating success or failure.
    """
    if not entry_text or not isinstance(entry_text, str):
        return False, "Error: Log entry text cannot be empty and must be a string."

    log_dir = _ensure_log_files_dir_exists(project_base_path)
    log_filename = get_daily_log_filename()
    log_filepath = os.path.join(log_dir, log_filename)

    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3] # Millisecond precision

    formatted_entry = f"[{timestamp}] [{level.upper()}]"
    if experiment_id:
        formatted_entry += f" [ExpID: {experiment_id}]"
    formatted_entry += f": {entry_text.strip()}\n" # Ensure newline

    try:
        with open(log_filepath, 'a', encoding='utf-8') as f: # Append mode
            f.write(formatted_entry)
        return True, f"Log entry added to '{log_filename}'."
    except Exception as e:
        return False, f"Error adding log entry: {e}"

def view_log_file(log_filename_or_date, project_base_path):
    """
    Retrieves the content of a specific log file.
    The identifier can be the full filename (e.g., "log_20231027.txt")
    or a date string "YYYYMMDD" or "YYYY-MM-DD".

    Args:
        log_filename_or_date (str): The filename or date string for the log.
        project_base_path (str): The base path of the project.

    Returns:
        str or None: The content of the log file if found, else None.
        str: Message indicating success or status.
    """
    log_dir = get_log_files_dir(project_base_path) # Does not ensure_exists, as we are reading
    if not os.path.isdir(log_dir):
        return None, f"Log directory '{log_dir}' does not exist."

    log_filename = ""
    if log_filename_or_date.startswith("log_") and log_filename_or_date.endswith(".txt"):
        log_filename = log_filename_or_date
    else:
        try:
            # Attempt to parse as YYYY-MM-DD or YYYYMMDD
            date_str = log_filename_or_date.replace("-", "")
            datetime.strptime(date_str, "%Y%m%d") # Validate date format
            log_filename = f"log_{date_str}.txt"
        except ValueError:
            return None, "Error: Invalid date format. Use 'YYYYMMDD', 'YYYY-MM-DD', or full filename."

    log_filepath = os.path.join(log_dir, log_filename)

    if not os.path.exists(log_filepath):
        return None, f"Log file '{log_filename}' not found at '{log_filepath}'."

    try:
        with open(log_filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        return content, f"Content of '{log_filename}' retrieved."
    except Exception as e:
        return None, f"Error reading log file '{log_filename}': {e}"

def list_log_files(project_base_path):
    """
    Lists all available log files in the log directory.

    Args:
        project_base_path (str): The base path of the project.

    Returns:
        list: A list of log filenames found.
        str: Message, typically empty on success or an error message.
    """
    log_dir = get_log_files_dir(project_base_path)
    if not os.path.isdir(log_dir):
        return [], f"Log directory '{log_dir}' not found."

    try:
        files = os.listdir(log_dir)
        log_files = sorted([
            f for f in files
            if os.path.isfile(os.path.join(log_dir, f)) and \
               f.startswith("log_") and f.endswith(".txt")
        ], reverse=True) # Most recent first
        return log_files, f"Found {len(log_files)} log file(s)."
    except Exception as e:
        return [], f"Error listing log files: {e}"


if __name__ == '__main__':
    print("--- Testing Logbook ---")

    current_script_path = os.path.dirname(os.path.abspath(__file__))
    TEST_PROJECT_BASE = os.path.dirname(current_script_path)
    print(f"Using project base for testing: {os.path.abspath(TEST_PROJECT_BASE)}")
    os.makedirs(TEST_PROJECT_BASE, exist_ok=True)

    log_dir_for_test = _ensure_log_files_dir_exists(TEST_PROJECT_BASE)
    print(f"Test logs will be stored in: {log_dir_for_test}")

    today_log_filename = get_daily_log_filename()
    today_log_filepath = os.path.join(log_dir_for_test, today_log_filename)

    # Clean up today's log file if it exists from a previous test run to start fresh
    if os.path.exists(today_log_filepath):
        os.remove(today_log_filepath)
        print(f"Removed existing test log file: {today_log_filepath}")

    print("\n1. Adding log entries:")
    success, msg = add_log_entry("Test log entry 1: System initialized.", TEST_PROJECT_BASE, experiment_id="EXP001", level="INFO")
    print(msg)
    assert success

    success, msg = add_log_entry("Test log entry 2: Sensor reading out of range.", TEST_PROJECT_BASE, experiment_id="EXP001", level="WARNING")
    print(msg)
    assert success

    success, msg = add_log_entry("Test log entry 3: Critical failure in component X.", TEST_PROJECT_BASE, level="ERROR")
    print(msg)
    assert success

    success, msg = add_log_entry("", TEST_PROJECT_BASE) # Empty entry
    print(f"Attempting to add empty entry: {msg}")
    assert not success


    print("\n2. Viewing today's log file:")
    content, msg = view_log_file(today_log_filename, TEST_PROJECT_BASE)
    print(msg)
    assert content is not None, "Failed to retrieve today's log content."
    if content:
        print("--- Log Content ---")
        print(content.strip()) # Strip trailing newline for cleaner print
        print("--- End Log Content ---")
        assert "System initialized." in content
        assert "[INFO]" in content
        assert "[WARNING]" in content
        assert "[ERROR]" in content
        assert "[ExpID: EXP001]" in content

    print("\n3. Viewing log file by date string (YYYYMMDD):")
    date_str_yyyymmdd = datetime.now().strftime('%Y%m%d')
    content_date, msg_date = view_log_file(date_str_yyyymmdd, TEST_PROJECT_BASE)
    print(msg_date)
    assert content_date is not None, "Failed to retrieve log by YYYYMMDD."
    assert content_date == content # Should be same content

    print("\n4. Viewing log file by date string (YYYY-MM-DD):")
    date_str_yyyy_mm_dd = datetime.now().strftime('%Y-%m-%d')
    content_date2, msg_date2 = view_log_file(date_str_yyyy_mm_dd, TEST_PROJECT_BASE)
    print(msg_date2)
    assert content_date2 is not None, "Failed to retrieve log by YYYY-MM-DD."
    assert content_date2 == content

    print("\n5. Listing log files:")
    log_files, list_msg = list_log_files(TEST_PROJECT_BASE)
    print(list_msg)
    print(f"  Files: {log_files}")
    assert today_log_filename in log_files

    print("\n6. Testing view non-existent log:")
    non_existent_content, non_existent_msg = view_log_file("log_19990101.txt", TEST_PROJECT_BASE)
    print(non_existent_msg)
    assert non_existent_content is None

    # Clean up the created log file for the test
    # print(f"\nCleaning up test log file: {today_log_filepath}")
    # if os.path.exists(today_log_filepath):
    #     os.remove(today_log_filepath)
    # Commented out so the log file remains for inspection after test.

    print("\nLogbook tests completed.")
