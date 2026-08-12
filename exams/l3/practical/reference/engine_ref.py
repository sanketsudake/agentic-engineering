"""Maintainer reference implementation of `rollout/engine.py`.

Candidates never import this; `tests/conftest.py` aliases it over
`rollout.engine` only when LAB_TARGET=solution, so CI can prove the
practical is completable. Keep it in sync with the docstring spec in
`rollout/engine.py` and with MAINTAINERS.md.
"""
from __future__ import annotations

STAGES = ("GATE", "CANARY", "FLEET", "ROLLBACK", "BLOCK")

_TERMINAL = ("FLEET", "ROLLBACK", "BLOCK")


def _gate(state: dict) -> dict:
    policy = state["policy"]
    base = state["eval"]["baseline"]
    cand = state["eval"]["candidate"]
    base_agg, cand_agg = base["aggregate"], cand["aggregate"]
    if (cand_agg >= policy["min_score"]
            and cand_agg >= base_agg - policy["max_regression"]):
        return {"next_stage": "CANARY",
                "reason": (f"gate passed: candidate aggregate {cand_agg:.2f} meets "
                           f"min_score {policy['min_score']:.2f} and is within "
                           f"max_regression {policy['max_regression']:.2f} of "
                           f"baseline aggregate {base_agg:.2f}")}
    regressed = sorted(
        task_id for task_id, scores in cand["per_task"].items()
        if scores["mean"] < base["per_task"][task_id]["mean"] - policy["max_regression"])
    return {"next_stage": "BLOCK",
            "reason": (f"gate blocked: candidate aggregate {cand_agg:.2f} vs baseline "
                       f"{base_agg:.2f} (min_score {policy['min_score']:.2f}, "
                       f"max_regression {policy['max_regression']:.2f}); regressed "
                       f"tasks: {', '.join(regressed) if regressed else 'none'}")}


def _canary(state: dict) -> dict:
    policy = state["policy"]
    baseline = state["baseline_telemetry"]
    ticks = state["canary_ticks"]
    bounds = (("error_rate", "max_error_rate_delta"),
              ("cost_per_solve", "max_cost_delta"))
    for i, tick in enumerate(ticks):
        for metric, delta_key in bounds:
            allowed = baseline[metric] + policy[delta_key]
            if tick[metric] > allowed:
                return {"next_stage": "ROLLBACK",
                        "reason": (f"canary tick {i} breached {metric}: observed "
                                   f"{tick[metric]:.4f}, allowed at most {allowed:.4f} "
                                   f"(baseline {baseline[metric]:.4f} + "
                                   f"{delta_key} {policy[delta_key]:.4f})")}
    required = policy["required_clean_ticks"]
    if len(ticks) >= required:
        return {"next_stage": "FLEET",
                "reason": (f"canary clean: {len(ticks)} ticks within bounds, "
                           f"required_clean_ticks {required} met — promote to fleet")}
    return {"next_stage": "CANARY",
            "reason": (f"canary holding: {len(ticks)} of {required} required "
                       f"clean ticks observed, all within bounds")}


def next_action(state: dict) -> dict:
    """Reference `next_action()` — see the spec in `rollout/engine.py`."""
    stage = state["stage"]
    if stage in _TERMINAL:
        return {"next_stage": stage,
                "reason": f"{stage} is terminal: the rollout is finished here"}
    if stage == "GATE":
        return _gate(state)
    if stage == "CANARY":
        return _canary(state)
    raise ValueError(f"unknown rollout stage: {stage!r}")
