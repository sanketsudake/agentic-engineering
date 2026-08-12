"""Provided part: the toolbox. Working — do not edit.

Three read-only tools over a tiny in-process runbook store, declared
Lab 2 style: a definition the model reads, an implementation the harness
runs. `make_toolbox()` builds a fresh toolbox per run so no test depends
on another.
"""
from __future__ import annotations

import copy

RUNBOOKS = {
    "api-restart": ("1. Drain traffic from the pod.\n"
                    "2. Send SIGTERM and wait 30 seconds.\n"
                    "3. Start the pod and watch the healthcheck."),
    "db-failover": ("1. Freeze writes on the primary.\n"
                    "2. Promote the replica.\n"
                    "3. Repoint the connection string.\n"
                    "4. Unfreeze writes."),
    "cache-flush": ("1. Flush the cache keys under app:*.\n"
                    "2. Warm the top 100 queries."),
}


def list_runbooks() -> str:
    """Return every runbook name, one per line, sorted."""
    return "\n".join(sorted(RUNBOOKS))


def read_runbook(name: str) -> str:
    """Return the full content of one runbook."""
    if name not in RUNBOOKS:
        raise KeyError(f"no runbook named {name}")
    return RUNBOOKS[name]


def count_steps(name: str) -> str:
    """Return the number of steps in one runbook."""
    if name not in RUNBOOKS:
        raise KeyError(f"no runbook named {name}")
    return str(len(RUNBOOKS[name].splitlines()))


TOOL_DEFS = {
    "list_runbooks": {
        "name": "list_runbooks",
        "description": (
            "List every available runbook name, one per line. "
            "Call this first when you do not know which runbook applies."
        ),
        "input_schema": {
            "type": "object",
            "properties": {},
            "required": [],
            "additionalProperties": False,
        },
    },
    "read_runbook": {
        "name": "read_runbook",
        "description": (
            "Return the full numbered steps of one runbook. "
            "Call this before answering any question about a procedure; "
            "use list_runbooks first if you do not know the exact name."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "Exact runbook name, from list_runbooks.",
                },
            },
            "required": ["name"],
            "additionalProperties": False,
        },
    },
    "count_steps": {
        "name": "count_steps",
        "description": (
            "Return how many steps one runbook has. "
            "Call this when only the length matters, not the content."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "Exact runbook name, from list_runbooks.",
                },
            },
            "required": ["name"],
            "additionalProperties": False,
        },
    },
}


def make_toolbox() -> dict:
    """A fresh toolbox: {"tool_defs": ..., "registry": ...}."""
    return {
        "tool_defs": copy.deepcopy(TOOL_DEFS),
        "registry": {
            "list_runbooks": list_runbooks,
            "read_runbook": read_runbook,
            "count_steps": count_steps,
        },
    }
