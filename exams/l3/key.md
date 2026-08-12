# L3 Exam — Grading key

Repo-only. Never referenced from any file that renders into the PDF.
Every entry gives point-anchored award criteria; award partial credit only where a criterion says so.
Tier-3 entries (E3.A3, E3.A4) grade the design against the Appendix C Tier-3 row:
the walk, the class-level design, the verification — not a recited checklist.
E3.B1 grades against the Appendix C Tier-4 row, mapped line by line to points below.

## Section A

**E3.A1 (10 pts)**

**Award.** Both sides must be argued from failure modes before the commit;
cap at 5 pts if only one design's failure mode appears.

- 2 pts: frames the real question — subtask cost is unknowable up front (research subtasks are context-heavy and uneven), so the design decides who absorbs the variance: each worker alone, or the job as a whole.
- 3 pts: per-subagent caps' failure mode — the cap is a per-worker guess. The ballooning subtask hits it and returns a truncated or shallow report while the other four finish far under budget; the job "succeeds" with one silently weak section, and the unspent budget is stranded where it is not needed. The failure is silent: no error, just a worse merged answer.
- 3 pts: shared budget's failure modes — one runaway worker starves its siblings (the noisy-neighbor problem), so the orchestrator must meter mid-flight, which is new coordination logic that can itself fail; and the blast radius widens — one worker's loop-until-budget bug now takes down the whole job, not one section.
- 2 pts: a committed choice plus the flip evidence. Either commitment earns the points if it follows from the failure modes — e.g. shared budget with per-worker floors when subtask variance is high; hard caps when subtasks are uniform or one overrun must never sink the job. The flip evidence must be measurable: stranded-budget rate, truncated-report rate, or job-level failure rate moving the other way.

**E3.A2 (10 pts)**

**Award.**

- 3 pts: states what the gate's green must claim — "this change does not hurt our users on our tasks" (the suite encodes the org's definition of good; Chapter 10). That claim is only measurable on the org's own task distribution; a benchmark's green claims something about someone else's.
- 3 pts: the decoupling mechanism — the benchmark samples different task shapes, tools, and graders, so a change can move the benchmark score and production quality independently. Both gate errors follow: a regression ships because the benchmark never exercises the failing shape, and a good change is blocked by benchmark noise it never caused.
- 2 pts: contamination and Goodhart — public benchmarks leak into training data, and once a score gates releases, teams optimize the score; the number stops measuring what it measured.
- 2 pts: what the benchmark is still for — comparing base models at selection time, a coarse external sanity check, trend awareness across model generations; never a merge gate. Strong answers add the harvest loop: production failures become suite tasks (twenty real failures beat a thousand synthetic ones).

**E3.A3 (10 pts)**

**Award.** Score the design, not a recited tool list.
Cap at 5 pts if the answer never treats the ask-budget as a designed, measured quantity.

- 2 pts: derives capability from the task shape, not the agent product — triage needs read access to logs, diffs, and CI artifacts; it does not need production credentials, repo write, or open egress. Anything beyond the task is excessive agency: free ammunition on the adversarial path.
- 2 pts: audits the trifecta explicitly — CI agents read untrusted content by design (build logs, PR diffs, dependency output), so the other two legs get cut: no secrets in the context (scoped, short-lived, read-only tokens) and egress pinned to an allowlist (provider API, artifact store, ticket system).
- 2 pts: tiers with a named owner per tier — reads allowed by rule; scoped, reversible writes (comment on the build, open a ticket, push to a quarantined branch) gated by deterministic rules and hooks; irreversible or egress-bearing actions (touching pipeline config, anything with production reach) denied outright or held for a human. The gate is the harness, not a system-prompt plea.
- 2 pts: the ask-budget as human-attention economics — two hundred unattended agents cannot ask per action; asks are reserved for the rare, decidable case and routed to an on-call queue with the evidence attached (the diff, the host, the amount). States a target rate the reviewers can actually read.
- 2 pts: the mis-tier metric and the loop — approval rate near 100% means the gate is theater (move that class to allow); a rising deny/attempt rate flags either an attack or a missing capability. Guardrail hits and ask rates are dashboards, and the surface is reviewed like production code.

