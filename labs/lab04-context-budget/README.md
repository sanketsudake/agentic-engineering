# Lab 4 — Keep a session under a token budget

**Goal:** implement `fit_context()` — a compactor the harness calls before
every model turn so a long session never blows its context window.

**Level:** [L2] · **Stack:** plain Python · **Time:** ~45 min

**Offline mode (default, no keys):**

```bash
uv sync
uv run pytest                      # 9 red tests are your task list
```

**Reference check:**

```bash
LAB_TARGET=solution uv run pytest  # the reference implementation passing
```

## Your task

1. Read `starter/budget/tokens.py` first. Token counting is provided and
   fixed: `count_tokens(text) = max(1, len(text) // 4)`, plus 4 tokens of
   overhead per message. You do not touch this file.
2. Open `starter/budget/fit.py`. The docstring on `fit_context()` is the
   full spec, in priority order: never lose the system or task message,
   never exceed the budget, truncate oversized tool results before
   dropping anything, then drop whole turns oldest-first, and mark what you
   dropped so the model knows its context was compacted.
3. Make the 9 tests in `tests/test_lab.py` pass. They run against the
   shared 22-message coding-agent fixture in `tests/conftest.py` — a
   realistic session with one 5,000-character tool dump buried in the
   middle.

**Done means:** `uv run pytest` is fully green against `starter/`.

## What this proves

A harness cannot hand the model an unbounded transcript — every context
window has a ceiling, and a long session hits it. Trace 8 (Chapter 3,
"what happens when the context window fills") is this lab end to end:
the harness truncates, then drops, then tells the model what happened.

The order matters. Truncating an oversized tool result loses detail, but
the shape of the exchange survives. Dropping a whole turn is worse: the
model no longer has the intermediate steps that got it to its current
state, and Trace 7 ("what happens when the context for a turn is
assembled") shows what it does next — it re-derives what it can no longer
see. Silent context loss is the failure mode; a strong harness makes the
loss visible instead, with a marker message, so the model can ask again
rather than confidently restate a wrong assumption.

There is no live mode for this lab on purpose: `fit_context()` never calls
a model. It is pure list-in, list-out logic over a transcript, so the same
9 tests can assert its behavior exactly, turn by turn.
