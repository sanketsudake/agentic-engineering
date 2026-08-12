"""Deterministic canary telemetry for the rollout engine.

A real canary reads `error_rate` and `cost_per_solve` off the telemetry
sink (Chapter 12). Here the sink is scripted so the exam is offline and
every run sees the same numbers: `telemetry_tick()` is a pure function of
its arguments — no clock, no randomness.

Two candidate profiles exist:

- `"good"` — matches `BASELINE_TELEMETRY`, plus a tiny deterministic
  wobble (+0.001 on odd ticks) that stays inside every sane bound. A
  canary policy that rolls this back is too tight.
- `"bad"` — `error_rate` is 3x baseline (0.06 vs 0.02): a real breach on
  any sane `max_error_rate_delta`. Its `cost_per_solve` stays in bounds
  on purpose, so `error_rate` is the metric a rollback reason must name.

Neither profile breaches on cost. A test that needs a cost breach builds
its tick by hand from `BASELINE_TELEMETRY` (see `tests/test_practical.py`).
"""
from __future__ import annotations

BASELINE_TELEMETRY = {"error_rate": 0.02, "cost_per_solve": 0.20}

_PROFILES = {
    "good": {"error_rate": 0.02, "cost_per_solve": 0.20},
    "bad": {"error_rate": 0.06, "cost_per_solve": 0.20},
}


def telemetry_tick(candidate: str, tick: int) -> dict:
    """One canary observation for `candidate` ("good" | "bad") at `tick`."""
    profile = _PROFILES[candidate]
    wobble = 0.001 * (tick % 2)
    return {"error_rate": round(profile["error_rate"] + wobble, 6),
            "cost_per_solve": round(profile["cost_per_solve"] + wobble, 6)}


def canary_ticks(candidate: str, n: int) -> list[dict]:
    """The first `n` canary observations for `candidate`, oldest first."""
    return [telemetry_tick(candidate, i) for i in range(n)]
