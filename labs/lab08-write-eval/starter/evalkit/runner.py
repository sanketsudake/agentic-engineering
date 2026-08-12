"""Lab 8 — your task: run every task through an agent and grade it."""
from __future__ import annotations

from typing import Callable


def run_eval(agent_fn: Callable[[dict], object], tasks: list[dict],
             graders: dict[str, Callable[[list[dict], dict], float]]) -> dict:
    """Run every task, score it with every grader, aggregate.

    `agent_fn(task) -> AgentResult` — an object with a `.transcript`
    attribute (see `agents_under_test/good_agent.py`).
    `graders` maps a name to a `(transcript, task) -> float` callable. Bind
    extra arguments a grader needs (e.g. `judge_grader`'s `judge_model`)
    with a closure before putting it in this dict — `run_eval` calls every
    grader as `grader(transcript, task)`.

    Returns a report:
        {"per_task": {task_id: {grader_name: score, ..., "mean": <float>}},
         "aggregate": <float>}  # mean over tasks of each task's mean
    """
    raise NotImplementedError("run agent_fn over tasks, score with graders, aggregate")
