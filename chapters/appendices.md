# Appendices

## Appendix A — Quick-reference tables

The numbers and checklists worth reviewing last.
Every volatile number sits in the dated snapshot at the end;
everything before it is structural.

### Context budget per turn

The six segments of Trace 7, with representative sizes for a coding-agent turn.

| Segment | Representative size | Grows with |
|---|---|---|
| System prompt | 1–5K tokens | prompt deploys only; stable across turns |
| Tool definitions | 5–20K tokens (thirty rich schemas) | tool count × schema richness |
| Memory and instructions | 1–10K tokens | store size, unless an injection budget caps it |
| History | the dominant line; ~2K per tool result | turns × tool-result size |
| Injected content | 0–20K tokens | retrieval k × chunk size; hook output |
| Current turn | usually the smallest | task data |

Rule of thumb: fifty tool calls at 2,000 tokens each add 100K tokens to every later request (Chapter 3).

### Cache economics

| Quantity | Value |
|---|---|
| Cache read | ~0.1× input price |
| Cache write, 5-minute TTL | 1.25× input price |
| Cache write, 1-hour TTL | 2× input price |
| Batch processing | 0.5× on everything |
| Break-even, 5-minute TTL | the 2nd request (1.25 + 0.1 < 2 × 1.0) |
| Break-even, 1-hour TTL | the 3rd request (2 + 0.1 + 0.1 < 3 × 1.0) |
| Minimum cacheable prefix | model-dependent, 512–4,096 tokens; below it, caching silently no-ops |
| Breakpoints | max 4; prefix match; render order tools → system → messages |

The four silent invalidators (Trace 6):
a timestamp in the system prompt, unsorted serialization, a tool-set change, a model switch.
Verify with `usage.cache_read_input_tokens`: zero across repeats means an invalidator.

### Tool-schema quality checklist

| Check | Why it matters |
|---|---|
| Description says when to use AND when not | the description is a prompt; ambiguity invites wrong calls |
| Every parameter described | undescribed parameters get guessed values |
| Enum wherever the value set is finite | frees the model from inventing strings |
| `required` list correct | optional-by-accident parameters silently vanish |
| `additionalProperties: false` | required for `strict` mode; blocks invented arguments |
| Result size capped | one generous result can flood the window (Chapter 4) |
| Idempotency stated | decides whether the harness may retry it |

### Retry and timeout defaults

| Stage | Retry? | Backoff | Surface to model? |
|---|---|---|---|
| Model call (429, 5xx) | yes, capped attempts | exponential with jitter | no; the harness owns it |
| Idempotent tool | yes, once or twice | short fixed delay | only the final failure, as `is_error` |
| Non-idempotent tool | never automatically | — | yes; the model decides with fresh state |
| Subagent | re-brief; do not blind-rerun | — | return the failure report to the parent |

Every tool call gets a timeout.
A timed-out non-idempotent tool is in an unknown state — check before acting again (Trace 10).

### Latency anatomy

| Component | Scales with | The lever |
|---|---|---|
| Time to first token (TTFT) | uncached input length | cache the prefix; shorten the context |
| Generation time | output tokens ÷ tokens per second | ask for less output; tokens/s is fixed per tier |
| Loop iterations | turn count | fewer turns — each one repays a full TTFT plus generation |

Streaming improves perceived latency only; the total is unchanged (Chapter 12).

### Model selection

| Dimension | The question to ask |
|---|---|
| Capability tier | does this step need judgment, or mechanics? |
| Context window | does the working set fit, with headroom for results? |
| Cost ratio | adjacent tiers differ 2–5×, top to bottom ~10×; volume multiplies it |
| Latency | is a user waiting on this call? |

Route by decision cost: mechanical steps to a cheap tier, judgment to a capable one;
when a wrong answer is cheap to detect, prefer cheap-and-verify (Chapter 12).

### Failure modes at a glance

Twelve rows aggregated from the chapters' "Where this can fail" lists.

