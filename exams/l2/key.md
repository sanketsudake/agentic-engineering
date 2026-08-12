# L2 Exam — Grading key

Repo-only. Never referenced from any file that renders into the PDF.
Every entry gives point-anchored award criteria; award partial credit only where a criterion says so.
Tier-3 entries (E2.A6, E2.A7) grade the bisection walk against the Appendix C Tier-3 row:
hypothesis, the evidence that would kill it, cheapest check first, a class-level fix, a verification step.

## Section A

**E2.A1 (5 pts)**

**Award.** 1 pt per step, each requiring the acting component by name — "the system" earns nothing:

- 1 pt: the **harness** parses the `tool_use` block (id, name, input) and looks the name up in its registry; an unknown name becomes an error result, never a crash.
- 1 pt: the **harness** validates the input against the tool's schema; mismatches become error results.
- 1 pt: the **gate** (permission rules / hooks) decides allow, deny, or ask before anything runs.
- 1 pt: the **executor** runs the tool and captures everything as text (stdout, stderr, return value, or exception), and the harness truncates it to the result budget with an explicit marker.
- 1 pt: the **harness** appends a `tool_result` block with the matching `tool_use_id` and resends the entire context; the model reads the result as ordinary input tokens.

Order must be broadly correct (parse/validate before gate before execute before append).
Subtract nothing for extra correct detail (retry policy, `is_error`, streaming).

**E2.A2 (5 pts)**

**Award.**

- 2 pts: prompt caching — the provider matches the rendered request prefix (tools, then system, then messages) against a cached prefix ending at a `cache_control` breakpoint, and reads the match at ~0.1× the input price; only the new suffix is processed in full.
- 1 pt: the first request paid a write premium (1.25× at the 5-minute TTL, 2× at 1 hour), which is why the saving starts at the second request.
- 1 pt: names `usage.cache_read_input_tokens` — nonzero on the repeat is the proof.
- 1 pt: one correct fragility: any changed byte earlier in the prefix invalidates everything after it; TTL expiry; or the minimum cacheable prefix size below which caching silently no-ops.

**E2.A3 (10 pts)**

**Award.**

- 3 pts: the API contract — every `tool_use` block in an assistant message must have a matching `tool_result` in the immediately following user message. Splitting leaves unmatched `tool_use_id`s, so the provider rejects the next request outright; the session dies exactly when the model parallelizes.
- 3 pts: why "sooner" is an illusion — the model does not exist between requests. It sees context only when the next call is assembled and sent; there is no consumer to receive an early result, so nothing can start early.
- 2 pts: even if the provider accepted it, each extra round-trip is a full model call — full input tokens for the whole context, plus TTFT — so the refactor costs more and is slower, the opposite of its goal.
- 2 pts: states the correct design — run the tool executors concurrently if useful, collect all results, and return them together in one user message, each paired to its `tool_use_id`.

**E2.A4 (10 pts)**

**Award.**

- 3 pts: states the rule — code chooses where the steps are known and variance is expensive; the model chooses where the path depends on what earlier steps discover. Neither answer is an identity; it is a per-step decision.
- 3 pts: applies it per step — all five steps are fixed and known, and "post to billing" is irreversible, so the pipeline stays code. Credit any bounded model-assisted sub-step (classifying a malformed record, drafting the notify text) if it is argued from variance cost and kept behind the code-owned control flow.
- 2 pts: quantifies what the agent would add with nothing to buy — nondeterministic paths, per-run token cost, and an eval suite to prove behavior, all to make choices no run ever needs to vary.
- 2 pts: names a decision record or kill-criterion — e.g. "if an agentic step's variance never changes the outcome, demote it to code"; or the reverse trigger, revisit when inputs become heterogeneous enough that the path genuinely depends on the data.

**E2.A5 (10 pts)**

**Award.**

- 3 pts: names the core problem — the agent did not change, so the 22-point jump is a measurement change. The judge is an uncalibrated instrument; its number is not comparable to the old grader's and not admissible on its own.
- 3 pts: calibration — score the judge's agreement with human labels on a labeled subset before trusting it, and publish that agreement number next to every metric the judge produces.
- 2 pts: bias probes — verbosity bias (check score-vs-length correlation), position bias (run pairwise comparisons in both orders), self-preference (strip model names and telltale formatting).
- 2 pts: operational discipline — pin the judge model and prompt like any deploy artifact, keep humans on the disagreement sample, re-calibrate when the judge or the task distribution drifts.

