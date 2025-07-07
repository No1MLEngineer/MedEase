# planetary_scientist_assistant/main.py
import sys
import os

# Determine the directory where this script (main.py) is located.
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# Add SCRIPT_DIR to sys.path to allow imports of modules from subdirectories
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

# Lazy imports within functions to ensure sys.path is updated and avoid top-level import errors if modules are not found immediately.
# from knowledge_base import document_manager, note_taker
# from sci_utils import unit_converter, calculator
# from experiment_support import logbook

def display_welcome_message():
    """Displays a welcome message to the user."""
    print("***********************************************")
    print("* Welcome to the Planetary Scientist's Assistant (PSA)! *")
    print("***********************************************")
    print(f"\nPSA System running from: {SCRIPT_DIR}\n")

def display_main_menu(agent):
    print("\n--- Planetary Scientist's Assistant Main Menu ---")
    print("1. Knowledge Base")
    print("2. Scientific Utilities")
    print("3. Experiment Logbook")
    print("4. Data Management")
    print("5. Exit")
    print("\n[Autonomous Agent Suggestion]:", agent.suggest_next_action())
    choice = input("Enter your choice: ")
    return choice

# --- Knowledge Base Menu Handler ---
def handle_knowledge_base_menu():
    from knowledge_base import document_manager
    from knowledge_base import note_taker

    while True:
        print("\n--- Knowledge Base Menu ---")
        print("--- Documents ---")
        print("D1. Add Document")
        print("D2. List Documents")
        print("D3. Search Documents (Keyword)")
        print("D4. View Document Details")
        print("D5. Remove Document")
        print("--- Notes ---")
        print("N1. Add Note")
        print("N2. List Notes")
        print("N3. Search Notes (Keyword)")
        print("N4. View Note Content")
        print("N5. Delete Note")
        print("0. Back to Main Menu")
        choice = input("KB Menu Choice: ").upper()

        if choice == 'D1':
            file_path = input("Enter full path of the document to add: ")
            if not os.path.isabs(file_path): # Ensure absolute path for clarity
                 file_path = os.path.abspath(file_path)
            success, msg = document_manager.add_document(file_path, project_base_path=SCRIPT_DIR)
            print(msg)
        elif choice == 'D2':
            docs = document_manager.list_documents(project_base_path=SCRIPT_DIR)
            if not docs: print("No documents in knowledge base.")
            else:
                print("\nAvailable Documents:")
                for i, doc in enumerate(docs): print(f"  {i+1}. ID: {doc.get('id_in_kb')}, Type: {doc.get('file_type')}, Imported: {doc.get('import_date')}")
        elif choice == 'D3':
            keyword = input("Enter keyword to search in documents: ")
            found = document_manager.search_documents_by_keyword(keyword, project_base_path=SCRIPT_DIR)
            if not found: print(f"No documents found with keyword '{keyword}'.")
            else:
                print(f"\nDocuments containing '{keyword}':")
                for i, doc in enumerate(found): print(f"  {i+1}. ID: {doc.get('id_in_kb')}, Type: {doc.get('file_type')}")
        elif choice == 'D4':
            doc_id = input("Enter Document ID (filename) for details: ")
            details = document_manager.get_document_details(doc_id, project_base_path=SCRIPT_DIR)
            if not details: print(f"Document '{doc_id}' not found.")
            else:
                print("\nDocument Details:")
                for k, v in details.items(): print(f"  {k.replace('_', ' ').capitalize()}: {v}")
        elif choice == 'D5':
            doc_id = input("Enter Document ID (filename) to remove: ")
            if input(f"Sure you want to remove '{doc_id}'? (yes/no): ").lower() == 'yes':
                success, msg = document_manager.remove_document(doc_id, project_base_path=SCRIPT_DIR)
                print(msg)
            else: print("Removal cancelled.")
        elif choice == 'N1':
            title = input("Note title: ")
            print("Note content (type '--ENDNOTE--' on a new line to finish):")
            content_lines = []
            while True:
                line = input()
                if line == "--ENDNOTE--": break
                content_lines.append(line)
            content = "\n".join(content_lines)
            success, msg = note_taker.add_note(title, content, project_base_path=SCRIPT_DIR)
            print(msg)
        elif choice == 'N2':
            notes = note_taker.list_notes(project_base_path=SCRIPT_DIR)
            if not notes: print("No notes found.")
            else:
                print("\nAvailable Notes:")
                for i, note in enumerate(notes): print(f"  {i+1}. ID: {note.get('id')}, Title: {note.get('title')}, Created: {note.get('created_date')}")
        elif choice == 'N3':
            keyword = input("Enter keyword to search in notes: ")
            found = note_taker.search_notes(keyword, project_base_path=SCRIPT_DIR)
            if not found: print(f"No notes found with keyword '{keyword}'.")
            else:
                print(f"\nNotes containing '{keyword}':")
                for i, note in enumerate(found): print(f"  {i+1}. ID: {note.get('id')}, Title: {note.get('title')}")
        elif choice == 'N4':
            note_id = input("Enter Note ID to view: ")
            details = note_taker.get_note_details(note_id, project_base_path=SCRIPT_DIR)
            content = note_taker.get_note_content(note_id, project_base_path=SCRIPT_DIR)
            if not details: print(f"Note '{note_id}' not found.")
            else:
                print(f"\n--- Note: {details.get('title', 'N/A')} (ID: {note_id}) ---")
                print(content if content is not None else "Error: Content not found or empty.")
                print("--- End of Note ---")
        elif choice == 'N5':
            note_id = input("Enter Note ID to delete: ")
            if input(f"Sure you want to delete note '{note_id}'? (yes/no): ").lower() == 'yes':
                success, msg = note_taker.delete_note(note_id, project_base_path=SCRIPT_DIR)
                print(msg)
            else: print("Deletion cancelled.")
        elif choice == '0': break
        else: print("Invalid KB menu choice.")
        if choice != '0': input("\nPress Enter to return to KB Menu...")

