"""The staged-rollout engine: one pure decision function.

This is the only file you edit. The docstring on `next_action()` is the
full contract; the 10 tests in `tests/test_practical.py` check nothing
that is not stated here.

The rollout is a state machine (Chapter 12's staged upgrades, Chapter 13's
eval-gated rollout, Trace 33, Trace 34):

    GATE -> CANARY -> FLEET        the happy path
    GATE -> BLOCK                  the eval gate refuses the candidate
    CANARY -> ROLLBACK             live telemetry breaks a bound

`FLEET`, `ROLLBACK`, and `BLOCK` are terminal. The engine never runs
anything itself — it reads the state a harness assembled and returns one
decision. That is what makes it a CI contract: deterministic, auditable,
and explainable to the human reading the log.
"""
from __future__ import annotations

STAGES = ("GATE", "CANARY", "FLEET", "ROLLBACK", "BLOCK")


def next_action(state: dict) -> dict:
    """Decide the next rollout step from `state`. Pure and read-only.

    Returns a decision dict with exactly two keys:

        {"next_stage": <one of STAGES>, "reason": <non-empty str>}

    `reason` is for the human reading the CI log: a plain-English sentence
    that names the numbers and metrics that drove the decision. An empty
    or generic reason ("blocked") fails the contract.

    `state` always carries:

    - `state["stage"]`: one of `STAGES` — the stage the rollout is in now.
    - `state["policy"]`: the rollout policy —
        `min_score` (float): minimum candidate eval aggregate,
        `max_regression` (float): largest tolerated eval-score drop,
        `max_error_rate_delta` (float): largest tolerated canary
            `error_rate` rise over baseline,
        `max_cost_delta` (float): largest tolerated canary
            `cost_per_solve` rise over baseline,
        `required_clean_ticks` (int): canary ticks that must all be
            within bounds before the fleet stage.
      (Terminal stages may omit `policy`; do not read it before the
      terminal check.)

    Stage rules:

    **GATE** — `state["eval"]` holds two `run_eval()` reports (see
    `provided/evalkit/runner.py`): `state["eval"]["baseline"]` and
    `state["eval"]["candidate"]`, each shaped
    `{"per_task": {task_id: {..., "mean": float}}, "aggregate": float}`.
    The candidate passes the gate iff BOTH hold (>= means exactly-at-bar
    passes):
        candidate aggregate >= policy["min_score"]
        candidate aggregate >= baseline aggregate - policy["max_regression"]
    Pass -> `{"next_stage": "CANARY", ...}`; the reason cites both
    aggregates. Fail -> `{"next_stage": "BLOCK", ...}`; the reason cites
    both aggregates AND lists, sorted and comma-separated, every regressed
    task id — a task regressed when its candidate per-task mean is below
    its baseline per-task mean by more than `max_regression`.

    **CANARY** — `state["baseline_telemetry"]` holds the fleet baseline
    (`{"error_rate": float, "cost_per_solve": float}`) and
    `state["canary_ticks"]` the observations so far, oldest first, each
    the same shape (see `provided/telemetry.py`). Scan the ticks in
    order; within a tick check `error_rate` first, then `cost_per_solve`.
    A metric breaches when its value is STRICTLY greater than
    `baseline + its policy delta` (exactly at the bound is clean):
        tick["error_rate"]     > baseline["error_rate"] + max_error_rate_delta
        tick["cost_per_solve"] > baseline["cost_per_solve"] + max_cost_delta
    First breach found -> `{"next_stage": "ROLLBACK", ...}`; the reason
    names the breached metric (the literal string "error_rate" or
    "cost_per_solve"), the observed value, and the allowed bound. No
    breach and `len(canary_ticks) >= required_clean_ticks` ->
    `{"next_stage": "FLEET", ...}`. No breach but fewer ticks ->
    `{"next_stage": "CANARY", ...}` (hold and keep watching); the reason
    counts clean ticks so far against the requirement.

    **FLEET / ROLLBACK / BLOCK** — terminal: return the same stage back,
    with a reason saying the rollout is finished there. Read nothing else
    from the state.

    Any other `state["stage"]` raises `ValueError`.

    Purity contract: the same `state` always yields an equal decision
    (no randomness, no clock, no I/O), and `state` is never mutated —
    the harness replays decisions from stored states during audits.
    """
    raise NotImplementedError("Section C: implement next_action() per this docstring")
