# L1 Practical — Assemble the micro-agent

**Section B of the L1 exam** · 30 points · ~45 min · open-repo · offline, no API keys.

The parts of a working agent are provided;
the loop that wires them together is not.
You assemble it.

## Setup

```bash
uv sync
uv run pytest        # as shipped: all 10 red — that is the exam
```

## The parts (provided working — do not edit)

- `parts/dispatcher.py` — `dispatch_tool_call(call, toolbox) -> str`.
  Validates the call against the toolbox's schemas, runs the tool,
  and turns every failure into an `"error: ..."` string. It never raises.
- `parts/toolbox.py` — three working read-only tools over a runbook store,
  plus `make_toolbox()`, which returns `{"tool_defs": ..., "registry": ...}`.
- `tests/test_practical.py` — the checker, driven by `ScriptedModel`
  (`worksheet_common`): a deterministic fake model, so no keys are needed.

## Your work

Implement `run_agent(model, dispatcher, toolbox, user_msg, max_turns=6)`
in `assemble/agent.py`.
Its docstring is the full spec.
The contract in brief:

- Every tool result flows through the provided `dispatcher` —
  never call a registry function directly, never rewrite its output.
- Results are appended in the model's order, each with its matching
  `tool_call_id`.
- If the model's text contains `DONE:`, stop immediately —
  dispatch nothing from that response —
  and return the text after the marker as the answer.
- After `max_turns` model calls, halt with `stopped="max_turns"`.
- Treat the toolbox as read-only.

Your changes go in `assemble/agent.py` only.

## Scoring — 10 checks × 3 points

Self-scoring, no judgment needed: `uv run pytest`, 3 points per passing check.

| Check | What it verifies | Points |
|---|---|---|
| `test_happy_path_returns_answer` | the loop runs a tool turn and returns the final text | 3 |
| `test_dispatcher_is_actually_used` | results flow through the injected dispatcher | 3 |
| `test_results_appended_in_order_with_matching_ids` | parallel calls keep order and ids | 3 |
| `test_unknown_tool_error_surfaced` | a hallucinated tool becomes visible error text | 3 |
| `test_malformed_args_error_surfaced` | a schema-invalid call becomes visible error text | 3 |
| `test_done_marker_stops_early` | `DONE:` stops the loop and returns the suffix | 3 |
| `test_max_turns_halts_with_stopped_state` | the turn cap halts with `stopped="max_turns"` | 3 |
| `test_transcript_shape_is_valid` | the transcript follows the documented shapes | 3 |
| `test_model_called_expected_number_of_times` | no extra or missing model calls | 3 |
| `test_toolbox_not_mutated` | the toolbox comes back untouched | 3 |

**Done means:** `uv run pytest` reports 10 passed.
Paste the output into the exam's score sheet.
