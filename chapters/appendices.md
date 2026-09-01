# Appendices

## Appendix A — Quick-reference tables

The numbers and checklists worth reviewing last.
Every number that changes with time sits in the dated snapshot at the end;
everything before it is structural.

### Context budget per turn

The six segments of [Trace 7](ch03.md#trace-7-what-happens-when-the-context-for-a-turn-is-assembled), with typical sizes for a coding-agent turn.

| Segment | Typical size | Grows with |
|---|---|---|
| System prompt | 1–5K tokens | new prompt deploys only; stable across turns |
| Tool definitions | 5–20K tokens (thirty rich schemas) | number of tools, size of each schema |
| Memory and instructions | 1–10K tokens | store size, unless the injection budget caps it |
| History | the largest segment; ~2K per tool result | number of turns, size of each result |
| Injected content | 0–20K tokens | chunks retrieved, chunk size, hook output |
| Current turn | usually the smallest | task data |

For example: fifty tool calls at 2,000 tokens each add 100K tokens to every later request ([Chapter 3](ch03.md)).

### Cache economics

| Quantity | Value |
|---|---|
| Cache read | ~0.1× input price |
| Cache write, 5-minute TTL | 1.25× input price |
| Cache write, 1-hour TTL | 2× input price |
| Batch processing | 0.5× on everything |
| Break-even, 5-minute TTL | the 2nd request (1.25 + 0.1 < 2 × 1.0) |
| Break-even, 1-hour TTL | the 3rd request (2 + 0.1 + 0.1 < 3 × 1.0) |
| Minimum cacheable prefix | model-dependent, 512–4,096 tokens; below it the cache does nothing and gives no error |
| Breakpoints | max 4; the prefix must match; render order is tools, then system, then messages |

Four changes break the cache and give no error ([Trace 6](ch02.md#trace-6-what-happens-when-a-prompt-cache-hits--and-misses)):

- A timestamp in the system prompt.
- A serialization that does not sort its keys.
- A tool-set change.
- A model switch.

Verify with `usage.cache_read_input_tokens`: a zero across repeats means one of the four.

### Tool-schema quality checklist

| Check | Why it matters |
|---|---|
| Description says when to use the tool and when not | the model reads the description as a prompt; an unclear one causes wrong calls |
| Every parameter described | the model guesses values you do not describe |
| Enum wherever the value set is finite | the model picks a value instead of inventing a string |
| `required` list correct | an accidentally optional parameter disappears with no error |
| `additionalProperties: false` | `strict` mode needs it; it blocks invented arguments |
| Result size capped | one large result can fill the context window ([Chapter 4](ch04.md)) |
| Idempotency stated | this decides whether the harness may retry the tool |

### Retry and timeout defaults

| Stage | Retry? | Backoff | Show to the model? |
|---|---|---|---|
| Model call (429, 5xx) | yes, capped attempts | exponential with jitter | no; the harness handles it |
| Idempotent tool | yes, once or twice | short fixed delay | only the final failure, as `is_error` |
| Non-idempotent tool | never automatically | — | yes; the model decides with the new state |
| Subagent | write a new brief; do not repeat the old one | — | return the failure report to the parent |

Every tool call gets a timeout.
After a non-idempotent tool times out, its state is unknown; check it before you act again ([Trace 10](ch04.md#trace-10-what-happens-when-a-tool-call-fails)).

### Where the latency comes from

| Component | Scales with | What to change |
|---|---|---|
| Time to first token (TTFT) | length of the input the cache misses | cache the prefix; shorten the context |
| Generation time | output tokens divided by tokens per second | ask for less output; the speed is fixed for a tier |
| Loop iterations | turn count | use fewer turns; each turn pays a full TTFT plus generation |

Streaming improves only the latency the user feels; the total time does not change ([Chapter 12](ch12.md)).

### Reliability over a loop

An agent multiplies its per-step reliability by itself, once for every step.
This table is that multiplication. It is the strongest argument in the book for short loops.

| Reliability per step | 5 steps | 10 steps | 20 steps | 50 steps |
|---|---|---|---|---|
| 99% | 95% | 90% | 82% | 61% |
| 95% | 77% | 60% | 36% | 8% |
| 90% | 59% | 35% | 12% | 1% |
| 80% | 33% | 11% | 1% | 0% |

Read the 95% row. A step that works nineteen times in twenty finishes a twenty-step task about a third of the time.
Two levers move that number, and only two:

- Raise the reliability of each step: better tool schemas, surfaced errors, a verification step.
- Use fewer steps: a shorter loop, a smaller task, code instead of a model where the path is already known.

A better prompt moves the first lever a little. Removing ten steps moves the second one a lot.

### Model selection

| Dimension | The question to ask |
|---|---|
| Capability tier | does this step need judgment, or mechanics? |
| Context window | does the working set fit, with space left for results? |
| Cost ratio | adjacent tiers differ by 2–5 times, top to bottom by about 10; volume multiplies it |
| Latency | does a user wait for this call? |

Route by the cost of the decision: mechanical steps to a cheap tier, judgment to a capable one.
When a wrong answer is cheap to detect, use the cheap tier and verify ([Chapter 12](ch12.md)).

### Failure modes and where to look

Twelve rows from the chapters' "Where this can fail" lists.

| Symptom | Likely cause | Where to look | Chapter |
|---|---|---|---|
| The loop never ends | no maximum-turn stop | turn count in the transcript | 1 |
| Response cut off inside the JSON | output hit `max_tokens`; the rest was cut | `stop_reason` and usage | 2 |
| Cache reads zero on every repeat | something in the prefix changed | the rendered request bytes | 2 |
| The agent loses a fact mid-task | compaction dropped the evidence | the transcript around the compaction | 3 |
| The tool reported success but nothing changed | the code hid the error from the context | the raw tool result | 4 |
| A stored fact is never used | recall missed it, or the budget cut it | the injected memory segment | 5 |
| Confident answer with wrong facts | retrieval missed; the model answered from weights | the retrieved chunks | 6 |
| The agent stalls mid-task | a gate waits for an answer nobody gave | the permission log | 7 |
| The subagent returns irrelevant work | a constraint never entered the brief | the brief | 8–9 |
| Eval scores change from run to run | sampling variance; too few attempts | attempts per task | 10 |
| The agent did something nobody asked for | an injected instruction in fetched content | full tool results in the transcript | 11 |
| The fleet changes overnight, with no deploy | a floating model alias, not a pin | the model id on the spans | 12 |

### Sampling parameters

| Parameter | What it does | When to change it |
|---|---|---|
| Temperature | makes the next token more random or less random | lower it for extraction and routing; keep the default for open-ended work |
| Output cap (`max_tokens`) | a hard limit the model cannot see | set it above the largest output you expect; always branch on `stop_reason` |
| Stop sequences | end generation at a string the caller gives | rarely; only for caller protocols |

No setting makes the model deterministic: the same prompt can give a different answer on each run.
Measure over many runs ([Chapter 10](ch10.md));
never claim that output is deterministic because the temperature is zero.

### Model and pricing snapshot (dated 2026-08)

List prices, August 2026; re-verify before relying on them.
The only place in this book with prices.

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
- **Agentic search** — a search the model drives itself: grep, list, and read calls, sharpened over turns.
- **Batch API** — offline processing at half price; results within 24 hours, in any order.
- **Brief** — the instructions and context a subagent receives; the only world it gets.
- **Cache breakpoint** — a request marker (`cache_control`) that says where the stored prefix ends.
- **Candidate edition** — this book built with the model answers removed, for self-testing.
- **Checkpoint** — a review gate placed where a mistake is still cheap to fix.
- **Checkpointer** — a LangGraph store that saves graph state at every superstep.
- **Chunking** — splitting documents into pieces small enough to embed and inject.
- **Compaction** — replacing old turns with a summary to keep the input under the model's limit.
- **Consolidation** — the memory step that updates, merges, or deletes existing entries as it writes.
- **Constrained decoding** — blocking invalid next tokens so output must match a schema.
- **Context engineering** — deciding what text enters the model's input each turn.
- **Context rot** — old facts that stay in the input, which the model reads as current.
- **Context window** — the token budget one model call carries; the model's entire world for a turn.
- **Cost per solve** — the cost of a session divided by the fraction of sessions that finish.
- **Elicitation** — a tool call that stops and asks the user for input.
- **Embedding** — a vector for a text chunk; similar meanings land near each other.
- **Entity resolution** — merging the names that mean one entity before they enter a graph index.
- **Ephemeral node** — an agent that exists for one step: a brief in, a report out, nothing kept.
- **Eval suite** — a scored task set that turns "it seems better" into a number you can defend.
- **Excessive agency** — capability beyond the task's needs, which an attacker can use.
- **Grader** — the code, model, or person that scores an eval attempt.
- **Graph engineering** — a 2026 name with two meanings: wiring agents into nodes and edges, and graph retrieval. Ask which one the writer means.
- **Graph retrieval** — storing facts as triples and querying the relations, instead of ranking text by similarity.
- **Guard metric** — a second metric that a shortcut on the target metric damages; it makes the shortcut visible.
- **Guardrail** — a classifier on what enters or leaves a run; a filter, never a boundary.
- **Handoff** — one agent transfers the conversation to another; control moves with it.
- **Harness** — the runtime that owns the loop, context assembly, and gating.
- **Hook** — a handler the harness runs at a lifecycle event; it can block the action.
- **Hybrid search** — vector and keyword search combined into one ranking.
- **Idempotent** — safe to run twice; the property that decides whether a tool may be retried.
- **Lethal trifecta** — private data, untrusted content, and a channel that sends data out, in one session.
- **LLM judge** — a model that scores transcripts against a rubric; it needs calibration itself.
- **Loop engineering** — a 2026 name for designing the agent loop, its checks, and its stop conditions instead of writing single prompts.
- **MCP** — Model Context Protocol; the open standard that puts tools outside the agent's process.
- **Memory** — anything the harness saves across sessions and injects again later.
- **Orchestrator** — the agent that divides the work, briefs the workers, and merges their reports.
- **Permission rule** — a deny, ask, or allow policy evaluated before a tool call dispatches.
- **Prompt caching** — the provider re-reads a matched request prefix at ~0.1× the input price.
- **Prompt injection** — an instruction that hides in the data the agent reads.
- **RAG** — retrieval-augmented generation: the harness searches an index and injects the top results.
- **Recall@k** — of the chunks the search should find, the fraction that appears in the top k.
- **Regression gate** — a score threshold a change must pass before it ships.
- **Reranker** — a stronger scorer that puts search candidates in a better order.
- **Resident node** — an agent that owns a domain across many runs and keeps that domain's context.
- **Role structure** — which agent holds which domain, tools, and permissions; it changes by deploy.
- **Sandbox** — a limit on what an approved process can touch, whoever approved it.
- **Session state** — the harness's record of one run; complete, and it ends with the session.
- **Skill** — instructions the harness loads only when the task needs them.
- **Solve rate** — the fraction of sessions that finish the task.
- **Stop reason** — the API's value for why generation ended; the loop reads it to choose the next step.
- **Streaming** — output sent piece by piece as the model writes it; only the latency the user feels improves.
- **Structured output** — output that must match a JSON Schema the caller supplies.
- **Subagent** — an agent another agent starts, with an isolated context; it returns a report.
- **System prompt** — the standing instructions the harness sets; stable across turns.
- **Temperature** — the setting that makes the next token more random or less random.
- **Token** — the model's unit of text; a piece of a word, a few characters long.
- **Tool** — a schema the model reads, plus the code you run for it.
- **Transcript** — the complete record of a session; the primary evidence when you debug.
- **Triple** — a subject, a relation, and an object; the unit a graph index stores.
- **TTFT** — time to first token; grows with the input the cache misses.
- **Verifier** — a node that tries to break a result, in a fresh context, against written criteria.
- **Work structure** — the task shape of one run; the orchestrator may reshape it while the run continues.
- **Workflow** — a fixed pipeline that may call models; the code chooses the next step.
- **Worktree** — a separate git checkout, so parallel agents write files without conflicts.

## Appendix C — Answer-quality rubric

This rubric grades every question in the book, the written exam sections, and the Part E capstones.
Question tiers carry the levels: Tier 1 → L1, Tier 2 and Tier 3 → L2, Tier 4 → L3.

### What each tier probes

| Tier | Probes | Strong signal | Weak signal |
|---|---|---|---|
| 1 — Explain | Can you describe the mechanism? | names the acting component at each step; keeps the correct order; defines terms as they appear | says "the system" instead of a component; skips steps; memorized phrases with no mechanism |
| 2 — Reason | Can you predict behavior from the mechanism? | derives the answer from a trace; states the trade-off both ways; knows what changes the answer | states conclusions with no chain of cause; one side of the trade-off only |
| 3 — Design & Debug | Can you work through a scenario? | forms a hypothesis, names the evidence that would disprove it, checks the cheapest first; fixes the class of fault, not the instance | jumps to a fix; changes settings before reading the transcript; no verification step |
| 4 — Judge | Can you commit to a position? | names assumptions and kill-criteria; argues the strongest counter-position honestly; then decides and owns it | surveys the options ("it depends") with no decision; weak counter-positions; no exit condition |

Signals of a strong engineer at every tier:

1. Reads the transcript before theorizing. The transcript is the primary evidence in an agentic system.
2. Separates the model from the harness. Most problems people call model problems are harness problems.
3. Quantifies with tokens, turns, and dollars — not adjectives.
4. States what would change their mind.

### One question at three quality levels

**Q — An agent re-reads the same three files every turn. What is happening, and what do you change?**

**Weak (does not pass L1).** "The model is forgetting. Use a bigger context window or a better model."
Names no component, spends money before a diagnosis, and treats the model as the whole system.

**Strong (passes L2).** "Re-reads mean the file contents are not in the context the harness assembles: compaction dropped them, or the harness never saved them.
I would read one transcript. If the reads are there but early, compaction is removing them, so I would pin or summarize them into the system segment.
If each turn starts with nothing, the harness is not carrying the history, and that is a state bug, not a model choice.
I would verify by running the same task again and counting read calls before and after."
Works through the bisection, names harness mechanisms, ends with a measurable check.

**Principal (passes L3).** Everything in the strong answer, plus:
"Re-reads are a class of symptom, not one incident. Any long session meets it. I would add turn count and repeated tool calls to the eval suite ([Chapter 10](ch10.md)) and gate merges on them.
The choice between pinned files and file memory ([Chapter 5](ch05.md)) depends on the task: pin for a fixed repository, memory for a fleet.
Kill-criterion: if the repeated-read rate stays above 10% after pinning, the compaction policy itself is wrong."
Turns the fix into a regression gate, names the choice to make, and sets an exit condition.

### How to read at your level

| You are | Read | Do | Prove it |
|---|---|---|---|
| L1 Builder | Parts A–B, [Chapter 7](ch07.md) | Labs 1–5; describe Traces 1, 2, 9 from memory | Tier 1–2 questions; the L1 exam |
| L2 Operator | everything except the Part E capstones | all labs through 10; debug one real transcript per chapter | Tier 3 questions; the L2 exam |
| L3 Architect | everything, plus Appendix D | Labs 11–12; write one Scenario critique per Part E chapter | Tier 4 questions; the L3 exam |

## Appendix D — The architect's lens

Chapters 1–12 teach mechanisms; the architect owns decisions.
This appendix gives each chapter as the decision it hands you,
states the recurring bets with kill-criteria,
and ends with critique prompts to argue out loud.

### The decision in each chapter

- **The loop (Ch 1).** The loop is a commodity. You decide which loops your organization runs, who owns each, and what evidence would retire it.
- **The API surface (Ch 2).** The provider contract is your biggest dependency. Pinned model ids and a branch on the stop reason freeze your interface against a vendor who ships monthly.
- **Context (Ch 3).** Context is the scarce resource your platform allocates. The budget for each segment is a policy document, and a stable cache order enforces it.
- **Tools (Ch 4).** Every tool is an API contract you will maintain; the schema freezes the interface, and MCP makes it public.
- **Memory (Ch 5).** Memory is a data product with a lifecycle. Someone owns curation, staleness, and deletion, or the store decays into a liability.
- **Retrieval (Ch 6).** The ingest pipeline is infrastructure: the pinned embedding model, re-ingest triggers, and index freshness are operations commitments, not model choices.
- **The harness (Ch 7).** Settings, permission rules, and hooks are real organization policy. Whoever writes them governs every session — review them like production code.
- **Operating agents (Ch 8).** Gate placement states your risk position: where human review sits decides which mistakes stay cheap.
- **Multi-agent (Ch 9).** Topology is a decision about cost and failure modes. Every context boundary is a contract you specify: a brief goes in, a report comes out.
- **Evals (Ch 10).** The eval suite holds your definition of good. It is the asset you always build and never buy.
- **Safety (Ch 11).** The permission surface is least-privilege design, and the budget for asks is the economics of human attention: too many prompts is a security regression.
- **Production (Ch 12).** Cost per solve is the number you defend. Pins, staged rollouts, and cache hit rate are how a fleet stays a business.

### The recurring bets

**Agents vs workflows.**
Choose for each decision; it is never an identity ([Chapter 13](ch13.md)).
Where the path depends on what earlier steps find, the model chooses — that is what you pay it for.
Where steps are known and variance is expensive, code chooses.
Kill-criterion: demote it to code if its variance never changes the outcome,
or its error rate stays above a fixed pipeline's after two eval cycles.

**Long context vs retrieval.**
Million-token windows plus cached reads make "put it all in" practical for corpora that fit ([Chapter 6](ch06.md)).
Long context pays a token cost every turn, and attention degrades;
retrieval pays for an ingest pipeline and recall failures.
Neither side has won; the choice is per corpus.
Kill-criterion: switch when the corpus outgrows the window,
or the cost of a query passes the pipeline's amortized cost — then measure recall@k.

**Single vs multi-agent.**
One agent beats several until context isolation or parallel wall-clock time pays ([Chapter 9](ch09.md)).
Coordination is a real cost: briefs, merges, reconciliation, and the failure modes of each.
Kill-criterion: collapse to one agent if merge cost passes the context savings,
or merged output scores below the single-agent baseline on your suite.

**Prompting vs fine-tuning.**
This is the one place this book discusses fine-tuning.
Frontier models with disciplined context engineering cover most enterprise needs.
Every mechanism in this book — briefs, retrieval, skills, memory — is prompting-side and survives a model upgrade.
Fine-tuning writes behavior into the weights.
It needs training data, an eval suite to prove the gain, and a repeat at every base-model upgrade — a recurring cost prompting never pays.
It earns its cost on narrow, stable, high-volume tasks where a small tuned model beats a prompted cheap tier on cost or latency at scale.
Kill-criterion: if a prompted cheap-tier model matches the tuned model's eval scores, the tuning pipeline is pure overhead — delete it.

**Build vs buy.**
Build what holds your judgment — domain tools, eval suites, your data.
Buy what holds everyone's — the harness, the observability pipes ([Chapter 13](ch13.md)).
An organization that inverts this has bought its judgment and built its plumbing.
Kill-criterion: a harness you built has already lost if a quarter of maintenance costs more than the switch; schedule the migration.

**Autonomy vs oversight.**
Autonomy extends where verification is automatic — tests, CI, typed schemas — and stops where a human must decide the work is done ([Chapter 14](ch14.md)).
The bottleneck is verification, not model capability,
so build milestones a machine can check before you extend the autonomy.
Kill-criterion: when unattended failure cost times failure rate passes the review time saved, reduce the autonomy.

### Critique prompts

Argue both sides out loud, then commit — expect the next question to attack the side you take.

1. **"The harness is a commodity; building your own is malpractice."** For: vendors improve it monthly, and a loop you build adds maintenance with no advantage. Against: a bought harness fixes your permission model, context policy, and telemetry to someone else's roadmap, and some regulated environments cannot accept that trust surface. A position: buy the harness, own the config surface and the evals. Build your own only when a hard constraint — isolation, latency, audit — fails on every product you can buy. Write the kill-criterion into the decision record.
2. **"RAG is dead; long context killed it."** For: huge windows plus cached reads at ~0.1× make "put it all in" cheap for corpora that fit. Against: corpora grow past any window, attention degrades on bulk text, and access control still has to happen somewhere. A position: long context won the small-corpus case; retrieval keeps the large, fresh, and permissioned ones — decide per corpus, and let recall@k settle it.
3. **"Multi-agent systems are a workaround for small context windows."** For: most fan-outs only divide the reading, and a bigger window plus agentic search does the same with no merge step. Against: isolation is about attention, cost, and permission separation, not only capacity — and parallel wall-clock time does not come from window size. A position: mostly true for read fan-outs, false for parallel writes and trust boundaries; justify each topology by what crosses its boundaries.
4. **"Prompt injection is unsolvable, so agents must never touch production data."** For: the model cannot reliably separate instruction from data; compliance stays probabilistic. Against: what the model cannot solve, the system can contain — deterministic gates, sandboxes, and breaking the trifecta are engineering, not hope. A position: contain it like the injection attacks of the last era — never solved in general, contained everywhere it matters. Size each capability to the damage you can accept.
5. **"LLM judges cannot be trusted to grade LLMs."** For: bias by position, by verbosity, and toward its own output is documented, and an unpinned judge drifts. Against: calibrated against human labels, pinned, and tested for bias, a judge grades at a scale no human team matches. A position: trust the judge as an instrument, not an oracle. Calibrate before use, re-calibrate on drift, and keep humans on the sample where judge and human disagree.

## Appendix E — Framework Rosetta

One table maps the book's recurring concepts to their names in the three stacks.
A "—" means the stack has no first-class primitive there; you build the pattern yourself.

| Concept | Anthropic API / SDK | OpenAI Agents SDK | LangGraph |
|---|---|---|---|
| The loop | your code around `POST /v1/messages`; the Claude Agent SDK ships the Claude Code loop as a library | `Runner.run()` drives the loop to a final output, and enforces `max_turns` | you build it: `StateGraph` nodes and edges, then compile |
| Tool definition | `{name, description, input_schema}` — JSON Schema | tools attached to an agent's definition | tools bound to a node that executes tools |
| Handoff / delegation | subagents: an isolated context, a report returned to the parent | handoffs: first-class delegation of a task between agents | conditional edges that route to another node or graph |
| Memory / state | owned by the harness: instruction files plus session state | conversation state carried between runs, as a pattern | checkpointers save graph state at every superstep |
| Guardrail / gate | permission rules and hooks, evaluated before dispatch | guardrails: validation of input and output | guard nodes and conditional edges you wire yourself |
| Streaming | SSE events, `message_start` through `message_stop` | — | — |
| Structured output | `output_config.format` with a JSON Schema; `strict: true` on tools | — | — |
| Persistence | owned by the harness; store the rendered request so you can replay it | — | a `thread_id` in the invocation config resumes the earlier state |

### Which stack when

**Provider SDK first.**
The book's default is plain Python plus the provider SDK:
the loop you build in Lab 3 is the whole core, a few dozen lines.
A framework must earn its abstraction —
adopt one for a primitive you need, never for the loop itself.

**The Agents SDK when handoffs are the shape.**
If the product is a triage agent plus specialists, control moves between agents in one conversation.
The Agents SDK makes that handoff pattern of [Trace 25](ch09.md#trace-25-what-happens-when-one-agent-hands-off-to-another) first-class,
with guardrails at the boundaries and a turn cap already enforced.

**LangGraph when the workflow graph is the product.**
When the deliverable is a fixed pipeline with conditional routes and resumable state,
LangGraph makes the graph explicit and saves checkpoints of the state.
There the code chooses the next step, which is what the agents-vs-workflows record in [Chapter 13](ch13.md) asks for on irreversible steps.

**For coding agents, any harness beats one you build.**
The harness is a commodity ([Chapter 13](ch13.md)).
A Claude Code-class harness ships the permission model, hooks, and context management you would otherwise rebuild badly.
Spend the build budget on your tools and your evals.

Maintenance note: framework APIs change faster than this book prints.
Version pins live in the lab lockfiles.
This table maps concepts, not versions —
when a name here changes, the concept column still tells you what to search for.

## Appendix F — Further reading

All entries are current as of August 2026.
Titles are stable, but page layouts move;
when a link fails, search the title on the named site.

**Provider documentation**

- Anthropic API documentation — the Messages API, tool use, prompt caching, structured outputs, batches; the primary source behind Chapters 2–3.
- Claude Code documentation (code.claude.com/docs) — settings, memory, hooks, permissions, skills, subagents; the primary source behind Chapters 7–8.
- Claude Agent SDK (`claude-agent-sdk` for Python, `@anthropic-ai/claude-agent-sdk` for TypeScript) — the Claude Code loop as a library you embed.
- OpenAI Agents SDK documentation (openai/openai-agents-python) — agents, `Runner.run`, handoffs, guardrails; the source of that column in Appendix E.
- LangGraph documentation (langchain-ai/langgraph) — StateGraph, checkpointers, thread-scoped persistence.

**Specifications**

- Model Context Protocol specification (modelcontextprotocol.io) — transports, lifecycle, primitives, auth; the source behind [Trace 11](ch04.md#trace-11-what-happens-when-the-agent-calls-an-mcp-server).
- The MCP changelog, same site — read it before you upgrade anything; the 2026-07-28 revision was breaking, and the next one can be too.

**Key papers and essays**

- "ReAct: Synergizing Reasoning and Acting in Language Models" (Yao et al.) — the paper that named the reason-act loop every agent still runs.
- Anthropic, "Building Effective Agents" — the essay that fixed the agents-vs-workflows vocabulary this book uses.
- Anthropic on its multi-agent research system (search: "how we built our multi-agent research system") — the orchestrator-worker pattern of [Chapter 9](ch09.md), with the provider's own cost figures: a large token multiple over one chat, and token use explaining most of the performance difference. Read it before you defend a fan-out.
- Microsoft's GraphRAG project (github.com/microsoft/graphrag) — the entity-graph pipeline and the local-versus-global query split of [Chapter 6](ch06.md).
- Anthropic's essay on context engineering (search: "effective context engineering for AI agents") — the provider's own statement of the discipline in [Chapter 3](ch03.md).
- Anthropic's essay on tool writing (search: "writing effective tools for agents") — the provider-side companion to [Chapter 4](ch04.md).
- Simon Willison's "lethal trifecta" writing (simonwillison.net) — the widely circulated security framing behind [Chapter 11](ch11.md); his continuing series on prompt injection is the best record in the field.
- OWASP Top 10 for LLM Applications (owasp.org, search the title) — the threat model of [Chapter 11](ch11.md) as a checklist; useful in audits and compliance conversations.

**Evals and operations**

- SWE-bench (search the title) — the benchmark for coding agents; read its task format before you design your own suite ([Chapter 10](ch10.md)).
- OpenTelemetry generative-AI semantic conventions (search the title) — a neutral telemetry shape for the neutral spine [Chapter 13](ch13.md) asks for.

## Appendix G — The open-source stack, by layer

The rest of this book teaches mechanisms and stays away from product names.
This appendix is the exception, because an architect must still choose something at each layer.
It is a map of the layers, not a catalogue.
The layers are stable. The projects in the last column are not.

**Dated August 2026.** Check the licence and the latest release on the project's own repository before you commit to it.
Treat the names as a starting shortlist, not a recommendation.

**How to choose inside a layer.** Three questions settle most decisions:

- Does the layer earn its place at all, or can an existing system do the job?
- Does the licence permit what you plan to build (MIT and Apache-2.0 are safe for commercial work; AGPL and SSPL carry obligations when you host the software as a service)?
- Does the project have enough users that your error message is already answered somewhere?

Adoption beats features. A weaker project with ten times the users costs less of your time.

### The model layer

| Layer | What you choose | Judge it on | Open options today |
|---|---|---|---|
| Open weights | the model you run yourself | licence, tool-use quality, sizes offered | Llama family, Qwen3, DeepSeek, gpt-oss |
| Serving engine | how weights become an API | throughput, prefix caching, batching | vLLM, SGLang |
| Local runtime | a model on your own machine | setup cost, quantisation, hardware reach | Ollama, llama.cpp |
| Gateway | one API in front of many providers | key management, cost control, fallback | LiteLLM |

A gateway is the layer that makes the routing and fallback of [Chapter 12](ch12.md) possible without a rewrite.

### The agent layer

| Layer | What you choose | Judge it on | Open options today |
|---|---|---|---|
| Agent framework | who owns the loop | control over state, resumability, escape cost | LangGraph, CrewAI, Microsoft Agent Framework, LlamaIndex |
| Coding-agent harness | the runtime of [Chapter 7](ch07.md) | permission model, hooks, repository awareness | OpenHands, Aider, Cline |
| Tool protocol | how tools reach the agent | transport, discovery, auth | Model Context Protocol, with SDKs and FastMCP |
| Sandbox | the blast radius of [Chapter 4](ch04.md) | isolation strength, start time, filesystem control | E2B, Firecracker, gVisor |

### The knowledge layer

| Layer | What you choose | Judge it on | Open options today |
|---|---|---|---|
| Vector store | recall over your corpus | filtering, hybrid search, operational cost | Qdrant, pgvector, Milvus, Chroma |
| Ingest and parsing | what a document becomes | table and layout fidelity, OCR quality | Docling, Unstructured, Marker |
| Memory layer | what survives a session | write policy, conflict handling, storage | Mem0, Letta, Graphiti, LangGraph checkpointers |

Choose `pgvector` when the vectors belong beside business data you already run in Postgres.
That decision removes a whole system from the diagram, which is worth more than a benchmark.

### The operations layer

| Layer | What you choose | Judge it on | Open options today |
|---|---|---|---|
| Tracing | whether you can see the loop | span model, transcript replay, retention | Langfuse, Arize Phoenix, OpenLLMetry |
| Eval framework | how a change is judged | grader types, CI fit, dataset handling | Ragas, DeepEval, Promptfoo, Inspect AI |
| Guardrails | what a policy can stop | rule expressiveness, latency, PII handling | NeMo Guardrails, Guardrails AI, LLM Guard, Presidio |
| Red teaming | what an attacker finds first | attack coverage, reporting | garak, PyRIT |
| Durable execution | what happens after a crash | retries, resumability, scheduling | Temporal, Ray |

Wire tracing before you wire features. You cannot debug what you cannot see, and every agent defect is a transcript that nobody has read yet ([Trace 32](ch12.md#trace-32-what-happens-when-a-bad-session-is-traced)).

### You need fewer layers than this table implies

A first production agent often needs four: a hosted model, a tool protocol, tracing, and an eval suite.
Every other layer is a decision you can defer until a real limit forces it.
Adopt a layer when you can name the limit it removes.
That test is the whole of [Chapter 13](ch13.md)'s build-versus-buy argument, applied one row at a time.

*The projects named above were shortlisted from the* Open Source Toolkit for Building AI Agents 2026, *compiled by Avinash Singh (Let's Code), August 2026. The selection there is that author's work; the judgements in this appendix are ours.*