**E2.A6 (10 pts)**

**Award.** Score the walk, not the conclusion (Appendix C Tier-3 row).
Cap at 5 pts total if the answer jumps to a fix before reading any evidence.

- 2 pts: reads evidence first — the transcript AND the tool telemetry/spans for that session, before changing anything.
- 3 pts: the fork, with the evidence that decides it — (a) two `tool_use` blocks in the transcript means the **model** re-requested (the first result read as failure or silence, so check what the model was shown); (b) one `tool_use` block but two executions in telemetry means the **harness** retried — typically a timeout retry, and a timeout is not proof of failure: the call may have committed before the response was lost.
- 3 pts: class-level fix — retry policy is per-tool, not global: mark tools idempotent or not at registration, never auto-retry non-idempotent tools, surface a timeout as "state unknown — verify before retrying" with a verification tool, and/or send an idempotency key so the server deduplicates.
- 2 pts: verification and a gate — reproduce in staging, then add a regression check (an eval task or a telemetry alert on duplicate side effects) so the class cannot silently return.

**E2.A7 (10 pts)**

**Award.** Score the walk, not the conclusion. This question is graded on the
suite-versus-production comparison axes, not on a generic debugging recitation.
Cap at 4 pts total if the answer never compares production transcripts against the suite.

- 2 pts: starts with ground truth — pulls the transcripts of the reported production failures and puts them next to the suite's tasks.
- 2 pts: coverage axis — the failing task shapes are not in the suite; the suite measures a distribution production has drifted away from. Fix: harvest the real failures into tasks (twenty real failures beat a thousand synthetic ones).
- 2 pts: grader axis — replay the failing production transcripts through the suite's graders; if they score as passes, the grader is too soft (often an uncalibrated or drifted judge). Fix: recalibrate against human labels.
- 2 pts: environment/pin axis — the suite runs a pinned model and config while the fleet floats (a floating alias, a config divergence, different tools). Evidence: compare the model id and config on production spans against the eval's.
- 2 pts: closes the loop — adds the harvested tasks, watches the suite go red, fixes, watches it go green; states that a green suite is a claim about the suite's distribution, nothing more.

## Section B

**E2.B1 (10 pts)**

**Award.** 3 pts per planted bug: named, mechanism explained, production impact stated.
1 pt for a severity ranking argued from blast radius.
No credit for findings outside the three planted bugs;
the loop otherwise follows the Lab 3 pattern and the comments about `tools.dispatch` are true.

- **Bug 1 — timestamp rebuilt into the system prompt every turn (3 pts).**
  1 pt names it: `build_system_prompt()` embeds `time.time()` and is called on every iteration.
  1 pt mechanism: the rendered prefix differs on every request, so the prompt cache never matches — a classic silent invalidator; `cache_read_input_tokens` stays zero.
  1 pt impact: every turn re-pays full input price on the whole growing context (plus write premiums), and TTFT grows with it — a fleet-scale cost and latency multiplier that no error ever surfaces.
- **Bug 2 — results keyed by tool name (3 pts).**
  1 pt names it: `results[call.name] = ...` collapses parallel calls to the same tool.
  1 pt mechanism: two `read_file` calls in one assistant message overwrite each other; one `tool_use_id` gets no `tool_result`, and the provider rejects the follow-up request (every `tool_use` must have a matching result in the next message).
  1 pt impact: the session dies exactly when the model does the reasonable thing — reading two files at once; also the surviving result silently replaces the lost one, so even a tolerant provider would feed the model wrong pairings.
- **Bug 3 — turn budget checked after execution, with `>` (3 pts).**
  1 pt names it: `turns` is incremented and compared only after the tool calls have run, and the comparison is `>`.
  1 pt mechanism: the loop makes `max_turns + 1` model calls before stopping, and the over-budget turn's tool calls have already executed by the time the check fires.
  1 pt impact: cost and side effects overrun the budget — a `max_turns=1` "safety cap" for a risky mode actually allows two full turns — and the loop then returns `""` with no signal that it hit the cap.
- **Ranking (1 pt).** Any order earns the point if argued from blast radius.
  The reference ranking: Bug 2 first (hard correctness/availability failure in normal operation), Bug 1 second (silent, unbounded fleet-wide cost), Bug 3 third (bounded overrun, but note the silent `""` return).

## Section C

Self-scoring: each passing pytest check is 3 points; the practical README maps checks to points.
