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

Source for this section: Anthropic model catalog + API reference (via the claude-api skill bundle, cache dated 2026-06-24); verified 2026-08-12.

- **Current Anthropic families:** Claude 5 (Fable 5, Opus 5, Sonnet 5), Claude 4.x (Opus 4.6–4.8, Sonnet 4.6, Haiku 4.5).
  Prose rule: prefer "current frontier models"; name a model only when correctness demands it.
- **Context windows:** 1M tokens on current Opus/Sonnet/Fable tiers; 200K on Haiku 4.5.
  Max output: 128K (64K Haiku); the SDKs require streaming for large `max_tokens` to avoid HTTP timeouts.
- **Thinking:** adaptive thinking (`thinking: {type: "adaptive"}`) is the current mechanism;
  fixed `budget_tokens` is removed on current models.
  Depth is controlled by `output_config.effort` (`low`…`max`).
- **Model discovery:** `GET /v1/models` returns per-model `max_input_tokens`, `max_tokens`, and a `capabilities` tree — capability facts can be queried live, not hardcoded.

## Provider API feature status

Source: Anthropic API reference (via the claude-api skill bundle, cache dated 2026-06-24); verified 2026-08-12. Status tags as of that date.

- **Messages API** (`POST /v1/messages`) is the single endpoint; tools and output constraints are features of it, not separate APIs. GA.
- **Tool use** (GA): tools declared as `{name, description, input_schema}` (JSON Schema);
  the model returns `tool_use` content blocks with `stop_reason: "tool_use"`;
  the caller executes and replies with `tool_result` blocks (matching `tool_use_id`) in a single user message.
  Parallel tool calls: one assistant message may carry multiple `tool_use` blocks; ALL results must return in ONE user message.
  Failed tools return `tool_result` with `is_error: true` — never dropped.
- **Stop reasons** (GA): `end_turn`, `max_tokens`, `stop_sequence`, `tool_use`, `pause_turn` (resumable server-tool pause), `refusal` (check `stop_details`), `model_context_window_exceeded`.
- **Structured outputs** (GA): `output_config.format` with `type: "json_schema"` (constrained decoding), and `strict: true` on tool definitions (guaranteed-valid tool inputs; schema needs `additionalProperties: false` + `required`). Old top-level `output_format` is deprecated.
- **Streaming** (GA): SSE event sequence `message_start` → `content_block_start` → `content_block_delta`* → `content_block_stop` (per block) → `message_delta` (carries stop_reason + usage) → `message_stop`.
- **Prompt caching** (GA): PREFIX match — any byte change invalidates everything after it.
  Render order `tools` → `system` → `messages`.
  `cache_control: {type: "ephemeral"}`, max 4 breakpoints, default TTL 5 min (`ttl: "1h"` option).
  Economics: reads ~0.1× input price; writes 1.25× (5m) / 2× (1h); minimum cacheable prefix is model-dependent (512–4096 tokens) — below it, caching silently does nothing.
  Verification: `usage.cache_read_input_tokens` (zero across repeats ⇒ a silent invalidator).
- **Batch API** (GA): `POST /v1/messages/batches`, 50% price discount, results within 24h, keyed by `custom_id` (arrival order not guaranteed).
- **Token counting** (GA): `POST /v1/messages/count_tokens`; counts are model-specific (tokenizers differ across generations).
- **Compaction** (beta, header `compact-2026-01-12`): server-side summarization of long conversations; the returned compaction block must be passed back verbatim.
- **Context editing** (beta, header `context-management-2025-06-27`): clears old tool results/thinking (pruning, not summarizing).
- **Server-side tools** (GA unless noted): web search, web fetch, code execution, tool search; MCP connector (beta `mcp-client-2025-11-20`).
- **Task budgets** (beta `task-budgets-2026-03-13`): advisory token budget the model sees and paces against — distinct from `max_tokens` (hard, invisible to the model).

## MCP spec facts

Source: modelcontextprotocol.io spec pages + changelog + release blog (corroborated across 4 primary pages); verified 2026-08-12.

- **Current revision: 2026-07-28** (a breaking, stateless release). Previous: 2025-11-25. Date-based versioning, bumped only on incompatible changes.
- **Transports:** stdio and Streamable HTTP. Streamable HTTP in the current revision is a single POST-only endpoint per request (no `Mcp-Session-Id`, no standalone GET/SSE stream, no `Last-Event-ID` resumability); routing headers `Mcp-Method`, `Mcp-Name`, `MCP-Protocol-Version`. HTTP+SSE (2024-11-05) is formally Deprecated.
- **Lifecycle — TWO ERAS (Trace 11 must say which it traces):**
  - *Legacy (≤2025-11-25, still common in the field):* `initialize` request (protocolVersion, capabilities, clientInfo) → server responds (capabilities, serverInfo, instructions) → client sends `notifications/initialized` → normal operation.
  - *Current (2026-07-28):* NO handshake. Every request carries protocol version + clientInfo + clientCapabilities in `params._meta`; servers accept/reject per request (`UnsupportedProtocolVersionError`, -32022, lists supported versions). `server/discover` is a mandatory RPC the client MAY call up front for supportedVersions/capabilities/serverInfo. The spec defines a legacy↔modern compatibility matrix.
  - Book ruling: Trace 11 traces the CURRENT stateless flow; Concepts carries one paragraph on the legacy handshake and the compatibility reality.
