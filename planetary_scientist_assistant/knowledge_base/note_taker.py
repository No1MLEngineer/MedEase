# planetary_scientist_assistant/knowledge_base/note_taker.py
import os
import json
import uuid
from datetime import datetime

NOTES_SUBDIR_NAME = "local_notes"
NOTES_METADATA_FILENAME = "notes_metadata.json"
NOTES_CONTENT_DIR_NAME = "content"

def get_project_notes_dir(project_base_path):
    return os.path.join(project_base_path, NOTES_SUBDIR_NAME)

def get_notes_metadata_path(project_base_path):
    return os.path.join(get_project_notes_dir(project_base_path), NOTES_METADATA_FILENAME)

def get_notes_content_dir(project_base_path):
    return os.path.join(get_project_notes_dir(project_base_path), NOTES_CONTENT_DIR_NAME)

def _ensure_notes_dirs_exist(notes_dir, content_dir, metadata_path):
    os.makedirs(notes_dir, exist_ok=True)
    os.makedirs(content_dir, exist_ok=True)
    if not os.path.exists(metadata_path):
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump({}, f)

def _load_notes_metadata(metadata_path):
    if not os.path.exists(metadata_path):
        return {}
    try:
        with open(metadata_path, 'r', encoding='utf-8') as f:
            content = f.read()
            if not content: return {}
            return json.loads(content)
    except (IOError, json.JSONDecodeError):
        return {}

def _save_notes_metadata(metadata_path, metadata):
    with open(metadata_path, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=4)

def add_note(title, content, project_base_path):
    notes_dir = get_project_notes_dir(project_base_path)
    content_dir = get_notes_content_dir(project_base_path)
    metadata_path = get_notes_metadata_path(project_base_path)
    _ensure_notes_dirs_exist(notes_dir, content_dir, metadata_path)

    note_id = str(uuid.uuid4())
    note_filename = f"{note_id}.txt"
    note_content_filepath = os.path.join(content_dir, note_filename)
    metadata = _load_notes_metadata(metadata_path)

    if note_id in metadata:
        return False, "Error: Note ID collision. Please try again."

    try:
        with open(note_content_filepath, 'w', encoding='utf-8') as f:
            f.write(content)

        metadata[note_id] = {
            "id": note_id, "title": title,
            "created_date": datetime.now().isoformat(),
            "last_modified_date": datetime.now().isoformat(),
            "content_filename": note_filename
        }
        _save_notes_metadata(metadata_path, metadata)
        return True, f"Note '{title}' (ID: {note_id}) added."
    except Exception as e:
        if os.path.exists(note_content_filepath) and note_id not in _load_notes_metadata(metadata_path):
            try: os.remove(note_content_filepath)
            except OSError: pass
        return False, f"Error adding note '{title}': {e}"

def list_notes(project_base_path):
    notes_dir = get_project_notes_dir(project_base_path)
    content_dir = get_notes_content_dir(project_base_path)
    metadata_path = get_notes_metadata_path(project_base_path)
    _ensure_notes_dirs_exist(notes_dir, content_dir, metadata_path)
    metadata = _load_notes_metadata(metadata_path)
    return sorted(metadata.values(), key=lambda x: x.get("created_date", ""), reverse=True)

def get_note_content(note_id, project_base_path):
    metadata = _load_notes_metadata(get_notes_metadata_path(project_base_path))
    note_info = metadata.get(note_id)
    if not note_info or not note_info.get("content_filename"): return None

    note_content_filepath = os.path.join(get_notes_content_dir(project_base_path), note_info["content_filename"])
    if not os.path.exists(note_content_filepath): return None
    try:
        with open(note_content_filepath, 'r', encoding='utf-8') as f: return f.read()
    except IOError: return None

def get_note_details(note_id, project_base_path):
    metadata_path = get_notes_metadata_path(project_base_path)
    _ensure_notes_dirs_exist(get_project_notes_dir(project_base_path),
                             get_notes_content_dir(project_base_path),
                             metadata_path)
    return _load_notes_metadata(metadata_path).get(note_id)

def search_notes(keyword, project_base_path):
    if not keyword: return []
    keyword_lower = keyword.lower()
    all_notes_metadata = list_notes(project_base_path)
    found_notes_info = []
    for note_meta in all_notes_metadata:
        if keyword_lower in note_meta.get("title", "").lower():
            found_notes_info.append(note_meta)
            continue
        content = get_note_content(note_meta.get("id"), project_base_path)
        if content and keyword_lower in content.lower():
            found_notes_info.append(note_meta)
    return found_notes_info

def delete_note(note_id, project_base_path):
    notes_dir, content_dir, metadata_path = (get_project_notes_dir(project_base_path),
                                             get_notes_content_dir(project_base_path),
                                             get_notes_metadata_path(project_base_path))
    _ensure_notes_dirs_exist(notes_dir, content_dir, metadata_path)
    metadata = _load_notes_metadata(metadata_path)
    note_info = metadata.get(note_id)

    if not note_info: return False, f"Error: Note ID '{note_id}' not found."

    content_filepath = os.path.join(content_dir, note_info.get("content_filename", "")) if note_info.get("content_filename") else None
    try:
        if content_filepath and os.path.exists(content_filepath): os.remove(content_filepath)
        del metadata[note_id]
        _save_notes_metadata(metadata_path, metadata)
        return True, f"Note ID '{note_id}' (Title: {note_info.get('title')}) deleted."
    except Exception as e:
        return False, f"Error deleting note ID '{note_id}': {e}"

if __name__ == '__main__':
    print("--- Running note_taker.py direct test ---")
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    TEST_PROJECT_BASE = os.path.dirname(SCRIPT_DIR)
    print(f"Using project base for testing: {os.path.abspath(TEST_PROJECT_BASE)}")
    os.makedirs(TEST_PROJECT_BASE, exist_ok=True)

    _ensure_notes_dirs_exist(get_project_notes_dir(TEST_PROJECT_BASE),
                             get_notes_content_dir(TEST_PROJECT_BASE),
                             get_notes_metadata_path(TEST_PROJECT_BASE))
    print("Test environment for notes initialized.")

    title, content = "Test Note Alpha", "Content about alpha particles and planets."
    success, msg = add_note(title, content, TEST_PROJECT_BASE)
    assert success, msg
    note_id_alpha = list_notes(TEST_PROJECT_BASE)[0]['id']
    print(f"Added note '{title}': {msg}")

    assert get_note_content(note_id_alpha, TEST_PROJECT_BASE) == content
    assert len(search_notes("alpha", TEST_PROJECT_BASE)) == 1

    success, msg = delete_note(note_id_alpha, TEST_PROJECT_BASE)
    assert success, msg
    assert len(list_notes(TEST_PROJECT_BASE)) == 0
    print("Direct tests passed for note_taker.py.")
    print("--- note_taker.py direct test complete ---")
