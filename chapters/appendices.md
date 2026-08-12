# Appendices

## Appendix A — Quick-reference tables

*(Placeholder — filled in Phase 4.)*
Planned tables: context-budget math, cache economics, sampling parameters,
tool-schema checklist, retry and timeout defaults, latency anatomy,
model-selection dimensions, the cross-chapter failure-mode grid,
and one dated model and pricing snapshot (the only place volatile numbers appear).

## Appendix B — Glossary

*(Placeholder — filled in Phase 4.)*
One-line definitions for every term the book uses.

- **Agent** — a model that calls tools in a loop to reach a goal.
- **Harness** — the runtime that owns the loop, context assembly, and gating.

## Appendix C — Answer-quality rubric

This rubric grades every question in the book, the exam written sections, and the Part E capstones.
Question tiers carry the levels: Tier 1 → L1, Tier 2 and Tier 3 → L2, Tier 4 → L3.

### What each tier probes

| Tier | Probes | Strong signal | Weak signal |
|---|---|---|---|
| 1 — Explain | Can you narrate the mechanism? | Names the acting component at each step; correct order; defines terms in passing | Vague agents ("the system"), missing steps, memorized phrases without mechanism |
| 2 — Reason | Can you predict behavior from the mechanism? | Derives the answer from a trace; states the trade-off both ways; knows what changes the answer | Asserts conclusions without a causal chain; one-sided trade-offs |
| 3 — Design & Debug | Can you walk a scenario? | Bisects: forms a hypothesis, names the evidence that would kill it, checks cheapest first; fixes the class, not the instance | Jumps to a fix; changes settings before reading the transcript; no verification step |
| 4 — Judge | Can you commit to a position? | Names assumptions and kill-criteria; argues the strongest counter-position honestly; then decides and owns it | Survey answers ("it depends") with no decision; strawman counter-positions; no exit condition |

Cross-tier signals of a strong engineer:

1. Reads the transcript before theorizing. The transcript is the ground truth of an agentic system.
2. Distinguishes the model from the harness. Most "model problems" are harness problems.
3. Quantifies with tokens, turns, and dollars — not adjectives.
4. States what would change their mind.

### One question at three quality levels

**Q — An agent re-reads the same three files every turn. What is happening, and what do you change?**

**Weak (does not pass L1).** "The model is forgetting. Use a bigger context window or a better model."
Names no component, proposes spend before diagnosis, and treats the model as the whole system.

**Strong (passes L2).** "Re-reads mean the file contents are not in the context the harness assembles — dropped by compaction, or never persisted.
I would read one transcript: if the reads are there but early, compaction is evicting them — pin or summarize them into the system segment.
If each turn starts fresh, the harness is not carrying history — that is a state bug, not a model choice.
Verify by re-running the same task and counting read calls before and after."
Walks the bisection, names harness mechanisms, ends with a measurable check.

**Principal (passes L3).** Everything in the strong answer, plus:
"Re-reads are a symptom class, not an incident: any long session will hit it, so I would add turn-count and repeated-tool-call metrics to the eval suite (Chapter 10) and gate merges on them.
Whether to pin files or teach the agent file-memory (Chapter 5) depends on task shape — pin for a fixed repo, memory for a fleet.
Kill-criterion: if repeated-read rate stays above 10% after pinning, the compaction policy itself is wrong."
Turns the fix into a regression gate, names the fork in the road, and sets an exit condition.

### How to read at your level

| You are | Read | Do | Prove it |
|---|---|---|---|
| L1 Builder | Parts A–B, Chapter 7 | Labs 1–5; narrate Traces 1, 2, 9 from memory | Tier 1–2 questions; the L1 exam |
| L2 Operator | Everything except Part E capstones | All labs through 10; debug one real transcript per chapter | Tier 3 questions; the L2 exam |
| L3 Architect | Everything, plus Appendix D | Labs 11–12; write one Scenario critique per Part E chapter | Tier 4 questions; the L3 exam |

## Appendix D — The architect's lens

*(Placeholder — filled in Phase 4.)*
Per-chapter zoom-out, the recurring bets with kill-criteria, and critique prompts.

## Appendix E — Framework Rosetta

*(Placeholder — filled in Phase 4.)*
One table mapping every recurring concept across the Anthropic SDK,
OpenAI Agents SDK, and LangGraph, plus "which stack when".

## Appendix F — Further reading

*(Placeholder — filled in Phase 4.)*
Provider docs, the MCP spec, seminal posts and papers; every entry dated.
