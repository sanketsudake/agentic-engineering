# Lab 3 — Build the tool loop

**Goal:** implement `run_agent()` — the loop from Trace 2 — against a scripted model.
You are the harness: the model proposes tool calls, you validate, dispatch, and loop.

**Level:** L1 · **Stack:** plain Python · **Time:** ~45 min

**Offline mode (default, no keys):**

```bash
uv sync
uv run pytest                      # 7 red tests are your task list
```

**Reference check:**

```bash
LAB_TARGET=solution uv run pytest  # the reference implementation passing
```

## Your task

1. Open `starter/agent/loop.py`. The docstring on `run_agent()` is the full spec.
2. Finish the `TODO` in `starter/agent/tools.py` (`calculator` argument validation).
3. Make the 7 tests in `tests/test_lab.py` pass. Each test names one classic
   loop failure: crashed dispatch, swallowed errors, runaway loops, broken transcripts.

**Done means:** `uv run pytest` is fully green against `starter/`.

## What this proves

A loop that survives bad arguments, unknown tools, and a model that never stops —
the three failures every production harness must absorb (see "Where this can fail"
under Trace 2, and Q 1.4).

There is no live mode for this lab on purpose: the scripted model asserts the
loop's behavior turn by turn, which a real model cannot do deterministically.
