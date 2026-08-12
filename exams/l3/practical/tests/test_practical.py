"""L3 practical checker: 10 checks × 3 points, self-scoring.

Run with `uv run pytest`. As shipped, all 10 fail — that is the exam.
Done means all 10 pass WITHOUT editing this file, `provided/`, or
`reference/`. Everything the checks assert is stated in the docstring of
`rollout/engine.py::next_action` — implement that spec, nothing more.
"""
from __future__ import annotations

import copy

import pytest

from provided.baseline_agent import run_task as baseline_run
from provided.candidate_bad import run_task as bad_run
from provided.candidate_good import run_task as good_run
from provided.evalkit.graders import exact_grader, trajectory_grader
from provided.evalkit.runner import run_eval
from provided.tasks import TASKS
from provided.telemetry import BASELINE_TELEMETRY, canary_ticks, telemetry_tick
from rollout.engine import next_action

GRADERS = {"exact": exact_grader, "trajectory": trajectory_grader}

POLICY = {
    "min_score": 0.8,
    "max_regression": 0.05,
    "max_error_rate_delta": 0.02,
    "max_cost_delta": 0.05,
    "required_clean_ticks": 3,
}

# The 6 tasks (of 10) the bad candidate regresses on — see provided/tasks.py.
ERROR_TASK_IDS = {
    "price-err-1", "price-err-2",
    "weather-err-1", "weather-err-2",
    "docs-err-1", "docs-err-2",
}


def _gate_state(candidate_run) -> dict:
    return {
        "stage": "GATE",
        "policy": dict(POLICY),
        "eval": {
            "baseline": run_eval(baseline_run, TASKS, GRADERS),
            "candidate": run_eval(candidate_run, TASKS, GRADERS),
        },
    }


def _canary_state(ticks: list[dict]) -> dict:
    return {
        "stage": "CANARY",
        "policy": dict(POLICY),
        "baseline_telemetry": dict(BASELINE_TELEMETRY),
        "canary_ticks": ticks,
    }


@pytest.fixture(scope="module")
def gate_state_good():
    """The GATE state for the harmless candidate: eval scores match baseline."""
    return _gate_state(good_run)


@pytest.fixture(scope="module")
def gate_state_bad():
    """The GATE state for the planted-regression candidate."""
    return _gate_state(bad_run)


# -- 2 checks: the eval gate ------------------------------------------------

def test_gate_passes_good_candidate_to_canary(gate_state_good):
    """A candidate whose eval matches baseline advances to the canary."""
    decision = next_action(gate_state_good)
    assert decision["next_stage"] == "CANARY"


def test_gate_blocks_bad_candidate_and_reason_lists_failing_tasks(gate_state_bad):
    """The regressing candidate is blocked, and the human reading the CI
    log sees exactly which tasks regressed."""
    decision = next_action(gate_state_bad)
    assert decision["next_stage"] == "BLOCK"
    for task_id in sorted(ERROR_TASK_IDS):
        assert task_id in decision["reason"], \
            f"the BLOCK reason must list regressed task {task_id!r}"


# -- 3 checks: the canary ---------------------------------------------------

def test_canary_advances_to_fleet_after_required_clean_ticks():
    """Fewer clean ticks than required holds the canary; hitting the
    requirement promotes to the fleet."""
    holding = next_action(_canary_state(canary_ticks("good", 2)))
    assert holding["next_stage"] == "CANARY"
    promoted = next_action(_canary_state(canary_ticks("good", 3)))
    assert promoted["next_stage"] == "FLEET"


def test_canary_rolls_back_on_error_rate_breach():
    """One tick with error_rate over baseline + max_error_rate_delta
    rolls the canary back, however clean the earlier ticks were."""
    ticks = canary_ticks("good", 2) + [telemetry_tick("bad", 2)]
    decision = next_action(_canary_state(ticks))
    assert decision["next_stage"] == "ROLLBACK"


def test_canary_rolls_back_on_cost_breach():
    """A cost overrun alone is a rollback — a canary that only watches
    errors ships a fleet-wide cost regression."""
    breach = {
        "error_rate": BASELINE_TELEMETRY["error_rate"],
        "cost_per_solve": (BASELINE_TELEMETRY["cost_per_solve"]
                           + POLICY["max_cost_delta"] + 0.01),
    }
    decision = next_action(_canary_state(canary_ticks("good", 2) + [breach]))
    assert decision["next_stage"] == "ROLLBACK"


# -- 2 checks: terminal stages ----------------------------------------------

def test_rollback_is_terminal():
    """A rolled-back rollout stays rolled back: no decision resurrects it."""
    decision = next_action({"stage": "ROLLBACK"})
    assert decision["next_stage"] == "ROLLBACK"


def test_fleet_is_terminal():
    """A completed rollout stays completed."""
    decision = next_action({"stage": "FLEET"})
    assert decision["next_stage"] == "FLEET"


# -- 3 checks: the engine is a CI contract ----------------------------------

def test_decisions_are_deterministic(gate_state_good, gate_state_bad):
    """The same state always yields the same decision — a gate that
    flickers cannot be a CI contract."""
    states = [gate_state_good, gate_state_bad,
              _canary_state(canary_ticks("good", 3)),
              _canary_state(canary_ticks("bad", 3))]
    for state in states:
        assert next_action(state) == next_action(state)


def test_state_is_not_mutated(gate_state_bad):
    """The engine reads the state; it never edits it — audits replay
    decisions from stored states."""
    states = [gate_state_bad, _canary_state(canary_ticks("bad", 3))]
    for state in states:
        before = copy.deepcopy(state)
        next_action(state)
        assert state == before


def test_reasons_are_human_readable(gate_state_good, gate_state_bad):
    """Every decision carries a non-empty reason string, and a rollback
    reason names the metric that broke."""
    for state in [gate_state_good, gate_state_bad,
                  _canary_state(canary_ticks("good", 2)),
                  _canary_state(canary_ticks("good", 3)),
                  {"stage": "FLEET"}, {"stage": "ROLLBACK"}, {"stage": "BLOCK"}]:
        reason = next_action(state)["reason"]
        assert isinstance(reason, str) and reason.strip(), \
            "every decision must carry a non-empty reason string"
    error_breach = next_action(_canary_state(canary_ticks("bad", 1)))
    assert "error_rate" in error_breach["reason"], \
        "an error_rate rollback must name error_rate"
    cost_tick = {"error_rate": BASELINE_TELEMETRY["error_rate"],
                 "cost_per_solve": BASELINE_TELEMETRY["cost_per_solve"] + 0.10}
    cost_breach = next_action(_canary_state([cost_tick]))
    assert "cost_per_solve" in cost_breach["reason"], \
        "a cost_per_solve rollback must name cost_per_solve"
