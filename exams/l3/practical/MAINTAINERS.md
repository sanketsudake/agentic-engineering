# MAINTAINERS — L3 practical reference notes

Maintainer-only.
Candidates: reading this file before finishing is scoring against the key mid-exam —
close it and go read the docstring in `rollout/engine.py`.

## The shipped state

The repo ships RED on purpose:
`rollout/engine.py::next_action()` raises `NotImplementedError`,
so all 10 checks fail until the candidate implements the docstring spec.
Everything else — `provided/` (vendored from `labs/lab12-capstone/provided/`,
plus the new `telemetry.py`), `tests/`, `reference/` — is final infrastructure.

Shipped pytest state: 10 failed, 0 passed.

## The reference (the candidate's job)

The complete reference implementation lives in `reference/engine_ref.py`:
a terminal-stage check first (`FLEET`/`ROLLBACK`/`BLOCK` return themselves),
then the GATE comparison (candidate aggregate vs `min_score` and vs
baseline − `max_regression`, with the sorted regressed-task list in the
BLOCK reason), then the CANARY scan (ticks oldest first, `error_rate`
before `cost_per_solve`, strict `>` against baseline + delta), and
`ValueError` on an unknown stage.
A candidate solution is equivalent to pasting that module's logic into
`rollout/engine.py` under the shipped docstring.

## CI verification (reference/ + LAB_TARGET)

`tests/conftest.py` aliases `reference.engine_ref` over `rollout.engine`
when `LAB_TARGET=solution`, so CI proves the practical is completable
without shipping the answer in the candidate's path.
Keep `reference/engine_ref.py` in sync with the docstring spec in
`rollout/engine.py` — the tests assert nothing the docstring does not state.

## Re-verifying both states

```bash
cd exams/l3/practical
uv sync
uv run pytest                        # shipped: 10 failed
LAB_TARGET=solution uv run pytest    # reference: 10 passed
```

Leave the repo in the shipped (red) state.

`build/check_book.py` (repo root) checks the exam's
"10 checks × 3 points" line against the test count in `tests/test_practical.py` —
keep exactly 10 `def test_` functions in that one file.