| Symptom | Likely cause | Where to look | Chapter |
|---|---|---|---|
| The loop never ends | no max-turn stop | turn count in the transcript | 1 |
| Response cut off mid-JSON | `max_tokens` hit; valid prefix truncated | `stop_reason`, usage | 2 |
| Cache reads zero on every repeat | a silent invalidator in the prefix | the rendered request bytes | 2 |
| Agent "forgets" mid-task | compaction dropped the evidence | the transcript around the compaction | 3 |
| Tool "succeeded" but nothing changed | error swallowed before the context | the raw tool result | 4 |
| A stored fact is never used | recall missed it, or the budget cut it | the injected memory segment | 5 |
| Confident answer, wrong facts | retrieval missed; model answered from weights | the retrieved chunks | 6 |
| Agent stalls mid-task | a gate waiting on an unanswered ask | the permission log | 7 |
| Subagent returns irrelevant work | a constraint never entered the brief | the brief | 8–9 |
| Eval scores swing run to run | sampling variance; too few attempts | attempts per task | 10 |
| Agent did something nobody asked | an injection in fetched content | full tool results in the transcript | 11 |
| Fleet shifts overnight, no deploy | a floating model alias, not a pin | the model id on the spans | 12 |

### Sampling parameters

| Parameter | What it does | When to touch it |
|---|---|---|
| Temperature | concentrates or spreads next-token choice | lower it for extraction and routing; leave the default for open-ended work |
| Output cap (`max_tokens`) | hard limit, invisible to the model | set it above the worst expected output; always branch on `stop_reason` |
| Stop sequences | end generation at a caller-defined string | rarely; caller protocols only |

No setting guarantees determinism: the same prompt can differ run to run.
Measure over many runs (Chapter 10);
never ship a "deterministic because temperature is zero" claim.

### Model and pricing snapshot (dated 2026-08)

List prices, August 2026; re-verify before relying on them.
The only place in this book prices appear.

| Model tier | Input $/1M | Output $/1M |
|---|---|---|
| Frontier (Fable-class) | 10.00 | 50.00 |
| Opus-class | 5.00 | 25.00 |
| Sonnet-class | 3.00 | 15.00 |
| Haiku-class | 1.00 | 5.00 |

Multipliers: cache read ~0.1×, cache write 1.25× (5m) / 2× (1h), batch 0.5× (table above).

| Tier | Context window | Max output |
|---|---|---|
| Frontier, Opus, Sonnet classes | 1M tokens | 128K |
| Haiku class | 200K tokens | 64K |

## Appendix B — Glossary

- **Agent** — a model that calls tools in a loop to reach a goal.
- **Agentic search** — search the model drives itself: grep, list, and read calls, sharpened over turns.
- **Batch API** — offline processing at half price; results within 24 hours, arrival order not guaranteed.
- **Brief** — the instructions and context a subagent receives; the only world it gets.
- **Cache breakpoint** — a request marker (`cache_control`) setting where a cacheable prefix ends.
- **Candidate edition** — the book build with model answers stripped, for self-testing.
- **Checkpoint** — a review gate placed where a mistake is still cheap to fix.
- **Checkpointer** — a LangGraph store that persists graph state at every superstep.
- **Chunking** — splitting documents into pieces small enough to embed and inject.
- **Compaction** — replacing old turns with a summary to keep the window under its limit.
- **Consolidation** — the memory-write step that updates, deduplicates, or deletes against existing entries.
- **Constrained decoding** — masking invalid next tokens so output must match a schema.
- **Context engineering** — deciding what enters the context window each turn.
- **Context rot** — stale facts persisting in the window and weighing like fresh evidence.
- **Context window** — the token budget one model call carries; the model's entire world for a turn.
- **Cost per solve** — cost per session divided by solve rate; the fleet KPI.
- **Elicitation** — the MCP pattern where a tool call pauses to request user input.
- **Embedding** — a vector for a text chunk; similar meanings land near each other.
- **Eval suite** — a scored task set that turns "seems better" into a defensible number.
- **Excessive agency** — capability beyond the task's needs; the attacker's free ammunition.
- **Grader** — the code check, LLM judge, or human that scores an eval attempt.
- **Guardrail** — a classifier on what enters or leaves a run; a filter, never a boundary.
- **Handoff** — one agent transfers the conversation to another; control moves with it.
- **Harness** — the runtime that owns the loop, context assembly, and gating.
- **Hook** — a handler the harness fires at a lifecycle event; it can block the action.
- **Hybrid search** — vector and keyword search fused into one ranking.
- **Idempotent** — safe to run twice; the property that decides whether a tool may be retried.
- **Lethal trifecta** — private data, untrusted content, and an exfiltration channel in one session.
- **LLM judge** — a model that grades transcripts against a rubric; itself needs calibration.
- **MCP** — Model Context Protocol; the open standard that puts tools outside the agent's process.
- **Memory** — anything the harness persists across sessions and re-injects later.
- **Orchestrator** — the agent that decomposes work, briefs workers, and merges their reports.
- **Permission rule** — a deny, ask, or allow policy evaluated before a tool call dispatches.
- **Prompt caching** — re-reading a matched request prefix at ~0.1× the input price.
- **Prompt injection** — an instruction hiding in data the agent reads.
- **RAG** — retrieval-augmented generation: the harness searches an index and injects the top results.
- **Recall@k** — of the chunks that should be found, the fraction appearing in the top k.
- **Regression gate** — an eval threshold a change must pass before it ships.
- **Reranker** — a stronger scorer that reorders search candidates for precision.
- **Sandbox** — bounds on what an approved process can touch, whoever approved it.
- **Session state** — the harness-side record of one run; complete and session-scoped.
- **Skill** — packaged instructions loaded on demand; progressive disclosure in practice.
- **Solve rate** — the fraction of sessions that finish the task.
- **Stop reason** — the API's statement of why generation ended; the loop's control signal.
- **Streaming** — token deltas delivered as the model generates; improves perceived latency only.
- **Structured output** — decoding constrained to a caller-supplied JSON Schema.
- **Subagent** — an agent launched by another, with an isolated context; it returns a report.
- **System prompt** — the standing frame the harness sets; stable across turns.
- **Temperature** — the sampling knob that spreads or concentrates next-token choice.
- **Token** — the model's unit of text; a subword chunk of a few characters.
- **Tool** — a schema the model reads plus an executor you own.
- **Transcript** — the complete record of a session; the ground truth of debugging.
- **TTFT** — time to first token; grows with uncached input length.
- **Workflow** — a fixed pipeline that may call models; the code chooses the next step.
- **Worktree** — a separate git checkout so parallel agents write without conflicts.

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

