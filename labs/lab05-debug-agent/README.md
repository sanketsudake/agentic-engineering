# Lab 5 — Debug a broken agent

**Goal:** find and fix three bugs planted in a complete,
working-looking agent loop.

**Level:** L2 · **Stack:** plain Python · **Time:** ~45 min

**Offline mode (default, no keys):**

```bash
uv sync
uv run pytest                      # the failing tests are your task list
```

**Reference check:**

```bash
LAB_TARGET=solution uv run pytest  # the reference implementation passing
```

## Your task

1. Open `starter/agent/loop.py`.
   It runs.
   It looks production-ready.
   It dispatches tools, handles unknown tools, retries on timeout,
   and never crashes on a bad tool call.
   It still has three bugs.
2. Read the failing tests in `tests/test_lab.py` first.
   Each test names one bug and states the correct behavior.
3. Fix `starter/agent/loop.py` until the tests pass.
   Do not change the tests or `starter/agent/tools.py`.

**Done means:** `uv run pytest` is fully green against `starter/`.

## What this proves

Three bug classes account for most production agent incidents
(see Trace 10 and the Chapter 4 code-reading exercises):

- **Context flood** — a tool result lands in the transcript with no size limit,
  and it crowds out everything else the model needs to see.
- **Non-idempotent retry** — the harness re-runs a tool after a timeout,
  even though the tool is not safe to call twice.
- **Swallowed error** — a tool raises,
  and the harness turns that failure into a silent empty result.
  The model reads silence as success.

Finding these bugs by reading failing tests, not by guessing,
is the operator skill this lab checks.
