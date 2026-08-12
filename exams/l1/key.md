# L1 Exam — Grading key

Repo-only. Never referenced from any file that renders into the PDF.
Every entry gives point-anchored award criteria; award partial credit only where a criterion says so.
Tier-1 entries (E1.A1–E1.A4) grade against the Appendix C Tier-1 row:
the acting component named at each step, correct order, terms defined in passing.
Tier-2 entries (E1.A5–E1.A7) grade the causal chain, not the conclusion.

## Section A

**E1.A1 (10 pts)**

**Award.** This is Trace 2. Every step requires the acting component by name —
"the system" or "the AI" earns nothing for that step:

- 2 pts: the **harness** assembles the context, naming at least three of its ingredients:
  system prompt, memory/instructions, conversation history, tool definitions.
- 1 pt: the **model** generates and emits a tool call instead of an answer
  (stop reason `tool_use`); it executes nothing itself.
- 2 pts: the **harness** validates the call and checks it against permission rules
  before anything runs (1 pt validation, 1 pt gating).
- 1 pt: the **tool executor** runs the call in the environment
  (filesystem, shell — wherever the rename actually happens).
- 2 pts: the **harness** appends the tool result to the context and resends
  the whole thing; the loop repeats until the model has what it needs
  (1 pt for the append, 1 pt for naming the repetition as a loop with a stop).
- 1 pt: the **model** emits final text; the **harness** post-processes —
  any one of writing memory, firing hooks, recording telemetry.
- 1 pt: the order is broadly correct end to end
  (assemble before generate, validate/gate before execute, append before the next model call).

Subtract nothing for extra correct detail (parallel tool calls, truncation, caching).

**E1.A2 (10 pts)**

**Award.**

- 3 pts: names the three parts — `name`, `description`, `input_schema`
  (JSON Schema), with per-parameter descriptions and a `required` list
  (2 pts for the three parts, 1 pt for parameter-level descriptions or `required`).
- 2 pts: the **model** reads the description and parameter descriptions to decide
  when to call, which tool to call, and with what arguments — no other channel
  informs that decision.
- 2 pts: the **harness** reads the name to look up the executor in its registry,
  and the schema to validate the model's input before dispatch.
- 1 pt: the **provider** can enforce the schema through constrained decoding
  (`strict: true`, requiring `additionalProperties: false` and `required`) —
  which removes syntactic failures, not semantic ones.
- 2 pts: the failure — a description that omits when to use the tool (and when not)
  leaves the model guessing: wrong-tool calls, calls that should not happen, or a
  tool that is never picked. Full credit requires stating that tool descriptions
  are prompts and deserve prompt-level review.

**E1.A3 (10 pts)**

**Award.**

- 3 pts: the correction — the provider API is stateless per call; nothing about the
  session persists server-side between requests.
- 3 pts: the actual mechanism — the **harness** appended the tool result to the
  message list and resends the entire context (system prompt, tool definitions,
  full history) on the next request; the model reads the file as ordinary input
  tokens it was handed, not as anything it remembers.
- 2 pts: the 40-turn implication — 40 growing requests, not 40 small ones, so
  input tokens dominate agent cost and every oversized tool result is re-paid on
  every later turn (hence result budgets and truncation).
- 2 pts: heads off the near-miss — prompt caching makes the resend cheaper but is
  a cost optimization, not server-side state: the full prefix is still sent and
  any changed byte invalidates the match.

**E1.A4 (10 pts)**

**Award.**

- 4 pts: the segments, at 1 pt each up to 4, each with what it holds:
  system prompt (identity, standing rules); tool definitions (every schema and
  description); memory/instructions (project files, stored facts); history
  (prior messages and tool results); injected content (retrieved documents,
  hook output, reminders); the current turn (newest user message or tool result).
- 2 pts: names **history** — specifically accumulated tool results — as the
  segment that dominates a long agent session.
- 2 pts: the arithmetic — results accumulate: fifty tool calls returning 2,000
  tokens each add 100,000 tokens to every later request; tool definitions are
  constant but wide; the system prompt and user messages are usually smallest.
- 2 pts: one structural truth — the segments are a harness fiction: the model
  receives one flat token sequence with no boundaries (1 pt), and a segment you
  cannot measure is a segment you cannot control — measure per segment (1 pt).

**E1.A5 (10 pts)**

**Award.**

- 3 pts: the core mechanism — tool definitions live in the context window and the
  harness sends all of them every turn, called or not.
- 2 pts: the cost effect — five more schemas add their tokens to every single
  request in every session, so cost per session rises with zero calls made.
- 3 pts: the quality effect — the definitions shift what the model attends to;
  descriptions are prompts, and overlapping or vague ones pull the model toward
  wrong choices on tasks that used to work (2 pts for the attention/behavior
  mechanism, 1 pt for noting cache invalidation: a changed tool list changes the
  request prefix, so cached turns reprice at full input cost).
- 2 pts: the change — remove or prune the unused tools, or load them
  just-in-time / progressively (carry a one-line description, load the body on
  use) instead of pre-loading five full schemas.

**E1.A6 (10 pts)**

**Award.**

- 2 pts: assigns correctly — one-shot RAG for the 200k-document support corpus,
  agentic search for the coding agent.
- 3 pts: defends RAG for support — the corpus dwarfs the context window; the
  harness searches the index and injects top results, so each answer is one model
  call at low cost; query shape is known and repetitive, which is what an ingest
  pipeline (chunk, embed, index) is good at.
- 3 pts: defends agentic search for code — the repo changes hourly, so an index
  is stale by the time it is queried, while search tools read live data; code is
  already greppable, so no ingest pipeline is needed; exploratory questions let
  the model sharpen its query each round.
- 2 pts: names the price both ways — agentic search pays per turn (every round is
  a full model call, so latency and token cost scale with search depth), and RAG
  pays in pipeline ops and freshness (re-ingest triggers, or the index quietly
  serves stale truth).

**E1.A7 (10 pts)**

**Award.**

- 3 pts: the prediction — the model reads `"done"` as success, builds on state
  that does not exist, and reports the task complete; a confidently wrong answer,
  not a retry (the model retries what it can see failing, and it saw success).
- 2 pts: the transcript — it ends looking healthy: a tool call, a result, final
  text claiming the write happened; nothing changed in the environment.
- 3 pts: the mechanism — the model can only fix what is in its context; the
  operator log is telemetry the model never reads, so the error reached the wrong
  audience (2 pts), and this is the silent-success class, the worst tool-failure
  class (1 pt).
- 2 pts: why it is hardest to spot, and the fix — no crash, no error string, no
  loop; only comparing the transcript's claim against the environment reveals it.
  Fix: every failure becomes text in the `tool_result` (exception type and
  message, `is_error: true`), and logging stays telemetry, not the error channel.

## Section B

Self-scoring: each passing pytest check is 3 points; the practical README maps checks to points.
