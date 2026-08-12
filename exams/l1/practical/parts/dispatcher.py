"""Provided part: the dispatcher. Working — do not edit.

Lab 2's reference dispatcher, adapted to take the whole toolbox:
it validates a tool call against the toolbox's schemas, runs the tool,
and turns every failure into text the model can read. It never raises.
"""
from __future__ import annotations

from worksheet_common import ToolCall

_JSON_TYPES = {"string": str, "integer": int, "number": (int, float), "boolean": bool}


def dispatch_tool_call(call: ToolCall, toolbox: dict) -> str:
    tool_defs, registry = toolbox["tool_defs"], toolbox["registry"]
    if call.name not in registry or call.name not in tool_defs:
        return f"error: unknown tool {call.name}"
    schema = tool_defs[call.name]["input_schema"]
    props = schema.get("properties", {})
    required = schema.get("required", [])
    for name in props:
        if name in required and name not in call.input:
            return f"error: missing required argument {name}"
    for name in sorted(call.input):
        if name not in props:
            return f"error: unknown argument {name}"
    for name, spec in props.items():
        if name in call.input:
            expected = _JSON_TYPES.get(spec.get("type"))
            # bool is an int subclass in Python; reject it for integer args
            value = call.input[name]
            if expected and (not isinstance(value, expected) or
                             (spec.get("type") == "integer" and isinstance(value, bool))):
                return f"error: argument {name} must be {spec['type']}"
    try:
        return str(registry[call.name](**call.input))
    except Exception as exc:  # surface, never crash
        return f"error: {exc}"
