# L2 Practical — Fix the agent the eval caught

**Section C of the L2 exam** · 30 points · ~90 min · open-repo · offline, no API keys.

A vendored tool-loop agent (Lab 3's shape, Lab 8's eval shape) fails
3 of the 10 tasks in the provided eval suite.
Your job has three parts: diagnose, fix, and guard.

## Setup

```bash
uv sync
uv run pytest                      # as shipped: mostly red — that is the exam
uv run python -m evalsuite.run     # the eval report; failing transcripts land in transcripts/
```

## Step 1 — Diagnose (from the transcripts, not from guessing)

Run the eval.
Three tasks fail;
`evalsuite/run.py` writes each failing transcript to `transcripts/<task-id>.json`.
Read them.
Ask the operator's questions:
what did the model ask for, what did it actually see next,
and how did the session end (`stopped`)?
The eval suite is provided working — the suite is not the bug.

Do not edit `evalsuite/tasks.py`, `evalsuite/graders.py`,
`evalsuite/runner.py`, `agent/buggy_reference.py`, or `tests/`.
Your changes go in `agent/loop.py` and `evalsuite/tasks_regression.py` only.

## Step 2 — Fix the agent

Fix `agent/loop.py` so the loop honors this contract:

- Every tool call's result reaches the transcript — success, error, big or small.
- A result larger than `RESULT_BUDGET` stays present but truncated:
  keep the head of the real output, cut near the budget
  (the checker allows up to 500 characters total),
  and append an explicit marker that contains the word `truncated`.
- Keep `RESULT_BUDGET = 400`. Raising the budget is not a fix;
  the next big file would just raise it again.

## Step 3 — Extend the eval (guard the fix)

A fix without a regression task can silently un-fix itself.
Add at least one task to `evalsuite/tasks_regression.py`
(a template is in that file's docstring) that catches the bug class:
your fixed agent must score 1.0 on it,
and the frozen buggy variant in `agent/buggy_reference.py`
must score below 1.0 on it.
The tests re-plant the bug through that frozen module —
that is how "would catch it if it returned" is checked, not claimed.

## Scoring — 10 checks × 3 points

Self-scoring, no judgment needed: `uv run pytest`, 3 points per passing check.

| Checks | What they verify | Points |
|---|---|---|
| `test_aggregate_clears_the_bar` | suite aggregate ≥ 0.9 | 3 |
| `test_build_log_task_passes` | broken task 1 now passes | 3 |
| `test_deploy_log_task_passes` | broken task 2 now passes | 3 |
| `test_latency_report_task_passes` | broken task 3 now passes | 3 |
| `test_no_clean_task_regressed` | the 7 passing tasks still pass | 3 |
| `test_every_tool_call_has_a_result` | no transcript leaves a call unanswered | 3 |
| `test_big_result_present_but_truncated` | the fix truncates instead of dropping | 3 |
| `test_truncation_marker_included` | the cut is visible to the model | 3 |
| `test_regression_task_exists_and_is_well_formed` | the eval grew a guard | 3 |
| `test_regression_task_catches_the_replanted_bug` | the guard actually catches the bug class | 3 |

**Done means:** `uv run pytest` reports 10 passed.
Paste the output into the exam's score sheet.
