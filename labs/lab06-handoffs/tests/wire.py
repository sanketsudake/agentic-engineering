"""OpenAI chat.completions wire-shape helpers, plus SDK<->mock wiring, for Lab 6.

The OpenAI Agents SDK defaults to OpenAI's Responses API
(`POST /v1/responses`, a different wire shape than chat.completions).
`worksheet_common.mockllm.MockLLM` serves the well-documented, simpler
chat.completions shape on `/v1/chat/completions` (see its `_KNOWN_PATHS`)
and does not speak Responses.

Verified empirically (see the lab's build notes / README): calling
`agents.set_default_openai_api("chat_completions")` switches the SDK's
default OpenAI client onto chat.completions with zero other changes —
`Agent`, `Runner.run_sync`, and handoffs all work unmodified against
MockLLM once that one line is set. That is the choice this lab makes,
and the only reason this file exists instead of importing response
builders from `worksheet_common` directly: chat.completions payloads are
lab-specific wire shapes, not something the shared harness needs to own.
"""
from __future__ import annotations

import json
from contextlib import contextmanager

from agents import set_default_openai_api, set_default_openai_client, set_tracing_disabled
from openai import AsyncOpenAI

from worksheet_common.mockllm import MockLLM


def openai_text_response(
    text: str,
    *,
    id: str = "chatcmpl-mock",
    model: str = "gpt-mock",
) -> dict:
    """Build a minimally-valid `chat.completions` response with a text answer.

    This is a final turn: no tool calls, `finish_reason: "stop"`. The Agents
    SDK reads `choices[0].message.content` as the agent's final output.
    """
    return {
        "id": id,
        "object": "chat.completion",
        "created": 0,
        "model": model,
        "choices": [
            {
                "index": 0,
                "message": {"role": "assistant", "content": text},
                "finish_reason": "stop",
            }
        ],
        "usage": {"prompt_tokens": 10, "completion_tokens": 10, "total_tokens": 20},
    }


def openai_tool_call_response(
    fn_name: str,
    args: dict,
    *,
    call_id: str = "call_mock",
    id: str = "chatcmpl-mock",
    model: str = "gpt-mock",
) -> dict:
    """Build a `chat.completions` response that calls one function/tool.

    `fn_name` is the tool name the model chose to call — for a handoff, that
    is the SDK-generated transfer tool (`agents.Handoff.default_tool_name`,
    e.g. `"transfer_to_refunds"`). `finish_reason: "tool_calls"` is what
    tells the SDK to dispatch instead of treating `content` as final output.
    """
    return {
        "id": id,
        "object": "chat.completion",
        "created": 0,
        "model": model,
        "choices": [
            {
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": None,
                    "tool_calls": [
                        {
                            "id": call_id,
                            "type": "function",
                            "function": {"name": fn_name, "arguments": json.dumps(args)},
                        }
                    ],
                },
                "finish_reason": "tool_calls",
            }
        ],
        "usage": {"prompt_tokens": 10, "completion_tokens": 10, "total_tokens": 20},
    }


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
