"""Run the eval suite against the agent and print the report.

    uv run python -m evalsuite.run

Writes the transcript of every non-perfect task to `transcripts/<id>.json`
— that is where your diagnosis starts.
"""
from __future__ import annotations

import json
import os

from agent.loop import run_task
from evalsuite.graders import default_graders
from evalsuite.tasks import TASKS
from evalsuite.tasks_regression import REGRESSION_TASKS


def main() -> None:
    graders = default_graders()
    os.makedirs("transcripts", exist_ok=True)
    task_means: list[float] = []
    for task in TASKS + REGRESSION_TASKS:
        result = run_task(task)
        scores = {name: grader(result.transcript, task)
                  for name, grader in graders.items()}
        mean = sum(scores.values()) / len(scores)
        task_means.append(mean)
        flag = "PASS" if mean == 1.0 else "FAIL"
        cells = "  ".join(f"{name}={score:.1f}" for name, score in scores.items())
        print(f"{flag}  {task['id']:<18} {cells}")
        if mean < 1.0:
            path = os.path.join("transcripts", f"{task['id']}.json")
            with open(path, "w") as fh:
                json.dump({"task": task["id"], "question": task["question"],
                           "stopped": result.stopped, "answer": result.answer,
                           "transcript": result.transcript}, fh, indent=2)
            print(f"      transcript -> {path}")
    aggregate = sum(task_means) / len(task_means)
    print(f"\naggregate: {aggregate:.2f} over {len(task_means)} tasks")


if __name__ == "__main__":
    main()
