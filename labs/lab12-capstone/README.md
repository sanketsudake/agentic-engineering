# Lab 12 — Capstone: eval-gated release

**Goal:** wire an agent and an eval into a release gate that blocks a
regressing change,
before the change ships.

**Level:** L3 · **Stack:** plain Python · **Time:** ~90 min

**Offline mode (default, no keys):**

```bash
uv sync
uv run pytest                      # 6 red tests are your task list
```

**Reference check:**

```bash
LAB_TARGET=solution uv run pytest  # the reference implementation passing
```

**See the gate run for real (after `starter/release/gate.py` is green):**

```bash
uv run python -m starter.release.cli                   # a harmless candidate: PASS
uv run python -m starter.release.cli --candidate bad    # a planted regression: BLOCK
```

## Your task

1. Read `provided/` (all of it, provided and identical in starter and
   solution). It vendors two labs you already built:
   - `provided/baseline_agent.py` — Lab 3's tool loop, adapted to Lab 8's
     tasks. This is the agent already running in production.
   - `provided/candidate_good.py` — the same loop with one harmless
     change: a more detailed tool-error message. No eval score should move.
   - `provided/candidate_bad.py` — the same loop with Lab 8's planted
     regression: a tool exception becomes silence instead of an error.
   - `provided/tasks.py` — Lab 8's 10 tasks, unchanged.
   - `provided/evalkit/` — Lab 8's solution graders and runner. You wrote
     these in Lab 8; here they are infrastructure, not the exercise.
2. Open `starter/release/gate.py`. The docstring on `release_gate()` is
   the full spec: run the eval on baseline and candidate, compare
   aggregates and per-task scores, decide `"PASS"` or `"BLOCK"`.
3. Make the 6 tests in `tests/test_lab.py` pass.
4. Run the CLI (`starter/release/cli.py`, provided — no work needed there)
   against both candidates and read the two reports.

**Done means:** `uv run pytest` is fully green against `starter/`.

## What this proves

No agent change ships on vibes.
A prompt tweak, a model upgrade, a "harmless" error-message change — every
one of them is a diff that can move behavior in ways a manual read of the
diff will not catch (Trace 33, Trace 34).
The gate is the org-scale contract: the same bar, mechanically applied, to
every change, for every team.
It does not replace judgment — someone still decides what the tasks and
the `min_score` and `max_regression` bars should be — but it replaces
"looks fine to me" with a number two people can agree on (Chapter 13).

`release_gate()` is small on purpose: it is Lab 8's `run_eval()` called
twice and a comparison.
That is the point.
The hard work — writing tasks that actually exercise the failure you care
about, writing graders that actually catch it (Trace 27) — is Lab 8's
work, done once and reused by every gate that calls it.
A capstone that reimplemented the eval would be missing the lesson: the
gate is infrastructure that composes, not a new thing to build from
scratch each time.

There is no live mode for this lab on purpose: the scripted model and the
scripted judge model both need to behave deterministically for `PASS` and
`BLOCK` to mean the same thing on every run — the entire point of a gate a
CI job can trust.
