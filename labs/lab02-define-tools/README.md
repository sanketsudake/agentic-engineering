# Lab 2 — Define and dispatch tools

**Goal:** write tool definitions the model can use well, and a dispatcher that
survives bad input. A tool definition is a prompt: its description and schema
are the only things the model sees before it decides to call.

**Level:** L1 · **Stack:** plain Python · **Time:** ~30 min

**Offline mode (default, no keys):**

```bash
uv sync
uv run pytest                      # red tests are your task list
```

**Reference check:**

```bash
LAB_TARGET=solution uv run pytest
```

## Your task

1. `starter/toolkit/schemas.py` — complete the three tool definitions
   (`search_notes`, `write_note`, `delete_note`): typed properties, per-property
   descriptions, `required`, `additionalProperties: false`, and a description
   that says WHEN to call the tool, not only what it does.
2. `starter/toolkit/dispatch.py` — implement `dispatch_tool_call()`: validate
   the input against the schema (missing required args, unknown args, wrong
   types), execute on success, and return every failure as an error STRING the
   model can read and correct.

**Done means:** `uv run pytest` fully green against `starter/`.

## What this proves

Schema quality and error surfacing are what separate tools a model uses well
from tools it fumbles (see Trace 9 and Trace 10 in Chapter 4).

There is no live mode: the tests assert schema shape and dispatcher behavior
directly, which needs no model at all.
