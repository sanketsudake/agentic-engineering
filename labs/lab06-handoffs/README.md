# Lab 6 — Multi-agent handoffs

**Goal:** build a triage agent that hands off to two specialists —
refunds and tech support —
using the OpenAI Agents SDK.
You are not writing the loop this time (Lab 3 did that);
`agents.Runner` owns it.
Your job is to declare the agents and the handoff relationship correctly.

**Level:** L2 · **Stack:** OpenAI Agents SDK (`openai-agents`) · **Time:** ~60 min · offline

**Offline mode (default, no keys):**

```bash
uv sync
uv run pytest                      # 5 red tests are your task list
```

**Reference check:**

```bash
LAB_TARGET=solution uv run pytest  # the reference implementation passing
```

## Your task

1. Open `starter/handoff/agents.py`.
   Each function's docstring is the full spec — there is no separate spec document.
2. Implement `build_agents()`: three `Agent` objects
   (`Triage`, `Refunds`, `Tech Support`),
   wired so `Triage` can hand off to both specialists.
3. Implement `run_triage(question)`: build fresh agents and run the triage
   agent with `Runner.run_sync`, returning the SDK's `RunResult` unchanged.
4. Make the 5 tests in `tests/test_lab.py` pass.

**Done means:** `uv run pytest` is fully green against `starter/`.

## What this proves

A handoff is a **tool call the model chooses to make** — the SDK turns each
agent in `handoffs=[...]` into an ordinary function tool
(`transfer_to_refunds`, `transfer_to_tech_support`),
declares it to the model like any other tool,
and the model decides whether to call it.
When it does, conversation ownership transfers:
every following turn runs under the specialist's own instructions,
not the triage agent's.
That is what `test_handoff_transfers_ownership_to_refunds` checks directly —
not just that the final answer sounds right,
but that the second request on the wire carries the refunds agent's system
prompt.
See Trace 25 and Chapter 9 for the mechanism this lab is scripting turn by
turn.

## Why chat.completions, not the Responses API

The OpenAI Agents SDK defaults to OpenAI's Responses API
(`POST /v1/responses`), a different wire shape than chat.completions.
`worksheet_common.mockllm.MockLLM` serves the simpler, well-documented
chat.completions shape on `/v1/chat/completions` and does not speak
Responses.

Verified empirically while building this lab: calling
`agents.set_default_openai_api("chat_completions")` switches the SDK's
default client onto chat.completions with no other changes needed —
`Agent`, `Runner.run_sync`, and handoffs all work unmodified against
MockLLM once that one line is set.
`tests/wire.py` sets it, alongside `set_tracing_disabled(True)`
(the SDK otherwise tries to phone home to OpenAI's tracing endpoint)
and a fresh `AsyncOpenAI(base_url=mock.base_url + "/v1", api_key="test-key")`
pointed at the mock —
`MockLLM.base_url` is the server root, so the `/v1` suffix is added by hand.

`tests/wire.py` also carries `openai_text_response()` and
`openai_tool_call_response()`, two small helpers that build chat.completions
response bodies (`choices[0].message` with `content` or `tool_calls`) for
scripting `MockLLM` turns.
They live in the lab, not in `worksheet_common`,
because this wire shape is specific to this lab's framework choice.

## What the tests check

1. A refund question: the mock scripts the triage turn to call the refunds
   transfer tool, then the refunds agent answers — the final output is the
   refunds agent's text.
2. The handoff actually transferred ownership: the second recorded request's
   system message is the refunds agent's own instructions, and
   `result.last_agent` is the refunds agent, not triage.
3. The same mechanism for tech support, proving routing isn't
   refunds-specific.
4. A question triage can answer directly produces exactly one request —
   no handoff tool gets called, and triage stays the owner.
5. The very first request already lists both transfer tools in its `tools`
   array — handoffs are declared to the model up front, whether or not it
   ends up using one.

There is no live mode for this lab.
A live model would not reliably choose the same handoff on every run,
which is exactly what these tests need to assert deterministically.
