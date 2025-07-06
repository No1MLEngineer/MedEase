# planetary_scientist_assistant/data_manager/data_loader.py
import os
import pandas as pd # Assuming pandas will be available. Installation: pip install pandas

# Define a directory for sample data or user-uploaded data, relative to project base
DATA_FILES_SUBDIR = "data_manager_files"

def get_data_files_dir(project_base_path):
    """Returns the path to the data files directory."""
    return os.path.join(project_base_path, DATA_FILES_SUBDIR)

def _ensure_data_files_dir_exists(project_base_path):
    """Ensures the data files directory exists."""
    data_dir = get_data_files_dir(project_base_path)
    os.makedirs(data_dir, exist_ok=True)
    return data_dir

def load_csv(file_path, project_base_path=None):
    """
    Loads data from a CSV file into a pandas DataFrame.
    The file_path can be absolute or relative to the project_base_path/DATA_FILES_SUBDIR if project_base_path is provided.

    Args:
        file_path (str): The name of the CSV file (if in default data dir) or full path to the CSV file.
        project_base_path (str, optional): The base path of the project. If provided,
                                           and file_path is just a filename, it will look
                                           in project_base_path/DATA_FILES_SUBDIR.

    Returns:
        pandas.DataFrame or None: DataFrame if successful, None otherwise.
        str: Message indicating success or failure.
    """
    actual_file_path = file_path
    if project_base_path and not os.path.isabs(file_path):
        # If a base path is given and file_path is relative, construct path to data dir
        data_dir = _ensure_data_files_dir_exists(project_base_path)
        actual_file_path = os.path.join(data_dir, file_path)
    elif not os.path.isabs(file_path):
        # If no base path and relative path, assume it's relative to current working directory
        actual_file_path = os.path.abspath(file_path)


    if not os.path.exists(actual_file_path):
        return None, f"Error: File not found at '{actual_file_path}'."
    if not actual_file_path.lower().endswith(".csv"):
        return None, f"Error: File '{os.path.basename(actual_file_path)}' is not a CSV file based on extension."

    try:
        df = pd.read_csv(actual_file_path)
        return df, f"CSV file '{os.path.basename(actual_file_path)}' loaded successfully. Shape: {df.shape}"
    except pd.errors.EmptyDataError:
        return None, f"Error: CSV file '{os.path.basename(actual_file_path)}' is empty."
    except Exception as e:
        return None, f"Error loading CSV file '{os.path.basename(actual_file_path)}': {e}"

def display_summary_statistics(dataframe, df_name="DataFrame"):
    """
    Prints summary statistics of a pandas DataFrame.

    Args:
        dataframe (pandas.DataFrame): The DataFrame to summarize.
        df_name (str): A name for the DataFrame for display purposes.

    Returns:
        str: A string containing the summary statistics, or an error message.
    """
    if not isinstance(dataframe, pd.DataFrame):
        return "Error: Input is not a valid pandas DataFrame."

    if dataframe.empty:
        return f"The {df_name} is empty."

    summary = f"\n--- Summary Statistics for {df_name} ---\n"
    summary += f"Shape: {dataframe.shape}\n"

    summary += "\nFirst 5 rows (head):\n"
    summary += dataframe.head().to_string() + "\n"

    summary += "\nBasic Info:\n"
    # Capture df.info() output which prints to stdout
    from io import StringIO
    buffer = StringIO()
    dataframe.info(buf=buffer)
    summary += buffer.getvalue() + "\n"

    summary += "\nDescriptive Statistics (for numerical columns):\n"
    # Check if there are any numerical columns before calling describe
    numerical_cols = dataframe.select_dtypes(include=['number'])
    if not numerical_cols.empty:
        summary += numerical_cols.describe().to_string() + "\n"
    else:
        summary += "No numerical columns to describe.\n"

    summary += "\nMissing Values (per column):\n"
    missing_values = dataframe.isnull().sum()
    missing_values = missing_values[missing_values > 0] # Show only columns with missing values
    if not missing_values.empty:
        summary += missing_values.to_string() + "\n"
    else:
        summary += "No missing values found.\n"

    return summary

