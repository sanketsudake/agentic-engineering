# L3 Exam — The Architect

This exam verifies: you can commit to defensible positions and design org-scale agentic systems.
Score yourself against `exams/l3/key.md` after finishing — not before.

**Time:** 3 hours (Section A closed-book, 60 min; Sections B–C open-repo, 120 min).
**Materials:** Section A: nothing. Sections B–C: this repo, no live model access needed.
**Total:** 100 points
**Pass:** at least 70 points overall AND at least 18/30 on Section B.

## Section A — Written (40 points)

**E3.A1 (10 pts) — Your orchestrator fans a nightly research job out to five subagents (Trace 24). One platform engineer proposes a hard token cap per subagent; another proposes one shared budget for the whole job, allocated by the orchestrator as it runs. Argue the choice from the failure modes of each design — what each does when one subtask balloons while the others run short — then commit to one and name the evidence that would flip you?**

**E3.A2 (10 pts) — A VP proposes replacing your org's homegrown eval suite with a respected public agent benchmark as the release gate, "so we can finally compare ourselves to the industry". Explain, from what a gate's green must claim, why the gate has to run on your org's own task distribution — and what the public benchmark is still legitimately for?**

**E3.A3 (10 pts) — Design the permission surface for a fleet of two hundred unattended CI agents that triage failing builds: they read logs and diffs, comment findings, and open tickets. Derive least privilege from the lethal trifecta, tier the capabilities and name the mechanism that owns each tier, and set an explicit ask-budget — including the metric that tells you the surface is mis-tiered?**

**E3.A4 (10 pts) — An agent in team A's fleet reads a poisoned wiki page; two hours later a secret leaves through team B's egress proxy (Trace 35's shape, across team boundaries). Design the observability that must already exist BEFORE this incident: name the spans, transcripts, and artifacts, then walk how the on-call uses them — from the proxy log back to the injected instruction, and out to every other session that read the same page?**

## Section B — Judgment memo (30 points)

**E3.B1 (30 pts) — Your 200-engineer org must choose: adopt an off-the-shelf harness org-wide, or keep the bespoke harness a platform team built last year. Write the one-page position memo?**

The facts on the table: three engineers maintain the bespoke harness,
and forty teams depend on it daily — its permission rules, its transcript
format, its deploy pipeline.
The off-the-shelf harness covers the loop, gating, subagents, and telemetry,
ships improvements monthly, and covers none of your internal integrations yet.
Nobody has costed the migration.

Address the memo to engineering leadership. One page. It must contain:

- your decision, committed in the first paragraph — not a framework for deciding later;
- the assumptions the decision stands on, stated so they can be checked;
- kill-criteria: the concrete, measurable signals that would reverse the decision;
- the strongest counter-position, argued honestly enough that its advocate would sign it;
- the first 90 days — a migration plan or a doubling-down plan, whichever your decision demands.

Scored on the Appendix C Tier-4 rubric row; the key maps each rubric line to points.

## Section C — Practical (30 points)

Open `exams/l3/practical/` and follow its README.
A candidate agent change must reach the fleet through a staged rollout:
eval gate, canary, fleet — with block and rollback exits (Trace 33, Trace 34).
The eval suite, both candidates, and deterministic canary telemetry are provided;
you implement the decision function, `next_action()` in `rollout/engine.py`,
to the contract its docstring states — boundaries, terminal stages, and
human-readable reasons included.
Scored by pytest: 10 checks × 3 points. Paste your pytest output into the score sheet.

## Score sheet

| Section | Max | Your score |
|---|---|---|
| A — Written | 40 | |
| B — Judgment memo | 30 | |
| C — Practical | 30 | |
| **Total** | **100** | |
