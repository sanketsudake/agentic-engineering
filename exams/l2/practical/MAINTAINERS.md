# MAINTAINERS — L2 practical reference notes

Maintainer-only.
Candidates: reading this file before finishing is scoring against the key mid-exam —
close it and go read the transcripts.

## The planted state

The repo ships in the BUGGY state on purpose:
`agent/loop.py` drops any tool result larger than `RESULT_BUDGET`
(`continue` instead of truncate),
so the model never sees the result of a big read and re-asks until `max_turns`.
Three eval tasks (`build-log-1`, `deploy-log-1`, `latency-report-1`) fail because of it,
and `evalsuite/tasks_regression.py` ships with an empty `REGRESSION_TASKS`.

Shipped pytest state: 9 failed, 1 passed (`test_no_clean_task_regressed`).

## The two reference edits (the candidate's job)

**Edit 1 — `agent/loop.py`:** replace

```python
            if len(content) > RESULT_BUDGET:
                continue  # skip oversized results to keep the window small
```

with

```python
            if len(content) > RESULT_BUDGET:
                content = (content[:RESULT_BUDGET]
                           + "\n[truncated: result exceeded 400 characters]")
```

**Edit 2 — `evalsuite/tasks_regression.py`:** replace the empty list with

```python
REGRESSION_TASKS: list[dict] = [
    {
        "id": "regress-big-result-1",
        "question": "Why was the last deploy rolled back?",
        "script": [
            ModelResponse(tool_calls=[ToolCall("t1", "read_file",
                                               {"path": "logs/deploy.log"})]),
            reactive_entry(
                on_result=ModelResponse(
                    text="The deploy rolled back: the healthcheck timed out after 300s."),
                on_missing=ModelResponse(
                    tool_calls=[ToolCall("t2", "read_file",
                                         {"path": "logs/deploy.log"})]),
            ),
        ],
        "cycle": True,
        "expected_answer": "The deploy rolled back: the healthcheck timed out after 300s.",
        "required_tools": ["read_file"],
    },
]
```

With both edits applied: 10 passed.

## Re-verifying both states

```bash
cd exams/l2/practical
uv sync
uv run pytest            # shipped: 9 failed, 1 passed
# apply the two edits above
uv run pytest            # fixed: 10 passed
# revert both edits exactly; leave the repo in the shipped (buggy) state
uv run pytest            # back to 9 failed, 1 passed
rm -rf transcripts/      # if evalsuite.run was executed
```

`build/check_book.py` (repo root) checks the exam's
"10 checks × 3 points" line against the test count in `tests/test_practical.py` —
keep exactly 10 `def test_` functions in that one file.

## CI verification (reference/ + LAB_TARGET)

`reference/` carries the two edits as importable modules
(`loop_fixed.py`, `tasks_regression_ref.py`).
`tests/conftest.py` aliases them over the shipped modules when
`LAB_TARGET=solution`, so the labs CI workflow proves the practical is
completable without shipping the answers in the candidate's path.
Keep `reference/` in sync with the edits above.
