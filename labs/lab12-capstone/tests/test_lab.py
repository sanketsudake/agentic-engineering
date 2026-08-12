"""Lab 12 checker: 6 tests define "done".

They run against starter/ by default (your task list) and against
solution/ with LAB_TARGET=solution (the reference passing). `provided/` —
the vendored Lab 3 agent, the Lab 8 tasks, and Lab 8's solution evalkit —
is identical either way: infrastructure here, not the exercise.
"""
from types import SimpleNamespace

import pytest
from worksheet_common import ModelResponse, ScriptedModel

# The 6 tasks (of 10) whose script plants a tool error — see provided/tasks.py.
ERROR_TASK_IDS = {
    "price-err-1", "price-err-2",
    "weather-err-1", "weather-err-2",
    "docs-err-1", "docs-err-2",
}


def _graders_for(judge_model, graders):
    return {
        "exact": graders.exact_grader,
        "trajectory": graders.trajectory_grader,
        "judge": lambda transcript, task: graders.judge_grader(transcript, task, judge_model),
    }


def _release_graders(tasks, graders, baseline_correct_ids, candidate_correct_ids):
    """Build a graders dict (exact + trajectory + a scripted judge) for one
    `release_gate()` call.

    `release_gate` evaluates baseline_fn before candidate_fn, so the
    judge's script lists baseline verdicts first, then candidate verdicts,
    each block in task order — one `ScriptedModel` covers both `run_eval`
    calls a single `release_gate()` call makes.
    """
    task_ids = [t["id"] for t in tasks]
    script = [ModelResponse(text="1" if tid in baseline_correct_ids else "0")
              for tid in task_ids]
    script += [ModelResponse(text="1" if tid in candidate_correct_ids else "0")
               for tid in task_ids]
    judge = ScriptedModel(script)
    return _graders_for(judge, graders)


def test_good_candidate_passes_with_no_regressions(
        gate, tasks, graders, baseline_agent, candidate_good):
    """A harmless candidate change: PASS, and nothing regressed."""
    task_ids = {t["id"] for t in tasks}
    g = _release_graders(tasks, graders, baseline_correct_ids=task_ids,
                          candidate_correct_ids=task_ids)
    result = gate.release_gate(baseline_agent, candidate_good, tasks, g)
    assert result["verdict"] == "PASS"
    assert result["regressions"] == []
    assert result["candidate"] >= 0.8


def test_bad_candidate_blocks_and_lists_failing_tasks(
        gate, tasks, graders, baseline_agent, candidate_bad):
    """The planted-bug candidate: BLOCK, and the regressions are exactly
    the tasks whose tool call silently failed."""
    task_ids = {t["id"] for t in tasks}
    g = _release_graders(tasks, graders, baseline_correct_ids=task_ids,
                          candidate_correct_ids=task_ids - ERROR_TASK_IDS)
    result = gate.release_gate(baseline_agent, candidate_bad, tasks, g)
    assert result["verdict"] == "BLOCK"
    assert set(result["regressions"]) == ERROR_TASK_IDS
    assert result["candidate"] <= 0.5


def test_min_score_enforced_even_when_baseline_is_bad(
        gate, tasks, graders, candidate_bad):
    """A weakened baseline does not lower the bar: if the candidate is no
    better than a bad baseline, it still misses `min_score` and BLOCKs,
    even with zero per-task regressions."""
    task_ids = {t["id"] for t in tasks}
    correct_ids = task_ids - ERROR_TASK_IDS
    g = _release_graders(tasks, graders, baseline_correct_ids=correct_ids,
                          candidate_correct_ids=correct_ids)
    # candidate_bad is both the (deliberately weak) baseline and the candidate.
    result = gate.release_gate(candidate_bad, candidate_bad, tasks, g)
    assert result["regressions"] == []          # no worse than its own baseline
    assert result["candidate"] < 0.8             # but below min_score's default
    assert result["verdict"] == "BLOCK"


def test_max_regression_boundary_is_inclusive(gate):
    """Sitting exactly `max_regression` below baseline PASSes; one step
    further BLOCKs. Uses a custom grader/agent stub with exact binary
    fractions so the boundary comparison carries no float rounding risk."""
    stub_tasks = [{"id": "a"}, {"id": "b"}]

    def make_agent(scores):
        def agent_fn(task):
            return SimpleNamespace(transcript=[{"score": scores[task["id"]]}])
        return agent_fn

    def score_grader(transcript, task):
        return transcript[0]["score"]

    graders = {"score": score_grader}
    baseline_fn = make_agent({"a": 1.0, "b": 1.0})       # aggregate 1.0

    at_edge_fn = make_agent({"a": 0.75, "b": 0.75})      # aggregate 0.75, exactly
    result = gate.release_gate(baseline_fn, at_edge_fn, stub_tasks, graders,
                                min_score=0.0, max_regression=0.25)
    assert result["verdict"] == "PASS"

    past_edge_fn = make_agent({"a": 0.5, "b": 0.5})      # aggregate 0.5, past the edge
    result = gate.release_gate(baseline_fn, past_edge_fn, stub_tasks, graders,
                                min_score=0.0, max_regression=0.25)
    assert result["verdict"] == "BLOCK"


def test_report_rows_carry_task_ids_and_both_scores(gate):
    """Every report row names its task and both eval numbers, so a human
    (or a CI log) can see exactly what moved, not just the aggregate."""
    stub_tasks = [{"id": "x"}, {"id": "y"}]

    def agent_fn(scores):
        def run(task):
            return SimpleNamespace(transcript=[{"score": scores[task["id"]]}])
        return run

    def score_grader(transcript, task):
        return transcript[0]["score"]

    result = gate.release_gate(
        agent_fn({"x": 1.0, "y": 0.4}), agent_fn({"x": 1.0, "y": 0.1}),
        stub_tasks, {"score": score_grader}, min_score=0.0, max_regression=1.0)

    assert {row["id"] for row in result["report"]} == {"x", "y"}
    by_id = {row["id"]: row for row in result["report"]}
    assert by_id["x"]["baseline"] == 1.0 and by_id["x"]["candidate"] == 1.0
    assert by_id["y"]["baseline"] == pytest.approx(0.4)
    assert by_id["y"]["candidate"] == pytest.approx(0.1)


def test_release_gate_is_deterministic(gate, tasks, graders, baseline_agent, candidate_good):
    """Two runs over the same inputs produce the same report — a gate that
    is not deterministic cannot be a CI contract."""
    stateless_graders = {
        "exact": graders.exact_grader,
        "trajectory": graders.trajectory_grader,
    }
    first = gate.release_gate(baseline_agent, candidate_good, tasks, stateless_graders)
    second = gate.release_gate(baseline_agent, candidate_good, tasks, stateless_graders)
    assert first == second
