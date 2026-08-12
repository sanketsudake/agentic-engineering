"""Lab 3 — your task: implement the tool loop (Trace 2, steps 2-8).

You are the harness. The model proposes; you dispose.
"""
from __future__ import annotations

from dataclasses import dataclass, field

from worksheet_common import Model


@dataclass
class AgentResult:
    answer: str
    transcript: list[dict] = field(default_factory=list)
    stopped: str = "done"  # "done" | "max_turns"


def run_agent(model: Model, tools: dict, user_msg: str, max_turns: int = 8) -> AgentResult:
    """Run the agent loop until the model answers or the turn budget runs out.

    The transcript is a list of message dicts, in order:

    - the user message:      {"role": "user", "content": user_msg}
    - each assistant turn:   {"role": "assistant", "content": text_or_None,
                              "tool_calls": [{"id", "name", "input"}, ...]}
    - each tool result:      {"role": "tool", "tool_call_id": id, "content": str}

    The contract, in loop order:

    1. Append the user message, then call `model.complete(transcript, tools)`.
    2. Append the assistant message (serialize its tool_calls as dicts).
    3. If the response has tool calls, dispatch each IN ORDER:
       - unknown tool name        -> content "error: unknown tool <name>"
       - the tool raises          -> content "error: <exception message>"
       - bad/missing arguments    -> also an error result, never a crash
       Every dispatch appends one tool-result message, then loop to step 1's
       model call again (do NOT re-append the user message).
    4. If the response has final text instead, return AgentResult(answer=text,
       stopped="done").
    5. If `max_turns` model calls happen without a final answer, stop and
       return AgentResult(answer="", stopped="max_turns").

    Errors go INTO the transcript as tool results — the model can only fix
    what it can see (Q 1.4 in the book is about exactly this).
    """
    raise NotImplementedError("your loop goes here")
