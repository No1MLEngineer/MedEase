# planetary_scientist_assistant/data_manager/data_storage.py
import os
import pandas as pd # Assuming pandas is used for DataFrame operations

# This module is currently a placeholder for more advanced data storage.
# For now, it will focus on saving DataFrames to CSV files.
# Future enhancements could include SQLite integration or other local database solutions.

# Uses the same DATA_FILES_SUBDIR as data_loader for consistency
DATA_FILES_SUBDIR = "data_manager_files"

def get_data_files_dir(project_base_path):
    """Returns the path to the data files directory."""
    return os.path.join(project_base_path, DATA_FILES_SUBDIR)

def _ensure_data_files_dir_exists(project_base_path):
    """Ensures the data files directory exists."""
    data_dir = get_data_files_dir(project_base_path)
    os.makedirs(data_dir, exist_ok=True)
    return data_dir

def save_df_to_csv(dataframe, filename, project_base_path, overwrite=False):
    """
    Saves a pandas DataFrame to a CSV file in the project's data directory.

    Args:
        dataframe (pandas.DataFrame): The DataFrame to save.
        filename (str): The name for the CSV file (e.g., "processed_data.csv").
        project_base_path (str): The base path of the project.
        overwrite (bool): If True, overwrite the file if it already exists.
                          If False (default), do not overwrite and return an error.

    Returns:
        bool: True if successful, False otherwise.
        str: Message indicating success or failure.
    """
    if not isinstance(dataframe, pd.DataFrame):
        return False, "Error: Input is not a valid pandas DataFrame."

    if not filename.lower().endswith(".csv"):
        filename += ".csv" # Append .csv extension if not present

    data_dir = _ensure_data_files_dir_exists(project_base_path)
    destination_filepath = os.path.join(data_dir, filename)

    if os.path.exists(destination_filepath) and not overwrite:
        return False, f"Error: File '{filename}' already exists at '{destination_filepath}'. Set overwrite=True to replace it."

    try:
        dataframe.to_csv(destination_filepath, index=False) # index=False is common for data CSVs
        return True, f"DataFrame successfully saved to '{destination_filepath}'."
    except Exception as e:
        return False, f"Error saving DataFrame to CSV '{filename}': {e}"

def list_data_files(project_base_path, extension_filter=None):
    """
    Lists files in the project's data directory, optionally filtering by extension.

    Args:
        project_base_path (str): The base path of the project.
        extension_filter (str or list, optional): A file extension (e.g., ".csv")
                                                  or list of extensions to filter by.
                                                  Defaults to None (list all files).

    Returns:
        list: A list of filenames found in the data directory.
        str: Message, typically empty on success or an error message.
    """
    data_dir = get_data_files_dir(project_base_path) # No need to ensure_exists here, if it's not there, no files.
    if not os.path.isdir(data_dir):
        return [], f"Data directory '{data_dir}' not found."

    try:
        files = os.listdir(data_dir)

        if extension_filter:
            if isinstance(extension_filter, str):
                extension_filter = [extension_filter.lower()]
            elif isinstance(extension_filter, list):
                extension_filter = [ext.lower() for ext in extension_filter]
            else:
                return [], "Error: extension_filter must be a string or a list of strings."

            filtered_files = [
                f for f in files
                if os.path.isfile(os.path.join(data_dir, f)) and \
                   any(f.lower().endswith(ext) for ext in extension_filter)
            ]
            return filtered_files, f"Found {len(filtered_files)} file(s) matching filter."
        else:
            # List all items (files and directories) if no filter
            # Or, to list only files:
            all_files = [f for f in files if os.path.isfile(os.path.join(data_dir, f))]
            return all_files, f"Found {len(all_files)} file(s) in data directory."

    except Exception as e:
        return [], f"Error listing data files: {e}"


if __name__ == '__main__':
    print("--- Testing Data Storage ---")

    current_script_path = os.path.dirname(os.path.abspath(__file__))
    TEST_PROJECT_BASE = os.path.dirname(current_script_path)
    print(f"Using project base for testing: {os.path.abspath(TEST_PROJECT_BASE)}")
    os.makedirs(TEST_PROJECT_BASE, exist_ok=True)

    test_data_dir = _ensure_data_files_dir_exists(TEST_PROJECT_BASE)
    print(f"Test data will be saved in/listed from: {test_data_dir}")

    # Create a sample DataFrame
    sample_data = {'col1': [1, 2, 3], 'col2': ['a', 'b', 'c']}
    df_to_save = pd.DataFrame(sample_data)
    test_filename = "test_save.csv"
    test_filepath = os.path.join(test_data_dir, test_filename)

    print("\n1. Saving DataFrame to CSV:")
    success, msg = save_df_to_csv(df_to_save, test_filename, project_base_path=TEST_PROJECT_BASE)
    print(msg)
    assert success, "Failed to save DataFrame."
    assert os.path.exists(test_filepath), "CSV file was not created."

    print("\n2. Attempting to save again without overwrite (should fail):")
    success_no_overwrite, msg_no_overwrite = save_df_to_csv(df_to_save, test_filename, project_base_path=TEST_PROJECT_BASE, overwrite=False)
    print(msg_no_overwrite)
    assert not success_no_overwrite, "Should have failed to save without overwrite."

    print("\n3. Saving again with overwrite (should succeed):")
    df_modified = pd.DataFrame({'col1': [4,5,6], 'col2': ['d','e','f']})
    success_overwrite, msg_overwrite = save_df_to_csv(df_modified, test_filename, project_base_path=TEST_PROJECT_BASE, overwrite=True)
    print(msg_overwrite)
    assert success_overwrite, "Failed to save DataFrame with overwrite."
    # Verify content changed (optional, by loading and checking)
    df_loaded = pd.read_csv(test_filepath)
    assert df_loaded['col1'].iloc[0] == 4, "Content was not overwritten correctly."


    print("\n4. Listing data files (all):")
    # Create another dummy file to test listing
    dummy_other_file = os.path.join(test_data_dir, "other_file.txt")
    with open(dummy_other_file, "w") as f:
        f.write("dummy")

    all_files, list_msg_all = list_data_files(project_base_path=TEST_PROJECT_BASE)
    print(list_msg_all)
    print(f"  Files: {all_files}")
    assert test_filename in all_files
    assert "other_file.txt" in all_files

    print("\n5. Listing data files (CSV only):")
    csv_files, list_msg_csv = list_data_files(project_base_path=TEST_PROJECT_BASE, extension_filter=".csv")
    print(list_msg_csv)
    print(f"  CSV Files: {csv_files}")
    assert test_filename in csv_files
    assert "other_file.txt" not in csv_files
    assert len(csv_files) == 1


    # Clean up test files
    print("\nCleaning up test files...")
    if os.path.exists(test_filepath):
        os.remove(test_filepath)
    if os.path.exists(dummy_other_file):
        os.remove(dummy_other_file)

    print("\nData storage tests completed.")
