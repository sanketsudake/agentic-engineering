"""Your work goes here: assemble the micro-agent from the provided parts.

Implement `run_agent()` below. The docstring is the spec; the tests in
`tests/test_practical.py` check exactly what it says. The parts are
provided working — the dispatcher validates and never raises, and the
toolbox's three tools behave. Your job is the loop that wires them to
the model.
"""
from __future__ import annotations

from dataclasses import dataclass, field

from worksheet_common import Model

DONE_MARKER = "DONE:"


@dataclass
class AgentResult:
    answer: str
    transcript: list[dict] = field(default_factory=list)
    stopped: str = "done"  # "done" | "max_turns"


def run_agent(model: Model, dispatcher, toolbox: dict, user_msg: str,
              max_turns: int = 6) -> AgentResult:
    """Run the tool loop against the provided parts. This is the spec.

    Args:
        model: anything with `complete(messages, tools) -> ModelResponse`
            (the `worksheet_common.Model` protocol). Pass it the transcript
            and `toolbox["tool_defs"]`.
        dispatcher: a callable `dispatcher(call, toolbox) -> str`. EVERY
            tool call's result must be exactly what this callable returns —
            never call a registry function directly, and never rewrite what
            the dispatcher hands back (its "error: ..." strings included).
        toolbox: `{"tool_defs": {...}, "registry": {...}}`. Treat it as
            read-only: add, remove, and overwrite nothing in it.
        user_msg: the user's request. The transcript starts as
            `[{"role": "user", "content": user_msg}]`.
        max_turns: the maximum number of model calls.

    Each turn:

    1. Call `model.complete(transcript, toolbox["tool_defs"])`.
    2. Append the assistant message to the transcript as
       `{"role": "assistant", "content": resp.text,
         "tool_calls": [{"id": c.id, "name": c.name, "input": c.input}, ...]}`.
    3. The DONE marker — the early stop. Unlike Lab 3's model, this exam's
       model may return text AND tool calls in one response. If `resp.text`
       contains `DONE_MARKER`, stop immediately: dispatch NO tool call from
       that response, and return `AgentResult` with `answer` set to the text
       after the first marker (whitespace-stripped) and `stopped="done"`.
    4. Otherwise, if the response has no tool calls, return `AgentResult`
       with `answer=resp.text or ""` and `stopped="done"`.
    5. Otherwise send each tool call through `dispatcher(call, toolbox)`,
       in the order the model emitted them, and append one message per
       call: `{"role": "tool", "tool_call_id": call.id,
               "content": <the dispatcher's string>}`. Then loop.

    If `max_turns` model calls happen without a stop, return `AgentResult`
    with `answer=""` and `stopped="max_turns"`.
    """
    raise NotImplementedError("your loop goes here — the docstring above is the spec")
