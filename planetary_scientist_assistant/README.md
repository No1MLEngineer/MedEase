# Planetary Scientist's Assistant (PSA)

Welcome to the Planetary Scientist's Assistant (PSA)! This AI agent is designed to support scientists in their research and data management tasks, with a strong focus on offline capabilities for potential use on Earth or other planets.

## Project Goal

To create a versatile, command-line-driven assistant that helps scientists with:
-   **Knowledge Management:** Storing, searching, and retrieving local documents (text, PDF) and personal notes.
-   **Scientific Utilities:** Performing common scientific unit conversions and evaluating mathematical expressions.
-   **Experiment Support:** Logging experimental procedures and observations.
-   **Data Management:** Basic loading and saving of CSV data files.

This project is developed in Python 3 and aims to be usable without reliance on paid APIs or constant internet connectivity, making it suitable for remote or resource-constrained environments. The code is structured to be compatible with platforms like Google Colab for ease of experimentation and use, although it runs as a standalone Python application.

## Project Structure

The project is organized as follows, assuming the main directory is `planetary_scientist_assistant/`:

```
planetary_scientist_assistant/
├── main.py                     # Main application CLI entry point
├── AGENTS.md                   # Guidelines for AI development on this project
├── README.md                   # This file
├── data_manager/               # Module for data loading and storage
│   ├── __init__.py
│   ├── data_loader.py
│   └── data_storage.py
├── data_manager_files/         # Directory for CSV data files (created automatically)
├── experiment_logs/            # Directory for daily log files (created automatically)
├── experiment_support/         # Module for experiment logging
│   ├── __init__.py
│   └── logbook.py
├── knowledge_base/             # Module for document and note management
│   ├── __init__.py
│   ├── document_manager.py
│   └── note_taker.py
├── local_documents/            # Directory for storing added documents (created automatically)
│   └── kb_metadata.json        # Metadata for documents in the knowledge base
├── local_notes/                # Directory for storing notes (created automatically)
│   ├── content/                # Individual note files (UUID.txt)
│   └── notes_metadata.json     # Metadata for notes
├── sci_utils/                  # Module for scientific utilities
│   ├── __init__.py
│   ├── calculator.py
│   └── unit_converter.py
└── tests/                      # Unit tests
    └── test_unit_converter.py
```

## Getting Started

### Prerequisites

-   Python 3 (developed with Python 3.10+, should be compatible with 3.8+)
-   `pip` for installing dependencies.

### Dependencies

The project uses the following main external Python libraries:

-   **pandas:** For CSV data handling in the `data_manager` module.
-   **PyPDF2:** (Optional) For searching text content within PDF documents in the `knowledge_base.document_manager`. If not installed, PDF search functionality will be gracefully skipped.

You can install these (pandas is essential for data management features, PyPDF2 is optional for PDF search) using pip:

