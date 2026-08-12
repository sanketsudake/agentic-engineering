"""L2 practical checker: 10 checks × 3 points, self-scoring.

Run with `uv run pytest`. As shipped, most of these fail — that is the
exam. Done means all 10 pass WITHOUT editing this file,
`evalsuite/tasks.py`, `evalsuite/graders.py`, `evalsuite/runner.py`, or
`agent/buggy_reference.py`.
"""
from __future__ import annotations

import pytest

from agent import buggy_reference
from agent.loop import run_task
from agent.tools import FILES
from evalsuite.graders import default_graders
from evalsuite.runner import run_eval
from evalsuite.tasks import BIG_TASK_IDS, TASKS
from evalsuite.tasks_regression import REGRESSION_TASKS

CLEAN_TASK_IDS = {t["id"] for t in TASKS} - BIG_TASK_IDS


@pytest.fixture(scope="module")
def report():
    """One eval run over the 10 provided tasks, shared by the checks."""
    return run_eval(run_task, TASKS, default_graders())


# -- 6 checks: the eval suite passes after your fix ------------------------

def test_aggregate_clears_the_bar(report):
    """The suite's aggregate over all 10 tasks is at least 0.9."""
    assert report["aggregate"] >= 0.9


def test_build_log_task_passes(report):
    assert report["per_task"]["build-log-1"]["mean"] == 1.0


def test_deploy_log_task_passes(report):
    assert report["per_task"]["deploy-log-1"]["mean"] == 1.0


def test_latency_report_task_passes(report):
    assert report["per_task"]["latency-report-1"]["mean"] == 1.0


def test_no_clean_task_regressed(report):
    """The 7 tasks that passed before your change still pass after it."""
    for task_id in sorted(CLEAN_TASK_IDS):
        assert report["per_task"][task_id]["mean"] == 1.0, task_id


def test_every_tool_call_has_a_result(report):
    """Transcript-level: no task leaves a tool call without a result."""
    for task_id, scores in sorted(report["per_task"].items()):
        assert scores["paired"] == 1.0, task_id


# -- 2 checks: the fix is the right class ----------------------------------

def _big_tool_messages():
    """The tool-result messages from one run of the big build-log task."""
    task = next(t for t in TASKS if t["id"] == "build-log-1")
    result = run_task(task)
    return [m for m in result.transcript if m["role"] == "tool"]


def test_big_result_present_but_truncated():
    """The oversized result reaches the transcript, cut — not dropped,
    and not passed through whole."""
    tool_msgs = _big_tool_messages()
    assert tool_msgs, "the oversized tool result never reached the transcript"
    content = tool_msgs[0]["content"]
    assert content.startswith(FILES["logs/build.log"][:80]), \
        "the truncated result must keep the head of the real output"
    # Hardcoded on purpose: raising RESULT_BUDGET is not a fix.
    assert len(content) <= 500, "the result must be cut near the 400-char budget"


def test_truncation_marker_included():
    """The cut is explicit: the model must be able to see it happened."""
    tool_msgs = _big_tool_messages()
    assert tool_msgs, "the oversized tool result never reached the transcript"
    assert "truncated" in tool_msgs[0]["content"].lower(), \
        "include a marker containing the word 'truncated'"


# -- 2 checks: the regression task exists and catches a re-planted bug -----

REQUIRED_TASK_KEYS = ("id", "question", "script", "expected_answer", "required_tools")


def test_regression_task_exists_and_is_well_formed():
    assert REGRESSION_TASKS, "add at least one task to evalsuite/tasks_regression.py"
    for task in REGRESSION_TASKS:
        for key in REQUIRED_TASK_KEYS:
            assert key in task, f"regression task missing key {key!r}"


def test_regression_task_catches_the_replanted_bug():
    assert REGRESSION_TASKS, "add at least one task to evalsuite/tasks_regression.py"
    graders = default_graders()
    fixed = run_eval(run_task, REGRESSION_TASKS, graders)
    assert fixed["aggregate"] == 1.0, \
        "your fixed agent must pass your own regression task"
    try:
        buggy = run_eval(buggy_reference.run_task, REGRESSION_TASKS, graders)
    except AssertionError as exc:  # ScriptExhausted — forgot "cycle": True?
        pytest.fail(f"the regression task crashed the buggy reference instead "
                    f"of scoring it: {exc}")
    assert buggy["aggregate"] < 1.0, \
        "the frozen buggy agent must score below 1.0 on your regression task"
