"""Reference solution for Lab 5: the same tool loop, with three bugs fixed.

- Tool results over MAX_RESULT_CHARS are truncated (no context flood).
- A timed-out tool is never re-executed (no non-idempotent retry).
- A tool exception is surfaced as an error, never swallowed as success.
"""
from __future__ import annotations

from dataclasses import dataclass, field

from worksheet_common import Model

MAX_RESULT_CHARS = 2000
TIMEOUT_SECONDS = 5


@dataclass
class AgentResult:
    answer: str
    transcript: list[dict] = field(default_factory=list)
    stopped: str = "done"  # "done" | "max_turns"


def _truncate(content: str) -> str:
    if len(content) <= MAX_RESULT_CHARS:
        return content
    return content[:MAX_RESULT_CHARS] + f"\n[truncated: result was {len(content)} chars]"


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
                    content = _truncate(str(fn(**call.input)))
                except TimeoutError:
                    # Do not re-execute: the tool may not be idempotent.
                    # Surface the failure and let the model decide.
                    content = f"error: timed out after {TIMEOUT_SECONDS}s"
                except Exception as exc:
                    content = f"error: {exc}"
            transcript.append({"role": "tool", "tool_call_id": call.id,
                               "content": content})
    return AgentResult(answer="", transcript=transcript, stopped="max_turns")