**E3.A4 (10 pts)**

**Award.** The question asks what must exist BEFORE the incident;
cap at 5 pts if the answer designs after-the-fact logging or never crosses the team boundary.

- 2 pts: full transcripts retained for every session — every tool call and every tool result, including the untrusted content the model actually read, with retention long enough to cover a detection lag of hours to days. Without the transcript there is no ground truth to reconstruct from.
- 2 pts: spans with a correlation id that crosses team boundaries — session id and org-wide trace id propagated into every downstream call, and the egress proxy logging that id with each request. The cross-team join from team B's proxy line to team A's session is impossible to retrofit; it exists at incident time or never.
- 2 pts: content provenance artifacts — a hash (or stored copy) of each untrusted input read, with its source and version, plus which tool produced it; guardrail and classifier hits logged even when the action was allowed. This is what makes "who else read this page" answerable.
- 2 pts: the reconstruction walk, in order — start at the proxy log line, join on the correlation id to the session, open that transcript, find the secret leaving and the instruction that caused it, then walk back to the first untrusted read (the poisoned wiki version) as the entry point.
- 2 pts: closes the class — query by content hash for every other session that read the same page, rotate the exposed secret, and turn the incident into a regression: an eval task or a standing alert on that egress pattern. Strong answers name the readiness test: "can I answer 'what did the model see' for any production session, today?"

## Section B

**E3.B1 (30 pts)**

**Award.** Map the Appendix C Tier-4 row to points, 6 per line.
Either decision — adopt off-the-shelf or double down on bespoke — can earn full marks;
the grade is the quality of the commitment, not its direction.
Cap the whole question at 15 pts if the memo runs a survey ("it depends", both options kept alive)
instead of deciding.

- **Decision committed (6 pts).** One owned decision, stated in the first paragraph, unhedged, with the org named as the actor ("we adopt X; the platform team's new charter is Y"). 3 pts if the decision appears but only after the analysis, hedged; 0 pts for a framework-for-deciding-later.
- **Assumptions named (6 pts).** 2 pts each, up to 3, for load-bearing and checkable assumptions — e.g. the commodity harness covers the forty teams' loop, gating, and context needs; three maintainers is understated once on-call and integration churn are counted; the org's differentiation lives in tools, evals, and data, not in the loop (Appendix D's build-vs-buy bet). Decorative assumptions ("AI is moving fast") earn nothing.
- **Kill-criteria concrete and measurable (6 pts).** Signals with numbers and dates that would reverse this decision — e.g. "fewer than 10 of 40 teams migrated by day 60", "a hard isolation requirement fails the vendor spike", "bespoke maintenance exceeds two engineer-quarters per quarter". 3 pts if exit conditions exist but nothing would measurably trigger them; 0 pts if the decision has no exit.
- **Counter-position steelmanned (6 pts).** The strongest opposite case, argued so its advocate would sign it — for adoption: the bespoke harness encodes a year of org-specific permission and deploy decisions, forty dependent teams make migration a forty-team tax, and the vendor's roadmap now owns your policy surface; for doubling down: three engineers against a vendor's monthly release cadence is a losing race, and the maintenance is judgment outsourced to plumbing. Then answered, not waved at. 3 pts for a real but unanswered counter; 0 pts for a strawman.
- **90-day plan actionable (6 pts).** Dated, sequenced, owned — for migration: pilot teams chosen by week 2, an adapter for the transcript and permission formats, eval-gate parity proven before any team cuts over, the bespoke harness frozen (security fixes only), and the three engineers' new charter; for doubling down: a funded roadmap, an SLA to the forty teams, and the same eval-gated bar applied to the harness's own releases. 3 pts for a plan with steps but no dates or owners.

## Section C

Self-scoring: each passing pytest check is 3 points; the practical README maps checks to points.