Chapters 1–12 teach mechanisms; the architect owns decisions.
This appendix reframes each chapter as the decision it hands you,
states the recurring bets with kill-criteria,
and ends with critique prompts to argue out loud.

### Zoom out, chapter by chapter

- **The loop (Ch 1).** The loop is a commodity. The decision you own is which loops your org runs, who owns each one, and what evidence would retire it.
- **The API surface (Ch 2).** The provider contract is your biggest dependency: pinning model ids and branching on stop reasons is your interface freeze against a vendor who ships monthly.
- **Context (Ch 3).** Context is the scarce resource your platform allocates. The per-segment budget is a policy document, and cache-stable ordering is its enforcement mechanism.
- **Tools (Ch 4).** Every tool is an API contract you will maintain; the schema is the interface freeze, and MCP makes it a public one.
- **Memory (Ch 5).** Memory is a data product with a lifecycle. Someone owns curation, staleness, and deletion, or the store rots into a liability.
- **Retrieval (Ch 6).** The ingest pipeline is infrastructure: the embedding-model pin, re-ingest triggers, and index freshness are ops commitments, not model choices.
- **The harness (Ch 7).** Settings, permission rules, and hooks are de facto org policy. Whoever writes them governs every session — review them like production code.
- **Operating agents (Ch 8).** Gate placement is your risk posture: where human review sits decides which mistakes stay cheap.
- **Multi-agent (Ch 9).** Topology is a cost and failure-mode decision. Every context boundary is a contract you must specify: a brief in, a report out.
- **Evals (Ch 10).** The eval suite encodes your definition of good. It is the asset you always build and never buy.
- **Safety (Ch 11).** The permission surface is least-privilege design, and the ask-budget is human-attention economics: too many prompts is a security regression.
- **Production (Ch 12).** Cost per solve is the KPI you defend. Pins, staged rollouts, and cache hit rate are how a fleet stays a business.

### The recurring bets

**Agents vs workflows.**
A per-decision choice, never an identity (Chapter 13).
Where the path depends on what earlier steps discover, the model chooses — that is what you pay it for.
Where steps are known and variance is expensive, code chooses.
Kill-criterion: if an agentic step's variance never changes the outcome,
or its error rate stays above a fixed pipeline's after two eval cycles, demote it to code.

**Long context vs retrieval.**
Million-token windows plus cached reads make put-it-all-in viable for corpora that fit (Chapter 6).
Long context pays per-turn token cost and attention degradation;
retrieval pays an ingest pipeline and recall failures.
Neither side has won; the choice is per corpus.
Kill-criterion: when the corpus outgrows the window,
or per-query cost exceeds the pipeline's amortized cost, switch — and measure recall@k after.

