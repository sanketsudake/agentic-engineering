# Research notes — version-sensitive facts

Baseline: **August 2026**.
Every version-sensitive claim in the book (model names, API features, SDK behavior,
MCP spec details, prices) MUST match an entry here,
and every entry carries a source and a verified date.
A stale entry (older than one build cycle) blocks reuse until re-verified.

Writing rules:

- Name a model or version only when correctness demands it; prefer "current frontier models".
- Never present a beta or preview feature as default behavior.
- Volatile numbers (prices, context sizes) live only in the dated Appendix A table.
- Anything unverifiable at writing time is phrased as a pattern, not a product claim.

## Terminology rulings (the book's fixed definitions)

- **Agent** — a model that calls tools in a loop to reach a goal.
- **Workflow** — a fixed pipeline that may call models; the code chooses the next step.
- **Harness** — the runtime that owns the loop, context assembly, and gating.
- **Context engineering** — deciding what enters the context window each turn; supersedes "prompt engineering" as the umbrella term.

## Model families & capabilities

*(To verify and fill before Phase 1 writing begins.)*

## Provider API feature status

*(To verify and fill before Phase 1 writing begins: structured outputs, prompt-caching semantics, batch API, streaming event types, tool-use API shape — each tagged GA/beta with date.)*

## MCP spec facts

*(To verify and fill: spec revision date, transports, primitives, auth status.)*

## Harness facts (Claude Code)

*(To verify and fill: hook event list, skill/command format, subagent mechanics, settings surface.)*

## Framework facts

*(Partial — full pass in Phase 3. Feeds Appendix E.)*

- **OpenAI Agents SDK (Python):** `Runner.run()` executes the agent loop —
  calls the LLM, processes tool calls and handoffs until final output, with an
  enforced `max_turns` limit. Core primitives: agents (instructions + tools),
  handoffs (task delegation between agents), guardrails (input/output validation).
  Source: openai/openai-agents-python docs (index.md, running_agents.md, quickstart.md); verified 2026-08-12.
- **LangGraph:** the loop is an explicit `StateGraph` — you `add_node`/`add_edge`
  (plus conditional edges) and compile. Checkpointers persist graph state at every
  superstep; a `thread_id` in the invocation config resumes prior state, so
  persistence is a graph feature, not a chat feature.
  Source: langchain-ai/langgraph docs (libs/checkpoint README, graph examples); verified 2026-08-12.

## Pricing snapshot

*(To verify and fill; feeds only the dated Appendix A table.)*

## Sources

*(Each fact above lists its source and verified date inline.)*