# --- Scientific Utilities Menu Handler ---
def handle_sci_utils_menu():
    from sci_utils import unit_converter, calculator

    while True:
        print("\n--- Scientific Utilities Menu ---")
        print("U1. Convert Units")
        print("U2. Calculate Expression")
        print("0. Back to Main Menu")
        choice = input("SciUtils Menu Choice: ").upper()

        if choice == 'U1':
            print("\nUnit Converter")
            print(f"Supported categories: {unit_converter.get_supported_categories()}")
            category = input("Enter category (e.g., length, mass, temperature): ").lower()
            if category not in unit_converter.get_supported_categories():
                print("Invalid category.")
                continue
            print(f"Supported units in '{category}': {unit_converter.get_supported_units(category)}")
            try:
                value = float(input("Enter value to convert: "))
                from_unit = input(f"Convert from unit ({category}): ").lower()
                to_unit = input(f"Convert to unit ({category}): ").lower()
                result, msg = unit_converter.convert_unit(value, from_unit, to_unit, category)
                print(msg)
            except ValueError:
                print("Invalid numerical input for value.")
            except Exception as e:
                print(f"An error occurred: {e}")
        elif choice == 'U2':
            expression = input("Enter mathematical expression: ")
            result, msg = calculator.safe_eval(expression)
            print(f"Result: {result if result is not None else 'Error'}")
            print(f"Message: {msg}")
        elif choice == '0': break
        else: print("Invalid SciUtils menu choice.")
        if choice != '0': input("\nPress Enter to return to SciUtils Menu...")

# --- Experiment Logbook Menu Handler ---
def handle_experiment_logbook_menu():
    from experiment_support import logbook

    while True:
        print("\n--- Experiment Logbook Menu ---")
        print("L1. Add Log Entry")
        print("L2. View Log File (by date or filename)")
        print("L3. List All Log Files")
        print("0. Back to Main Menu")
        choice = input("Logbook Menu Choice: ").upper()

        if choice == 'L1':
            entry_text = input("Enter log entry text: ")
            exp_id = input("Enter Experiment ID (optional, press Enter to skip): ")
            level = input("Enter log level (INFO, WARNING, ERROR, DEBUG - default INFO): ").upper()
            if not level: level = "INFO"
            exp_id = exp_id if exp_id else None
            success, msg = logbook.add_log_entry(entry_text, project_base_path=SCRIPT_DIR, experiment_id=exp_id, level=level)
            print(msg)
        elif choice == 'L2':
            identifier = input("Enter log filename (e.g., log_YYYYMMDD.txt) or date (YYYYMMDD or YYYY-MM-DD): ")
            content, msg = logbook.view_log_file(identifier, project_base_path=SCRIPT_DIR)
            print(f"\n--- {msg} ---")
            if content: print(content.strip())
            else: print("No content found or error retrieving log.")
            print("--- End of Log View ---")
        elif choice == 'L3':
            files, msg = logbook.list_log_files(project_base_path=SCRIPT_DIR)
            print(msg)
            if files:
                print("Available log files (most recent first):")
                for f_name in files: print(f"  - {f_name}")
        elif choice == '0': break
        else: print("Invalid Logbook menu choice.")
        if choice != '0': input("\nPress Enter to return to Logbook Menu...")

