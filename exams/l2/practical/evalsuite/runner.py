"""Provided runner (Lab 8's shape). Working — do not edit."""
from __future__ import annotations

from typing import Callable


def run_eval(agent_fn: Callable[[dict], object], tasks: list[dict],
             graders: dict[str, Callable[[list[dict], dict], float]]) -> dict:
    """Run every task, score it with every grader, aggregate.

    `agent_fn(task) -> AgentResult` — an object with a `.transcript`
    attribute (see `agent/loop.py`).
    `graders` maps a name to a `(transcript, task) -> float` callable.

    Returns a report:
        {"per_task": {task_id: {grader_name: score, ..., "mean": <float>}},
         "aggregate": <float>}  # mean over tasks of each task's mean
    """
    per_task: dict[str, dict[str, float]] = {}
    task_means: list[float] = []
    for task in tasks:
        result = agent_fn(task)
        scores = {name: float(grader(result.transcript, task))
                  for name, grader in graders.items()}
        mean = sum(scores.values()) / len(scores) if scores else 0.0
        per_task[task["id"]] = {**scores, "mean": mean}
        task_means.append(mean)
    aggregate = sum(task_means) / len(task_means) if task_means else 0.0
    return {"per_task": per_task, "aggregate": aggregate}
