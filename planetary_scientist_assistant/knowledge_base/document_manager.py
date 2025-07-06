# planetary_scientist_assistant/knowledge_base/document_manager.py
import os
import shutil
import json
from datetime import datetime

METADATA_FILE = "metadata.json"
DOCUMENTS_DIR = "local_documents" # Relative to the knowledge_base directory or a global base? For now, assume relative to project root for simplicity.
# Let's make DOCUMENTS_DIR relative to the project root for easier management from main.py
# So, when used from main.py, it would be planetary_scientist_assistant/local_documents
# However, this module itself is in planetary_scientist_assistant/knowledge_base/
# For consistency, let's define paths relative to the project root.
# The main application will ensure these paths are correctly referenced.

PROJECT_ROOT_DOCS_DIR = "planetary_scientist_assistant/local_documents"
PROJECT_ROOT_KB_METADATA_PATH = os.path.join(PROJECT_ROOT_DOCS_DIR, METADATA_FILE)


def _ensure_docs_dir_exists():
    """Ensures the documents directory and metadata file exist."""
    os.makedirs(PROJECT_ROOT_DOCS_DIR, exist_ok=True)
    if not os.path.exists(PROJECT_ROOT_KB_METADATA_PATH):
        with open(PROJECT_ROOT_KB_METADATA_PATH, 'w') as f:
            json.dump({}, f)

def _load_metadata():
    """Loads the metadata from the JSON file."""
    _ensure_docs_dir_exists()
    try:
        with open(PROJECT_ROOT_KB_METADATA_PATH, 'r') as f:
            metadata = json.load(f)
    except (IOError, json.JSONDecodeError):
        metadata = {} # Initialize if file is corrupted or empty
    return metadata

def _save_metadata(metadata):
    """Saves the metadata to the JSON file."""
    _ensure_docs_dir_exists()
    with open(PROJECT_ROOT_KB_METADATA_PATH, 'w') as f:
        json.dump(metadata, f, indent=4)

def add_document(file_path):
    """
    Adds a document to the local collection.
    Copies the document to the local_documents directory and records metadata.

    Args:
        file_path (str): The path to the document to add.

    Returns:
        bool: True if successful, False otherwise.
        str: Message indicating success or failure.
    """
    _ensure_docs_dir_exists()
    if not os.path.exists(file_path):
        return False, f"Error: Source file '{file_path}' not found."

    if not os.path.isfile(file_path):
        return False, f"Error: Source '{file_path}' is not a file."

    filename = os.path.basename(file_path)
    destination_path = os.path.join(PROJECT_ROOT_DOCS_DIR, filename)

    if os.path.exists(destination_path):
        # Simple conflict resolution: append a timestamp or number if desired
        # For now, we'll just indicate it already exists.
        # A more robust solution might involve versioning or unique naming.
        return False, f"Error: Document '{filename}' already exists in the knowledge base."

    try:
        shutil.copy(file_path, destination_path)
        metadata = _load_metadata()

        doc_id = filename # Using filename as ID for simplicity; could be a UUID
        metadata[doc_id] = {
            "original_filename": filename,
            "path_in_kb": destination_path, # Storing the path within the KB structure
            "import_date": datetime.now().isoformat(),
            "size_bytes": os.path.getsize(destination_path),
            "file_type": os.path.splitext(filename)[1].lower()
        }
        _save_metadata(metadata)
        return True, f"Document '{filename}' added successfully to the knowledge base."
    except Exception as e:
        # Clean up if copy succeeded but metadata failed (optional)
        if os.path.exists(destination_path):
            # Check if it was the one we just copied before removing
            # This check is basic; more robust would be to ensure it wasn't pre-existing from a race condition
            pass # For now, leave it, as metadata is the source of truth for "managed" files
        return False, f"Error adding document '{filename}': {e}"

def list_documents():
    """
    Lists all documents currently in the knowledge base.

    Returns:
        list: A list of dictionaries, where each dictionary contains metadata of a document.
              Returns an empty list if no documents or metadata found.
    """
    metadata = _load_metadata()
    return [info for doc_id, info in metadata.items()]


def search_documents_by_keyword(keyword):
    """
    Searches documents by keyword in their content (basic text search).
    This is a very basic implementation and will be slow for large files or many documents.
    It only searches plain text and PDF files (if PyPDF2 is available and integrated).

    Args:
        keyword (str): The keyword to search for. Case-insensitive.

    Returns:
        list: A list of document metadata (dict) for documents containing the keyword.
    """
    if not keyword:
        return []

    keyword = keyword.lower()
    metadata = _load_metadata()
    found_documents_info = []

    for doc_id, info in metadata.items():
        file_path_in_kb = info.get("path_in_kb")
        file_type = info.get("file_type")

        if not file_path_in_kb or not os.path.exists(file_path_in_kb):
            # print(f"Warning: Document '{doc_id}' listed in metadata but not found at '{file_path_in_kb}'. Skipping.")
            continue

        try:
            content_to_search = ""
            if file_type == ".txt":
                with open(file_path_in_kb, 'r', encoding='utf-8', errors='ignore') as f:
                    content_to_search = f.read()
            elif file_type == ".pdf":
                try:
                    import PyPDF2
                    with open(file_path_in_kb, 'rb') as f:
                        reader = PyPDF2.PdfReader(f)
                        for page_num in range(len(reader.pages)):
                            content_to_search += reader.pages[page_num].extract_text() or ""
                except ImportError:
                    # print(f"PyPDF2 library not found. Cannot search PDF: {doc_id}. Please install it (`pip install PyPDF2`)")
                    pass # Silently skip if PyPDF2 not available, or log it.
                except Exception as pdf_e:
                    # print(f"Error reading PDF '{doc_id}': {pdf_e}")
                    pass # Skip malformed PDFs

            # Add more file types here if needed (e.g., .md, .json)
            # For .json, .md, they can be treated like .txt for simple keyword search

            if keyword in content_to_search.lower():
                found_documents_info.append(info)
        except Exception as e:
            # print(f"Error processing file '{doc_id}' for search: {e}")
            continue # Skip files that cause errors during search

    return found_documents_info

