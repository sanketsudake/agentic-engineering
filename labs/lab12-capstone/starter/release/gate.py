"""Lab 12 — your task: gate a release on eval scores (Trace 27, Trace 33,
Trace 34; Chapter 13).

This composes Lab 3's agent and Lab 8's eval: `provided/baseline_agent.py`
and `provided/candidate_*.py` are the agents under test; `provided/tasks.py`
and `provided/evalkit/` are the eval you built in Lab 8. Your job is the
piece neither lab built: the decision. Given two eval runs, should this
candidate ship?
"""
from __future__ import annotations

from typing import Callable


def release_gate(
    baseline_fn: Callable[[dict], object],
    candidate_fn: Callable[[dict], object],
    tasks: list[dict],
    graders: dict[str, Callable[[list[dict], dict], float]],
    min_score: float = 0.8,
    max_regression: float = 0.05,
) -> dict:
    """Run the eval on baseline and candidate, decide PASS or BLOCK.

    `baseline_fn` and `candidate_fn` each follow `run_eval`'s `agent_fn`
    contract: `agent_fn(task) -> AgentResult`, an object with a
    `.transcript` attribute (see `provided/baseline_agent.py`). Use
    `provided.evalkit.runner.run_eval` to score each one over the same
    `tasks` and the same `graders` — a task-ordering or grader mismatch
    between the two runs would make the comparison meaningless. Evaluate
    `baseline_fn` before `candidate_fn`: a grader can be stateful (a
    scripted judge model consumes its script in call order), so the order
    of the two `run_eval` calls is part of this function's contract, not an
    implementation detail.

    Verdict is "PASS" only if BOTH hold:
      - candidate aggregate >= min_score
      - candidate aggregate >= baseline aggregate - max_regression
        (the comparison is inclusive: sitting exactly on the boundary PASSes)

    Otherwise "BLOCK". `release_gate` is deterministic (same inputs, same
    output) and never raises because an agent or a grader scored badly — a
    bad score is data for the report, not a crash.

    Returns:
        {
          "verdict": "PASS" | "BLOCK",
          "baseline": <float>,     # baseline aggregate, from run_eval
          "candidate": <float>,    # candidate aggregate, from run_eval
          "regressions": [task_id, ...],
              # every task where the candidate's per-task mean score is
              # strictly lower than the baseline's per-task mean score on
              # that same task (run_eval's per_task[task_id]["mean"])
          "report": [
              {"id": task_id, "baseline": <float>, "candidate": <float>},
              ...  # one row per task, in `tasks` order
          ],
        }
    """
    raise NotImplementedError(
        "run the eval on baseline_fn and candidate_fn, compare aggregates "
        "and per-task scores, decide PASS or BLOCK")
