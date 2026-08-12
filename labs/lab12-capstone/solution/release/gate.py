"""Reference solution for Lab 12: the eval-gated release decision
(Trace 27, Trace 33, Trace 34; Chapter 13)."""
from __future__ import annotations

from typing import Callable

from provided.evalkit.runner import run_eval


def release_gate(
    baseline_fn: Callable[[dict], object],
    candidate_fn: Callable[[dict], object],
    tasks: list[dict],
    graders: dict[str, Callable[[list[dict], dict], float]],
    min_score: float = 0.8,
    max_regression: float = 0.05,
) -> dict:
    """Run the eval on baseline and candidate, decide PASS or BLOCK.

    See the starter docstring for the full contract. Baseline is evaluated
    before candidate so a stateful grader (e.g. a scripted judge model)
    sees the two runs in a predictable order.
    """
    baseline_report = run_eval(baseline_fn, tasks, graders)
    candidate_report = run_eval(candidate_fn, tasks, graders)

    report = []
    regressions = []
    for task in tasks:
        task_id = task["id"]
        baseline_score = baseline_report["per_task"][task_id]["mean"]
        candidate_score = candidate_report["per_task"][task_id]["mean"]
        report.append({
            "id": task_id,
            "baseline": baseline_score,
            "candidate": candidate_score,
        })
        if candidate_score < baseline_score:
            regressions.append(task_id)

    baseline_aggregate = baseline_report["aggregate"]
    candidate_aggregate = candidate_report["aggregate"]
    verdict = "PASS" if (
        candidate_aggregate >= min_score
        and candidate_aggregate >= baseline_aggregate - max_regression
    ) else "BLOCK"

    return {
        "verdict": verdict,
        "baseline": baseline_aggregate,
        "candidate": candidate_aggregate,
        "regressions": regressions,
        "report": report,
    }