**Single vs multi-agent.**
One agent beats N until context isolation or wall-clock parallelism pays (Chapter 9).
Coordination is a real cost: briefs, merges, reconciliation, and the failure modes of each.
Kill-criterion: if merge cost eats the context savings,
or merged output scores below the single-agent baseline on your suite, collapse to one agent.

**Prompting vs fine-tuning.**
This is the one place this book discusses fine-tuning.
Current frontier models with disciplined context engineering cover most enterprise needs,
and every mechanism in this book — briefs, retrieval, skills, memory — is prompting-side and survives a model upgrade intact.
Fine-tuning bakes behavior into weights:
it needs training data, an eval suite to prove the gain, and a redo at every base-model upgrade — a recurring cost prompting never pays.
It earns its keep on narrow, stable, high-volume tasks where a small tuned model beats a prompted cheap tier on cost or latency at scale.
Kill-criterion: if a prompted cheap-tier model matches the tuned model's eval scores, the tuning pipeline is pure overhead — delete it.

**Build vs buy.**
Build what encodes your judgment — domain tools, eval suites, your data.
Buy what encodes everyone's — the harness, the observability pipes (Chapter 13).
An org that inverts this has outsourced its judgment and insourced its plumbing.
Kill-criterion: a bespoke harness whose quarterly maintenance exceeds the switching cost has already lost; schedule the migration.

**Autonomy vs oversight.**
Autonomy lengthens where verification is automatic — tests, CI, typed schemas — and stalls where "done" needs a human (Chapter 14).
The bottleneck is verification, not model capability,
so invest in checkable milestones before longer leashes.
Kill-criterion: when unattended failure cost times failure rate exceeds the review time saved, shorten the leash.

### Critique prompts

Argue both sides out loud, then commit — expect the follow-up to attack whichever side you take.

1. **"The harness is a commodity; building your own is malpractice."** For: vendors improve it monthly, and a bespoke loop is compounding maintenance with zero differentiation. Against: a bought harness fixes your permission model, context policy, and telemetry to someone else's roadmap, and some regulated environments cannot accept the trust surface. A position: buy the harness, own the config surface and the evals; build only when a hard constraint — isolation, latency, audit — fails on every bought option, and write the kill-criterion into the decision record.
2. **"RAG is dead; long context killed it."** For: huge windows plus ~0.1× cached reads make put-it-all-in cheap for corpora that fit. Against: corpora grow past any window, attention degrades under bulk, and access control still has to happen somewhere. A position: long context won the small-corpus case; retrieval keeps the large, fresh, and permissioned ones — decide per corpus, with recall@k as the referee.
3. **"Multi-agent systems are a workaround for small context windows."** For: most fan-outs just shard reading, and a bigger window plus agentic search does the same with no merge step. Against: isolation is about attention, cost, and permission separation, not only capacity — and wall-clock parallelism never falls out of window size. A position: mostly true for read fan-outs, false for write parallelism and trust boundaries; justify each topology by what crosses its boundaries.
4. **"Prompt injection is unsolvable, so agents must never touch production data."** For: the model cannot reliably separate instruction from data; compliance stays probabilistic. Against: unsolvable in the model is not unsolvable in the system — deterministic gates, sandboxes, and breaking the trifecta are engineering, not hope. A position: contain it like the injection attacks of the last era — never solved in general, contained everywhere it matters; size each capability to the blast radius you can accept.
5. **"LLM judges cannot be trusted to grade LLMs."** For: position, verbosity, and self-preference biases are documented, and unpinned judges drift. Against: calibrated against human labels, pinned, and probed for bias, a judge scales grading no human team matches. A position: trust the judge as an instrument, not an oracle — calibrate before use, re-calibrate on drift, and keep humans on the disagreement sample.

## Appendix E — Framework Rosetta

One table, mapping the book's recurring concepts to their names in the three stacks.
A "—" means the stack has no first-class primitive there; you build the pattern yourself.