# --- Data Management Menu Handler (Basic CSV) ---
def handle_data_management_menu():
    from data_manager import data_loader, data_storage

    # Ensure data directory exists if user wants to interact with it
    data_loader._ensure_data_files_dir_exists(SCRIPT_DIR)

    while True:
        print("\n--- Data Management (CSV) Menu ---")
        print("DM1. Load CSV File to DataFrame")
        print("DM2. Display DataFrame Summary Statistics (requires loaded DataFrame)")
        print("DM3. Save DataFrame to CSV File (requires loaded DataFrame)")
        print("DM4. List CSV Data Files in storage")
        print("0. Back to Main Menu")
        choice = input("Data Management Menu Choice: ").upper()

        # Basic state: keep one loaded DataFrame in memory for this menu session
        # This is very simplistic; a real app might manage multiple DataFrames.
        if 'current_df' not in handle_data_management_menu.__dict__: # Initialize if not exists
            handle_data_management_menu.current_df = None
            handle_data_management_menu.current_df_name = ""

        if choice == 'DM1':
            file_name = input(f"Enter CSV filename (expected in '{data_loader.get_data_files_dir(SCRIPT_DIR)}'): ")
            df, msg = data_loader.load_csv(file_name, project_base_path=SCRIPT_DIR)
            print(msg)
            if df is not None:
                handle_data_management_menu.current_df = df
                handle_data_management_menu.current_df_name = file_name
                print(f"DataFrame '{file_name}' is now loaded.")
            else:
                handle_data_management_menu.current_df = None # Clear if load failed
                handle_data_management_menu.current_df_name = ""
        elif choice == 'DM2':
            if handle_data_management_menu.current_df is not None:
                summary = data_loader.display_summary_statistics(handle_data_management_menu.current_df, handle_data_management_menu.current_df_name)
                print(summary)
            else:
                print("No DataFrame loaded. Please load a CSV first using DM1.")
        elif choice == 'DM3':
            if handle_data_management_menu.current_df is not None:
                save_filename = input(f"Enter filename to save DataFrame as (e.g., processed_{handle_data_management_menu.current_df_name}): ")
                overwrite_choice = input("Overwrite if exists? (yes/no): ").lower()
                overwrite = True if overwrite_choice == 'yes' else False
                success, msg = data_storage.save_df_to_csv(handle_data_management_menu.current_df, save_filename, SCRIPT_DIR, overwrite)
                print(msg)
            else:
                print("No DataFrame loaded to save. Please load a CSV first using DM1.")
        elif choice == 'DM4':
            files, msg = data_storage.list_data_files(SCRIPT_DIR, extension_filter=".csv")
            print(msg)
            if files:
                print("Available CSV files in data storage:")
                for f_name in files: print(f"  - {f_name}")
            elif not msg.startswith("Error"): print("No CSV files found.")

        elif choice == '0': break
        else: print("Invalid Data Management menu choice.")
        if choice != '0': input("\nPress Enter to return to Data Management Menu...")


# --- Main Application Loop ---
def initialize_project_directories():
    """Ensures all necessary base directories for modules exist."""
    # These are the top-level directories within SCRIPT_DIR (planetary_scientist_assistant/)
    # that modules might expect or create subdirectories within (like local_documents, local_notes)
    module_data_roots = [
        os.path.join(SCRIPT_DIR, "local_documents"),
        os.path.join(SCRIPT_DIR, "local_notes"),
        os.path.join(SCRIPT_DIR, "experiment_logs"),
        os.path.join(SCRIPT_DIR, "data_manager_files"),
    ]
    # Directories for the module code itself
    module_code_paths = [
        os.path.join(SCRIPT_DIR, "knowledge_base"),
        os.path.join(SCRIPT_DIR, "sci_utils"),
        os.path.join(SCRIPT_DIR, "experiment_support"),
        os.path.join(SCRIPT_DIR, "data_manager"),
        os.path.join(SCRIPT_DIR, "tests") # ui dir not used if CLI is in main.py
    ]

    print("Ensuring base directories for PSA:")
    for d_path in module_data_roots + module_code_paths:
        os.makedirs(d_path, exist_ok=True)
        # print(f"  Ensured: {d_path}")


def main_application_loop():
    from autonomous_agent import AutonomousAgent
    agent = AutonomousAgent(SCRIPT_DIR)

    display_welcome_message()
    initialize_project_directories() # Create all necessary directories upfront

    while True:
        choice = display_main_menu(agent)
        if choice == '1': handle_knowledge_base_menu()
        elif choice == '2': handle_sci_utils_menu()
        elif choice == '3': handle_experiment_logbook_menu()
        elif choice == '4': handle_data_management_menu()
        elif choice == '0':
            print("\nExiting Planetary Scientist's Assistant. Goodbye!")
            break
        else:
            print("\nInvalid main menu choice. Please try again.")
            input("Press Enter to continue...")

if __name__ == "__main__":
    # This structure assumes main.py is inside 'planetary_scientist_assistant' directory,
    # and this directory is the root for all its modules and data subdirectories.
    main_application_loop()

def add_document(file_path, project_base_path):
    # Add your logic here, using file_path and project_base_path as needed
    pass

