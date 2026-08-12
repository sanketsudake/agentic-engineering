# L3 Exam — The Architect

This exam verifies: you can commit to defensible positions and design org-scale agentic systems.
Score yourself against `exams/l3/key.md` after finishing — not before.

**Time:** 3 hours (Section A closed-book, 60 min; Sections B–C open-repo, 120 min).
**Materials:** Section A: nothing. Sections B–C: this repo, no live model access needed.
**Total:** 100 points
**Pass:** at least 70 points overall AND at least 18/30 on Section B.

## Section A — Written (40 points)

**E3.A1 (10 pts) — Choose between a hard token cap for each subagent and one shared budget for the whole job.**

Your orchestrator splits a nightly research job across five subagents (Trace 24).
One platform engineer proposes a hard token cap for each subagent.
Another proposes one shared budget for the whole job,
which the orchestrator allocates while the job runs.

Your answer must:

- argue each design from its failure modes;
- say what each design does when one subtask grows far past its estimate and the others run short;
- commit to one design;
- name the evidence that would reverse your choice.

**E3.A2 (10 pts) — Explain why the release gate must run on your org's own task distribution.**

A VP proposes to replace your org's homegrown eval suite with a respected public agent benchmark.
The VP wants that benchmark as the release gate,
"so we can finally compare ourselves to the industry".

Your answer must:

- state what the green result of a gate must claim;
- derive from that claim why the gate needs your org's own task distribution;
- say what the public benchmark is still legitimately for.

**E3.A3 (10 pts) — Design the permission surface for a fleet of two hundred unattended CI agents.**

The agents triage failing builds.
They read logs and diffs, comment their findings, and open tickets.

Your answer must:

- derive least privilege from the lethal trifecta;
- tier the capabilities, and name the mechanism that owns each tier;
- set an explicit ask-budget;
- name the metric that tells you the surface is mis-tiered.

**E3.A4 (10 pts) — Design the observability that must exist BEFORE the incident below.**

An agent in team A's fleet reads a poisoned wiki page.
Two hours later a secret leaves through team B's egress proxy.
The incident has the shape of Trace 35, but it crosses a team boundary.

Your answer must:

- name the spans, the transcripts, and the artifacts;
- walk through how the on-call engineer uses them;
- go from the proxy log back to the injected instruction;
- go out from there to every other session that read the same page.

## Section B — Judgment memo (30 points)

**E3.B1 (30 pts) — Write a one-page position memo that decides between an off-the-shelf harness and your bespoke harness.**

Your 200-engineer org must choose one of the two, org-wide.
Three engineers maintain the bespoke harness that a platform team built last year.
Forty teams depend on it daily — on its permission rules,
its transcript format, and its deploy pipeline.
The off-the-shelf harness covers the loop, gating, subagents, and telemetry.
It ships improvements monthly, and it covers none of your internal integrations yet.
Nobody has costed the migration.

Address the memo to engineering leadership.
Keep it to one page.
It must contain:

- your decision, committed in the first paragraph — not a framework that decides later;
- the assumptions that the decision stands on, written so that a reader can check them;
- kill-criteria: the concrete, measurable signals that reverse the decision;
- the strongest counter-position, argued well enough that its advocate signs it;
- the first 90 days: a migration plan, or a plan that commits further to the bespoke harness.

Scored on the Appendix C Tier-4 rubric row; the key maps each rubric line to points.

## Section C — Practical (30 points)

Open `exams/l3/practical/` and follow its README.
A candidate agent change must reach the fleet through a staged rollout: eval gate, canary, fleet.
The rollout also carries a block exit and a rollback exit (Trace 33, Trace 34).
The project provides the eval suite, both candidates, and deterministic canary telemetry.
You implement the decision function `next_action()` in `rollout/engine.py`.
Follow the contract that its docstring states:
the boundaries, the terminal stages, and reasons that a human can read.
Scored by pytest: 10 checks × 3 points. Paste your pytest output into the score sheet.

## Score sheet

| Section | Max | Your score |
|---|---|---|
| A — Written | 40 | |
| B — Judgment memo | 30 | |
| C — Practical | 30 | |
| **Total** | **100** | |