- **Server primitives:** tools (`tools/list`, `tools/call`), resources (`resources/list`, `resources/read`), prompts (`prompts/list`, `prompts/get`).
  Client primitives: elicitation (kept, now via the Multi Round-Trip Request pattern — `resultType: "input_required"` + `inputRequests`/`inputResponses`); roots, sampling, logging are Deprecated (≥12-month removal window).
- **Tool results:** `result.content[]` (text/image/audio/resource blocks), optional `structuredContent` validated against `outputSchema`, and `isError: true` for tool-execution errors (model-visible) vs JSON-RPC protocol errors (malformed request/unknown tool). Every result carries `resultType` (`complete` | `input_required`). List results carry `ttlMs`/`cacheScope` caching hints.
- **Auth:** OAuth 2.1 for HTTP transports; MCP server = resource server; RFC9728 protected-resource metadata is MUST; RFC8707 `resource` parameter MUST; Client ID Metadata Documents favored, Dynamic Client Registration deprecated. stdio servers use environment credentials, not OAuth.

## Harness facts (Claude Code)

Source: code.claude.com/docs (hooks, settings, memory, skills, sub-agents, permissions, permission-modes, mcp, agent-sdk pages); verified 2026-08-12.
Claude Code is the book's worked example; these facts back Chapter 7-8 traces.

- **Session startup order (Trace 17 backing):** settings resolve by precedence
  managed policy → CLI args → `.claude/settings.local.json` → `.claude/settings.json` → `~/.claude/settings.json`.
  Memory files (CLAUDE.md) load broadest-first and CONCATENATE (never override-replace):
  managed → user `~/.claude/CLAUDE.md` → project `./CLAUDE.md` → `./CLAUDE.local.md`;
  `@path` imports, max depth 4. Subdirectory CLAUDE.md files load on demand.
- **Hooks (Trace 19 backing):** shell/HTTP/MCP handlers bound to lifecycle events in settings under `hooks.<EventName>` with matchers.
  Core events to teach: `SessionStart`, `UserPromptSubmit`, `PreToolUse`, `PostToolUse`, `Stop`, `SubagentStop`, `PreCompact`, `SessionEnd` (the full list is ~30 events; teach the shape, not the enumeration).
  Blocking semantics: exit 0 = success (stdout → context only for prompt/session events); exit 2 = BLOCKING (stops the action, wins over everything);
  JSON output can set `permissionDecision: allow|deny|escalate` (PreToolUse) and `continue: false`.
- **Permission model (Trace 18 backing):** rules `Tool` or `Tool(specifier)` in `permissions.allow/deny/ask`;
  evaluated **deny → ask → allow**, first match wins, specificity irrelevant.
  Modes: `default` (reads only), `acceptEdits`, `plan`, `auto` (classifier-gated), `dontAsk`, `bypassPermissions`.
  Interaction: PreToolUse hooks run BEFORE rule evaluation; a hook exit-2 blocks even an allow rule; a hook "allow" cannot override a deny/ask rule.
- **Skills (Trace 20 backing):** `<dir>/skills/<name>/SKILL.md` with YAML frontmatter (`name`, `description`, `when_to_use`, `allowed-tools`, `context: fork`, `disable-model-invocation`, …).
  Progressive disclosure: description always in context; body loads on invocation and persists for the session; sidecar files load on demand.
  Discovery: enterprise > personal `~/.claude/skills` > project `.claude/skills`; plugins namespaced.
  Slash commands (`.claude/commands/<name>.md`) are unified with skills; `$ARGUMENTS`/`$N` substitution; `` !`cmd` `` injects shell output.
- **Subagents (Trace 22 backing):** `.claude/agents/<name>.md`, YAML frontmatter (`name`, `description` required; `tools`, `model` sonnet|opus|haiku|inherit, `permissionMode`, `maxTurns`, `memory`, `isolation: worktree`).
  Invoked by automatic description-match, `@agent-<name>` mention, or the harness's Agent tool; isolated context, result returned to the parent.
- **MCP config:** `.mcp.json` at project root (project scope, committed, requires interactive approval); local + user scopes in `~/.claude.json`. Precedence local > project > user > plugin. Transports stdio, http (streamable), sse (deprecated), ws.
- **Claude Agent SDK:** `claude-agent-sdk` (Python) / `@anthropic-ai/claude-agent-sdk` (TS) — the same loop, tools, and context management that power Claude Code, as an in-process library (shares hooks, subagents, MCP, permissions, skills).

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
- **Lab-pinned framework versions** (authoritative pins live in each lab's `uv.lock`):
  lab07 pins langgraph 1.2.11, langgraph-checkpoint-sqlite 3.1.1, langchain-core 1.5.4 (verified 2026-08-12).
  Sharp edge: `SqliteSaver.from_conn_string` is a context manager; construct `SqliteSaver(sqlite3.connect(...))` directly when the checkpointer must outlive a block.

## Pricing snapshot

Feeds ONLY the dated Appendix A table; nothing else in the book states a price.
Source: Anthropic pricing (via the claude-api skill bundle, cache dated 2026-06-24); verified 2026-08-12. Re-verify at each release build.

| Model tier | Input $/1M | Output $/1M |
|---|---|---|
| Frontier (Fable-class) | 10.00 | 50.00 |
| Opus-class | 5.00 | 25.00 |
| Sonnet-class | 3.00 | 15.00 |
| Haiku-class | 1.00 | 5.00 |

Multipliers that matter for cost math (Appendix A): cache read ~0.1×, cache write 1.25× (5m TTL) / 2× (1h TTL), batch 0.5×.

## Sources

*(Each fact above lists its source and verified date inline.)*