if __name__ == '__main__':
    print("--- Testing Data Loader ---")

    # Determine TEST_PROJECT_BASE relative to this script
    current_script_path = os.path.dirname(os.path.abspath(__file__))
    TEST_PROJECT_BASE = os.path.dirname(current_script_path) # Should be 'planetary_scientist_assistant'
    print(f"Using project base for testing: {os.path.abspath(TEST_PROJECT_BASE)}")
    os.makedirs(TEST_PROJECT_BASE, exist_ok=True)

    # Ensure the data directory for tests exists
    test_data_dir = _ensure_data_files_dir_exists(TEST_PROJECT_BASE)
    print(f"Test data will be looked for/created in: {test_data_dir}")

    # Create a sample CSV file for testing
    sample_csv_filename = "sample_data.csv"
    sample_csv_filepath = os.path.join(test_data_dir, sample_csv_filename)

    sample_df_content = {
        'ID': [1, 2, 3, 4, 5],
        'Timestamp': ['2023-01-01T10:00:00Z', '2023-01-01T10:05:00Z', '2023-01-01T10:10:00Z', '2023-01-01T10:15:00Z', '2023-01-01T10:20:00Z'],
        'Temperature_C': [25.5, 26.0, 25.8, None, 26.1], # Added a None for missing value test
        'Pressure_kPa': [101.2, 101.1, 101.2, 101.0, 100.9],
        'Observation': ['Clear sky', 'Slight breeze', 'Clouds forming', 'Gusty wind', 'Stable']
    }
    pd.DataFrame(sample_df_content).to_csv(sample_csv_filepath, index=False)
    print(f"Created sample CSV: {sample_csv_filepath}")

    print("\n1. Loading the sample CSV file:")
    # Test loading by filename (expecting it in the data_manager_files subdir)
    df, msg = load_csv(sample_csv_filename, project_base_path=TEST_PROJECT_BASE)
    print(msg)
    assert df is not None, "Failed to load sample CSV by filename."
    if df is not None:
        print(f"  DataFrame shape: {df.shape}")

    print("\n2. Displaying summary statistics:")
    if df is not None:
        stats_summary = display_summary_statistics(df, "Sample CSV Data")
        print(stats_summary)
        assert "Shape: (5, 5)" in stats_summary
        assert "Temperature_C    1" in stats_summary # Test missing value count

    print("\n3. Testing loading a non-existent file:")
    non_existent_df, non_existent_msg = load_csv("non_existent.csv", project_base_path=TEST_PROJECT_BASE)
    print(non_existent_msg)
    assert non_existent_df is None

    print("\n4. Testing loading a non-CSV file (by extension):")
    # Create a dummy non-csv file
    dummy_txt_filename = "dummy.txt"
    dummy_txt_filepath = os.path.join(test_data_dir, dummy_txt_filename)
    with open(dummy_txt_filepath, "w") as f:
        f.write("This is not a CSV.")

    non_csv_df, non_csv_msg = load_csv(dummy_txt_filename, project_base_path=TEST_PROJECT_BASE)
    print(non_csv_msg)
    assert non_csv_df is None

    print("\n5. Testing loading an empty CSV file:")
    empty_csv_filename = "empty.csv"
    empty_csv_filepath = os.path.join(test_data_dir, empty_csv_filename)
    with open(empty_csv_filepath, "w") as f:
        pass # Create an empty file
    empty_df, empty_msg = load_csv(empty_csv_filename, project_base_path=TEST_PROJECT_BASE)
    print(empty_msg) # Should indicate EmptyDataError or similar
    assert empty_df is None

    # Clean up test files
    print("\nCleaning up test files...")
    os.remove(sample_csv_filepath)
    os.remove(dummy_txt_filepath)
    os.remove(empty_csv_filepath)
    # Optionally remove the test_data_dir if it was created solely for this test and is empty
    # For now, leave it, as it's a defined subdir for the module.

    print("\nData loader tests completed.")
