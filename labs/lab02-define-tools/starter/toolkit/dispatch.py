"""Lab 2, part 2 — your task: implement the dispatcher.

The dispatcher sits at step 4-5 of Trace 2: it turns a model's ToolCall into
a real function call, and turns every failure into an error STRING the model
can read. It must never raise.
"""
from __future__ import annotations

from worksheet_common import ToolCall

_JSON_TYPES = {"string": str, "integer": int, "number": (int, float), "boolean": bool}


def dispatch_tool_call(call: ToolCall, tool_defs: dict, registry: dict) -> str:
    """Validate `call.input` against the tool's schema, then execute.

    Return values (the tests define these exactly):
    - unknown tool name          -> "error: unknown tool <name>"
    - missing required argument  -> "error: missing required argument <name>"
    - unknown argument           -> "error: unknown argument <name>"
    - wrong argument type        -> "error: argument <name> must be <json type>"
    - the tool itself raises     -> "error: <exception message>"
    - success                    -> the tool's return value as a string

    Check in that order; report the first problem found (for arguments,
    iterate schema properties in definition order, then extra keys sorted).
    """
    raise NotImplementedError("your dispatcher goes here")
