# Lab 3 — Build the tool loop

*(Skeleton — starter, solution, and tests land in Phase 1.)*

**Goal:** implement `run_agent(model, tools, user_msg, max_turns=8)` —
the loop from Trace 2 — against a scripted model, no API keys.

**Level:** L1 · **Stack:** plain Python · **Time:** ~45 min · **Offline:** yes, fully.

**Done means:** all tests pass. The tests define the contract:
the happy path returns the right answer,
malformed tool arguments and unknown tools surface to the model as error results,
and the loop halts at `max_turns` and says so.

```bash
uv sync
uv run pytest                      # your task list
LAB_TARGET=solution uv run pytest  # the reference passing
```