def get_document_path(doc_id_or_filename):
    """
    Retrieves the full path of a document in the knowledge base by its ID/filename.

    Args:
        doc_id_or_filename (str): The ID or filename of the document.

    Returns:
        str or None: The full path to the document if found, else None.
    """
    metadata = _load_metadata()
    doc_info = metadata.get(doc_id_or_filename)
    if doc_info:
        return doc_info.get("path_in_kb")
    return None

def remove_document(doc_id_or_filename):
    """
    Removes a document from the knowledge base (deletes file and metadata entry).

    Args:
        doc_id_or_filename (str): The ID or filename of the document to remove.

    Returns:
        bool: True if successful, False otherwise.
        str: Message indicating success or failure.
    """
    metadata = _load_metadata()
    doc_info = metadata.get(doc_id_or_filename)

    if not doc_info:
        return False, f"Error: Document '{doc_id_or_filename}' not found in metadata."

    file_path_in_kb = doc_info.get("path_in_kb")

    try:
        if file_path_in_kb and os.path.exists(file_path_in_kb):
            os.remove(file_path_in_kb)

        # Remove from metadata
        del metadata[doc_id_or_filename]
        _save_metadata(metadata)

        return True, f"Document '{doc_id_or_filename}' removed successfully."
    except Exception as e:
        return False, f"Error removing document '{doc_id_or_filename}': {e}"

if __name__ == '__main__':
    # Basic test and usage examples
    print("Document Manager - Basic Test")
    _ensure_docs_dir_exists() # Ensure directory is there for testing

    # Create dummy files for testing
    test_txt_file = "planetary_scientist_assistant/test_doc.txt"
    test_pdf_file = "planetary_scientist_assistant/test_doc.pdf" # Requires a real PDF for PDF search to work

    with open(test_txt_file, "w") as f:
        f.write("This is a test document for the Planetary Scientist's Assistant.\nIt contains keywords like science, planet, and data.")

    # For PDF, you'd need to create one. For now, we'll just test adding it.
    # Actual PDF search testing would require PyPDF2 and a valid PDF file.
    # For simplicity in this test, we'll skip creating a real PDF unless PyPDF2 is confirmed available
    # and focus on the mechanism.

    print("\n1. Adding documents:")
    success, msg = add_document(test_txt_file)
    print(f"Adding '{test_txt_file}': {msg}")

    # Attempt to add a non-existent PDF to see error handling (if not creating one)
    # success, msg = add_document(test_pdf_file)
    # print(f"Adding '{test_pdf_file}': {msg}") # This will fail if file doesn't exist

    print("\n2. Listing documents:")
    docs = list_documents()
    if docs:
        for doc in docs:
            print(f"  - {doc.get('original_filename')} (Imported: {doc.get('import_date')}, Type: {doc.get('file_type')})")
    else:
        print("  No documents in knowledge base.")

    print("\n3. Searching documents (keyword: 'planet'):")
    found = search_documents_by_keyword("planet")
    if found:
        for doc_info in found:
            print(f"  Found in: {doc_info.get('original_filename')}")
    else:
        print("  No documents found with the keyword 'planet'.")

    print("\n4. Searching documents (keyword: 'galaxy'):")
    found_galaxy = search_documents_by_keyword("galaxy")
    if found_galaxy:
        for doc_info in found_galaxy:
            print(f"  Found in: {doc_info.get('original_filename')}")
    else:
        print("  No documents found with the keyword 'galaxy'.")

    print("\n5. Getting document path:")
    path = get_document_path("test_doc.txt")
    print(f"  Path for 'test_doc.txt': {path}")

    print("\n6. Removing document:")
    success, msg = remove_document("test_doc.txt")
    print(f"Removing 'test_doc.txt': {msg}")

    # Verify removal
    docs_after_removal = list_documents()
    print(f"  Documents after removal: {len(docs_after_removal)}")


    # Clean up dummy files created directly in project root (not the KB copies)
    if os.path.exists(test_txt_file):
        os.remove(test_txt_file)
    # if os.path.exists(test_pdf_file): # If it was created
    #     os.remove(test_pdf_file)

    print("\nTest complete. Check the 'planetary_scientist_assistant/local_documents' directory and its metadata.json.")
