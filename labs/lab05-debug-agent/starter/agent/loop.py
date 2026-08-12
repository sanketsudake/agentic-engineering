"""Lab 5 — your task: find and fix three bugs in this agent loop.

This loop runs. It dispatches tools, handles unknown tools, retries on
timeout, and never crashes on a bad tool call. Read the failing tests in
tests/test_lab.py: each one names one bug and states the correct behavior.
"""
from __future__ import annotations

from dataclasses import dataclass, field

from worksheet_common import Model

TIMEOUT_SECONDS = 5


@dataclass
class AgentResult:
    answer: str
    transcript: list[dict] = field(default_factory=list)
    stopped: str = "done"  # "done" | "max_turns"


def _safe_call(fn, call) -> str:
    """Run a tool call and never let it blow up the conversation."""
    try:
        return str(fn(**call.input))
    except Exception:
        return ""


def run_agent(model: Model, tools: dict, user_msg: str, max_turns: int = 8) -> AgentResult:
    transcript: list[dict] = [{"role": "user", "content": user_msg}]
    for _ in range(max_turns):
        resp = model.complete(transcript, tools)
        transcript.append({
            "role": "assistant",
            "content": resp.text,
            "tool_calls": [{"id": c.id, "name": c.name, "input": c.input}
                           for c in resp.tool_calls],
        })
        if not resp.tool_calls:
            return AgentResult(answer=resp.text or "", transcript=transcript,
                               stopped="done")
        for call in resp.tool_calls:
            fn = tools.get(call.name)
            if fn is None:
                content = f"error: unknown tool {call.name}"
            else:
                try:
                    content = str(fn(**call.input))
                except TimeoutError:
                    # Tools can be flaky under load — give the call one
                    # more chance before giving up on it.
                    content = _safe_call(fn, call)
                except Exception:
                    content = ""
            transcript.append({"role": "tool", "tool_call_id": call.id,
                               "content": content})
    return AgentResult(answer="", transcript=transcript, stopped="max_turns")
