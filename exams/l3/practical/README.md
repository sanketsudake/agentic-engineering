# L3 Practical — Gate and stage the rollout

**Section C of the L3 exam** · 30 points · ~90 min · open-repo · offline, no API keys.

A candidate agent change wants to replace the baseline running on a fleet.
Nothing reaches the fleet on vibes:
the change must pass an eval gate, survive a canary, and only then promote —
with a block or rollback exit at each stage, and a reason a human can read in the CI log
(Trace 33, Trace 34; Chapter 12, Chapter 13).
Everything is provided except the decision function. You implement it.

## Setup

```bash
uv sync
uv run pytest        # as shipped: 10 red — that is the exam
```

## What is provided (do not edit)

- `provided/` — vendored from Lab 12: the baseline agent, a harmless
  candidate, a regressing candidate, the 10 eval tasks, and the evalkit
  (graders + runner) the gate's eval reports come from.
- `provided/telemetry.py` — deterministic canary telemetry:
  `error_rate` and `cost_per_solve` ticks for a `"good"` or `"bad"`
  candidate, a pure function of its arguments.
- `tests/` and `reference/` — the checker and maintainer plumbing.

## Your task

Implement `next_action(state) -> decision` in `rollout/engine.py`.
Its docstring is the full contract — the stage machine
(GATE → CANARY → FLEET, with BLOCK and ROLLBACK exits),
the exact pass/breach boundaries, the decision shape,
and what every reason string must contain.
The 10 checks assert nothing that is not stated there.
Your changes go in `rollout/engine.py` only.

Design pressure to respect: the engine is a CI contract.
It runs nothing, calls no model, reads no clock —
it maps an assembled state to one decision, deterministically,
without mutating the state, and it explains itself.
An engine that cannot say *why* it blocked a release
is a gate no team will trust (Chapter 13).

## Scoring — 10 checks × 3 points

Self-scoring, no judgment needed: `uv run pytest`, 3 points per passing check.

| Checks | What they verify | Points |
|---|---|---|
| `test_gate_passes_good_candidate_to_canary` | a clean candidate advances | 3 |
| `test_gate_blocks_bad_candidate_and_reason_lists_failing_tasks` | a regression blocks, named per task | 3 |
| `test_canary_advances_to_fleet_after_required_clean_ticks` | hold below N clean ticks, promote at N | 3 |
| `test_canary_rolls_back_on_error_rate_breach` | the error bound is live | 3 |
| `test_canary_rolls_back_on_cost_breach` | the cost bound is live | 3 |
| `test_rollback_is_terminal` | nothing resurrects a rollback | 3 |
| `test_fleet_is_terminal` | nothing re-runs a finished rollout | 3 |
| `test_decisions_are_deterministic` | same state, same decision | 3 |
| `test_state_is_not_mutated` | the engine reads, never edits | 3 |
| `test_reasons_are_human_readable` | every decision names its numbers | 3 |

**Done means:** `uv run pytest` reports 10 passed.
Paste the output into the exam's score sheet.
