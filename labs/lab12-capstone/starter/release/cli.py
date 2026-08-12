"""Lab 12 — provided: print a release-gate report as a table.

Not reader work — this exercises `release_gate()` once you've implemented
it, so you can see the org-scale contract (Trace 27, Trace 33, Trace 34;
Chapter 13) render as a real go/no-go report a CI job could post.

Run:
    uv run python -m starter.release.cli                  # good candidate
    uv run python -m starter.release.cli --candidate bad   # planted regression
"""
from __future__ import annotations

import argparse

from worksheet_common import Model, ModelResponse

from provided.baseline_agent import run_task as baseline_fn
from provided.candidate_bad import run_task as candidate_bad_fn
from provided.candidate_good import run_task as candidate_good_fn
from provided.evalkit.graders import exact_grader, judge_grader, trajectory_grader
from provided.tasks import TASKS

from .gate import release_gate


class HeuristicJudge(Model):
    """A deterministic stand-in for a real judge model.

    Passes a transcript when the task's expected answer appears verbatim
    in the rendered transcript the judge prompt carries — a cheap, offline
    approximation of what a real LLM judge would conclude, good enough for
    this demo CLI (the lab's tests use an exact scripted judge instead).
    """

    def complete(self, messages: list[dict], tools: dict) -> ModelResponse:
        prompt = messages[-1]["content"]
        marker = "Expected answer: "
        start = prompt.index(marker) + len(marker)
        expected = prompt[start:prompt.index("\n", start)]
        transcript_part = prompt.split("Full transcript of the agent's run:\n", 1)[1]
        return ModelResponse(text="1" if expected in transcript_part else "0")


def _graders() -> dict:
    judge = HeuristicJudge()
    return {
        "exact": exact_grader,
        "trajectory": trajectory_grader,
        "judge": lambda transcript, task: judge_grader(transcript, task, judge),
    }


def _print_report(result: dict) -> None:
    print(f"{'task':<16} {'baseline':>10} {'candidate':>10}")
    for row in result["report"]:
        flag = " <-- regression" if row["id"] in result["regressions"] else ""
        print(f"{row['id']:<16} {row['baseline']:>10.2f} {row['candidate']:>10.2f}{flag}")
    print()
    print(f"baseline aggregate:  {result['baseline']:.3f}")
    print(f"candidate aggregate: {result['candidate']:.3f}")
    print(f"regressions:         {len(result['regressions'])}")
    print(f"verdict:             {result['verdict']}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the Lab 12 release gate.")
    parser.add_argument("--candidate", choices=["good", "bad"], default="good",
                         help="which candidate agent to gate (default: good)")
    args = parser.parse_args()

    candidate_fn = candidate_good_fn if args.candidate == "good" else candidate_bad_fn
    result = release_gate(baseline_fn, candidate_fn, TASKS, _graders())
    _print_report(result)
    return 0 if result["verdict"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