| Concept | Anthropic API / SDK | OpenAI Agents SDK | LangGraph |
|---|---|---|---|
| The loop | your code around `POST /v1/messages`; the Claude Agent SDK ships the Claude Code loop as a library | `Runner.run()` drives the loop to final output, with an enforced `max_turns` | you build it: `StateGraph` nodes and edges, then compile |
| Tool definition | `{name, description, input_schema}` — JSON Schema | tools attached to an agent's definition | tools bound to a tool-executing node |
| Handoff / delegation | subagents: isolated context, report returned to the parent | handoffs — first-class task delegation between agents | conditional edges routing to another node or graph |
| Memory / state | harness-owned: instruction files plus session state | conversation state carried between runs (pattern) | checkpointers persist graph state at every superstep |
| Guardrail / gate | permission rules and hooks, evaluated before dispatch | guardrails — input and output validation | guard nodes and conditional edges you wire yourself |
| Streaming | SSE events, `message_start` through `message_stop` | — | — |
| Structured output | `output_config.format` with a JSON Schema; `strict: true` on tools | — | — |
| Persistence | harness-owned; store the rendered request for replay | — | a `thread_id` in the invocation config resumes prior state |

### Which stack when

**Provider SDK first.**
The book's default is plain Python plus the provider SDK:
the loop you build in Lab 3 is the whole core, a few dozen lines.
A framework must earn its abstraction —
adopt one for a primitive you actually need, never for the loop itself.

**The Agents SDK when handoffs are the shape.**
If the product is triage-and-specialist — control moving between agents mid-conversation —
the Agents SDK makes the handoff pattern of Trace 25 first-class,
with guardrails at the boundaries and a turn cap already enforced.

**LangGraph when the workflow graph is the product.**
When the deliverable is a fixed pipeline with conditional routes and resumable state,
LangGraph makes the graph explicit and checkpointed.
Code chooses the next step there — which is exactly what Chapter 13's agents-vs-workflows record wants for irreversible steps.

**For coding agents, any harness beats a bespoke one.**
The harness is a commodity (Chapter 13).
A Claude Code-class harness ships the permission model, hooks, and context management you would otherwise rebuild badly.
Spend the build budget on your tools and your evals.

Maintenance note: framework APIs move faster than this book prints.
Version pins live in the lab lockfiles;
this table maps concepts, not versions —
when a name here drifts, the concept column still tells you what to search for.

## Appendix F — Further reading

All entries as of August 2026.
Titles are stable; page layouts move —
when a link rots, search the title on the named site.

**Provider documentation**

- Anthropic API documentation — the Messages API, tool use, prompt caching, structured outputs, batches; the primary source behind Chapters 2–3.
- Claude Code documentation (code.claude.com/docs) — settings, memory, hooks, permissions, skills, subagents; the primary source behind Chapters 7–8.
- Claude Agent SDK (`claude-agent-sdk` for Python, `@anthropic-ai/claude-agent-sdk` for TypeScript) — the Claude Code loop as an embeddable library.
- OpenAI Agents SDK documentation (openai/openai-agents-python) — agents, `Runner.run`, handoffs, guardrails; the source of that Appendix E column.
- LangGraph documentation (langchain-ai/langgraph) — StateGraph, checkpointers, thread-scoped persistence.

**Specifications**

- Model Context Protocol specification (modelcontextprotocol.io) — transports, lifecycle, primitives, auth; the source behind Trace 11.
- The MCP changelog, same site — read it before upgrading anything; the 2026-07-28 revision was breaking, and the next one can be too.

**Seminal writing**

- "ReAct: Synergizing Reasoning and Acting in Language Models" (Yao et al.) — the paper that named the reason-act loop every agent still runs.
- Anthropic, "Building Effective Agents" — the essay that fixed the agents-vs-workflows vocabulary this book uses.
- Anthropic's context-engineering essay (search: "effective context engineering for AI agents") — the provider's own statement of Chapter 3's discipline.
- Anthropic's tool-writing essay (search: "writing effective tools for agents") — the provider-side companion to Chapter 4.
- Simon Willison's "lethal trifecta" writing (simonwillison.net) — the widely circulated security framing behind Chapter 11; his running prompt-injection series is the field's best chronicle.
- OWASP Top 10 for LLM Applications (owasp.org, search the title) — Chapter 11's threat model in checklist form; useful in audits and compliance conversations.

**Evals and operations**

- SWE-bench (search the title) — the coding-agent benchmark; read its task format before designing your own suite (Chapter 10).
- OpenTelemetry generative-AI semantic conventions (search the title) — a neutral telemetry shape for the "neutral spine" Chapter 13 asks for.
