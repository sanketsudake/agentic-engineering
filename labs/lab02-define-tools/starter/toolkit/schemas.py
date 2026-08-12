"""Lab 2, part 1 — your task: complete the tool definitions.

A tool definition is a prompt. The model reads `description` to decide WHEN
to call, and the schema's property descriptions to decide WHAT to pass.

Requirements the tests check, for every definition:
- `description`: at least two sentences; says when to use the tool.
- `input_schema`: type "object", every property has a type and a non-empty
  "description", a correct "required" list, and "additionalProperties": False.
- `search_notes.limit` is an optional integer; `delete_note.note_id` is a
  required integer.
"""
from . import impl

TOOL_DEFS = {
    "search_notes": {
        "name": "search_notes",
        # TODO: description (what it does AND when to call it)
        "description": "",
        # TODO: input_schema for query (required string) + limit (optional int)
        "input_schema": {},
    },
    "write_note": {
        "name": "write_note",
        "description": "",  # TODO
        "input_schema": {},  # TODO: title + body, both required strings
    },
    "delete_note": {
        "name": "delete_note",
        "description": "",  # TODO: include that deletion is permanent
        "input_schema": {},  # TODO: note_id, required integer
    },
}

REGISTRY = {
    "search_notes": impl.search_notes,
    "write_note": impl.write_note,
    "delete_note": impl.delete_note,
}
