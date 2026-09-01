"""SDK<->mock wiring for Lab 6.

The OpenAI Agents SDK defaults to OpenAI's Responses API
(`POST /v1/responses`, a different wire shape than chat.completions).
`worksheet_common.mockllm.MockLLM` serves the well-documented, simpler
chat.completions shape on `/v1/chat/completions` (see its `_KNOWN_PATHS`)
and does not speak Responses.

Verified empirically (see the lab's build notes / README): calling
`agents.set_default_openai_api("chat_completions")` switches the SDK's
default OpenAI client onto chat.completions with zero other changes —
`Agent`, `Runner.run_sync`, and handoffs all work unmodified against
MockLLM once that one line is set. That is the choice this lab makes.

The chat.completions response builders (`openai_text_response`,
`openai_tool_call_response`) live in `worksheet_common.mockllm` next to
their Anthropic-shaped siblings; they are re-exported here so the lab's
tests keep one import point for all wire concerns.
"""
from __future__ import annotations

from contextlib import contextmanager

from agents import set_default_openai_api, set_default_openai_client, set_tracing_disabled
from openai import AsyncOpenAI

from worksheet_common.mockllm import (  # noqa: F401 (re-exported for tests)
    MockLLM,
    openai_text_response,
    openai_tool_call_response,
)


@contextmanager
def mock_provider(turns: list[dict]):
    """Start `MockLLM` on `turns` and point the Agents SDK's default client at it.

    Every test needs this: it disables tracing (the SDK otherwise tries to
    phone home to OpenAI's tracing endpoint), switches the SDK to the
    chat.completions API (see module docstring), and wires a fresh
    `AsyncOpenAI` client at the mock's `base_url` — done fresh on every call
    because `MockLLM` binds a new port each time and the SDK's default
    client is process-global state, not per-run.

    `MockLLM.base_url` is the server root; the OpenAI SDK's `base_url` must
    end in `/v1`, so this appends it.
    """
    set_tracing_disabled(True)
    set_default_openai_api("chat_completions")
    with MockLLM(turns) as mock:
        client = AsyncOpenAI(base_url=mock.base_url + "/v1", api_key="test-key")
        set_default_openai_client(client, use_for_tracing=False)
        yield mock
