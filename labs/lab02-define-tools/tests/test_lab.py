"""Lab 2 checker: schema quality first, then dispatcher behavior."""
from worksheet_common import ToolCall

EXPECTED = {
    "search_notes": {"required": ["query"], "props": {"query": "string", "limit": "integer"}},
    "write_note": {"required": ["title", "body"], "props": {"title": "string", "body": "string"}},
    "delete_note": {"required": ["note_id"], "props": {"note_id": "integer"}},
}


def test_schemas_are_complete(schemas):
    for name, want in EXPECTED.items():
        d = schemas.TOOL_DEFS[name]
        s = d["input_schema"]
        assert s.get("type") == "object", f"{name}: input_schema.type must be object"
        assert s.get("additionalProperties") is False, f"{name}: set additionalProperties false"
        assert sorted(s.get("required", [])) == sorted(want["required"]), f"{name}: wrong required list"
        for prop, jtype in want["props"].items():
            spec = s.get("properties", {}).get(prop)
            assert spec, f"{name}: missing property {prop}"
            assert spec.get("type") == jtype, f"{name}.{prop}: type must be {jtype}"
            assert spec.get("description", "").strip(), f"{name}.{prop}: needs a description"


def test_descriptions_say_when_to_call(schemas):
    for name, d in schemas.TOOL_DEFS.items():
        desc = d["description"]
        assert len(desc.split(".")) >= 2 and len(desc) >= 80, (
            f"{name}: description too thin — say what it does AND when to call it")
    assert "permanent" in schemas.TOOL_DEFS["delete_note"]["description"].lower() or \
           "cannot be undone" in schemas.TOOL_DEFS["delete_note"]["description"].lower(), \
        "delete_note: warn the model that deletion is permanent"


def test_dispatch_happy_path(schemas, dispatch_mod):
    out = dispatch_mod.dispatch_tool_call(
        ToolCall("t1", "write_note", {"title": "a", "body": "b"}),
        schemas.TOOL_DEFS, schemas.REGISTRY)
    assert out == "created note 1"


def test_unknown_tool(schemas, dispatch_mod):
    out = dispatch_mod.dispatch_tool_call(
        ToolCall("t1", "send_email", {"to": "x"}), schemas.TOOL_DEFS, schemas.REGISTRY)
    assert out == "error: unknown tool send_email"


def test_missing_required_argument(schemas, dispatch_mod):
    out = dispatch_mod.dispatch_tool_call(
        ToolCall("t1", "write_note", {"title": "a"}), schemas.TOOL_DEFS, schemas.REGISTRY)
    assert out == "error: missing required argument body"


def test_unknown_argument(schemas, dispatch_mod):
    out = dispatch_mod.dispatch_tool_call(
        ToolCall("t1", "search_notes", {"query": "x", "q": "x"}),
        schemas.TOOL_DEFS, schemas.REGISTRY)
    assert out == "error: unknown argument q"


def test_wrong_argument_type(schemas, dispatch_mod):
    out = dispatch_mod.dispatch_tool_call(
        ToolCall("t1", "delete_note", {"note_id": "1"}), schemas.TOOL_DEFS, schemas.REGISTRY)
    assert out == "error: argument note_id must be integer"


def test_tool_exception_surfaces_as_error(schemas, dispatch_mod):
    out = dispatch_mod.dispatch_tool_call(
        ToolCall("t1", "delete_note", {"note_id": 99}), schemas.TOOL_DEFS, schemas.REGISTRY)
    assert out.startswith("error:") and "99" in out


def test_optional_argument_accepted(schemas, dispatch_mod):
    dispatch_mod.dispatch_tool_call(
        ToolCall("t1", "write_note", {"title": "grocery list", "body": "eggs"}),
        schemas.TOOL_DEFS, schemas.REGISTRY)
    out = dispatch_mod.dispatch_tool_call(
        ToolCall("t2", "search_notes", {"query": "grocery", "limit": 1}),
        schemas.TOOL_DEFS, schemas.REGISTRY)
    assert "grocery list" in out