```bash
pip install pandas PyPDF2
```
(Note: If you are running this agent, it will handle installations if necessary. If you are running the code manually, you'll need to do this.)

### Running the Application

1.  Navigate to the `planetary_scientist_assistant` directory in your terminal.
2.  Run the main application script:

    ```bash
    python main.py
    ```

3.  This will start the Command-Line Interface (CLI), presenting you with a main menu to access different functionalities.

### Running Unit Tests

Unit tests are provided for some modules (currently `sci_utils.unit_converter`). To run the tests:

1.  Navigate to the `planetary_scientist_assistant` directory (the one containing `tests/` and the module directories).
2.  Use Python's `unittest` discovery mechanism:

    ```bash
    python -m unittest discover -s tests -v
    ```
    (Or, more generally from the parent of `planetary_scientist_assistant`):
    ```bash
    python -m unittest discover -s planetary_scientist_assistant/tests -v
    ```

This will discover and run all tests within the `tests` directory.

## Modules and Functionalities

### 1. Knowledge Base Management (`knowledge_base/`)

-   **Document Manager (`document_manager.py`):**
    -   Add external document files (e.g., `.txt`, `.pdf`) to a local knowledge base (`local_documents/`).
    -   List all managed documents.
    -   Search documents by keyword in their content (text and PDF supported, PDF requires PyPDF2).
    -   View metadata details of a specific document.
    -   Remove documents from the knowledge base.
    -   Metadata is stored in `local_documents/kb_metadata.json`.
-   **Note Taker (`note_taker.py`):**
    -   Create, view, and delete personal text notes.
    -   Notes are stored with unique IDs, with content in `local_notes/content/` and metadata in `local_notes/notes_metadata.json`.
    -   Search notes by keyword in their title or content.

### 2. Scientific Utilities (`sci_utils/`)

-   **Unit Converter (`unit_converter.py`):**
    -   Convert values between various scientific units.
    -   Supported categories: `length`, `mass`, `temperature`, `time`, `pressure`.
    -   Provides lists of supported units for each category.
-   **Calculator (`calculator.py`):**
    -   Safely evaluate mathematical expressions from strings.
    -   Supports common mathematical functions (sin, cos, log, sqrt, etc.) and constants (pi, e).

### 3. Experiment Logbook (`experiment_support/`)

-   **Logbook (`logbook.py`):**
    -   Add timestamped log entries to daily log files (e.g., `experiment_logs/log_YYYYMMDD.txt`).
    -   Entries can include an optional experiment ID and log level (INFO, WARNING, ERROR, DEBUG).
    -   View content of specific log files by filename or date.
    -   List all available log files.

### 4. Data Management (`data_manager/`)

-   **Data Loader (`data_loader.py`):**
    -   Load data from CSV files (expected in `data_manager_files/`) into pandas DataFrames.
    -   Display summary statistics for loaded DataFrames (shape, head, info, describe, missing values).
-   **Data Storage (`data_storage.py`):**
    -   Save pandas DataFrames to CSV files in `data_manager_files/`.
    -   Option to overwrite existing files.
    -   List data files in the storage directory, with optional extension filtering.

## Using with Google Colab / Jupyter

While PSA is a standalone Python application, its modules are designed to be importable and usable in environments like Google Colab or Jupyter notebooks, especially for data analysis tasks.

-   You would typically upload your data files (CSVs, documents) to your Colab environment or mount your Google Drive.
-   You can then copy relevant code snippets from the PSA modules or `main.py` into Colab cells.
-   Adjust file paths in the code to point to your data in the Colab environment.
-   Ensure necessary libraries (`pandas`, `PyPDF2`) are installed in your Colab notebook (e.g., using `!pip install pandas PyPDF2`).

For example, to use the `data_loader` in Colab:
```python
# In a Colab cell, after uploading 'my_data.csv' and the 'data_loader.py' (or its content)
# Assuming data_loader.py content is available or PSA modules are in sys.path

# If data_loader.py is in the same directory in Colab:
# from data_loader import load_csv, display_summary_statistics

# Or, if you've copied the functions:
# (define load_csv and display_summary_statistics functions here)

# Example usage:
# PROJECT_BASE_COLAB = "/content/" # Colab's base content directory
# Make sure your data_manager_files/my_data.csv exists relative to this.
# Or provide absolute path to load_csv.

# df, msg = load_csv("/content/my_data.csv") # Using absolute path in Colab
# if df is not None:
#     print(msg)
#     summary = display_summary_statistics(df, "My Uploaded Data")
#     print(summary)
# else:
#     print(msg)
```

## Future Enhancements (Ideas)

-   More sophisticated search for knowledge base (e.g., semantic search if feasible offline).
-   Support for more document types.
-   SQLite database integration for more robust data and metadata storage.
-   Expansion of scientific utilities (e.g., more conversions, statistical functions).
-   Basic plotting capabilities for data analysis.
-   More structured experiment protocol management.
-   A more interactive UI (e.g., using `curses` or a simple web interface if offline deployment allows).
```
