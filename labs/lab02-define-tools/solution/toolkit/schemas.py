"""Reference tool definitions."""
from . import impl

TOOL_DEFS = {
    "search_notes": {
        "name": "search_notes",
        "description": (
            "Search the note store by keyword and return matching note ids and "
            "titles. Call this before reading, updating, or deleting a note "
            "when you do not already know its id."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Keywords to match against note titles and bodies.",
                },
                "limit": {
                    "type": "integer",
                    "description": "Maximum number of matches to return. Defaults to 5.",
                },
            },
            "required": ["query"],
            "additionalProperties": False,
        },
    },
    "write_note": {
        "name": "write_note",
        "description": (
            "Create a new note with a title and body, and return its id. "
            "Call this when the user asks to save, record, or remember something."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "title": {
                    "type": "string",
                    "description": "Short title for the note.",
                },
                "body": {
                    "type": "string",
                    "description": "Full text content of the note.",
                },
            },
            "required": ["title", "body"],
            "additionalProperties": False,
        },
    },
    "delete_note": {
        "name": "delete_note",
        "description": (
            "Permanently delete one note by id; this cannot be undone. "
            "Call this only when the user explicitly asks to remove a note, "
            "and use search_notes first if you do not know the id."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "note_id": {
                    "type": "integer",
                    "description": "The id of the note to delete, from search_notes.",
                },
            },
            "required": ["note_id"],
            "additionalProperties": False,
        },
    },
}

REGISTRY = {
    "search_notes": impl.search_notes,
    "write_note": impl.write_note,
    "delete_note": impl.delete_note,
}
