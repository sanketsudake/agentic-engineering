"""A candidate release with a harmless change: `baseline_agent` plus a more
detailed tool-error message.

Identical to `baseline_agent`, with one line changed: the error result
names the tool that failed, e.g. "error: no such item: gadgets
(tool=lookup_price)" instead of "error: no such item: gadgets". The
message still starts with "error", so the scripted tasks in
`provided/tasks.py` still route to their `on_error` branch — the retry
happens exactly as before, every expected answer is unchanged. This is
the shape of most real releases: a genuine code diff that should not move
any eval score. `release_gate()` must let it through (Trace 33, Trace 34).
"""
from __future__ import annotations

from dataclasses import dataclass, field

from worksheet_common import Model, ScriptedModel

from provided.tools import TOOLS


@dataclass
class AgentResult:
    answer: str
    transcript: list[dict] = field(default_factory=list)
    stopped: str = "done"  # "done" | "max_turns"


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
                except Exception as exc:  # surface, never crash, and name
                    content = f"error: {exc} (tool={call.name})"  # the tool
            transcript.append({"role": "tool", "tool_call_id": call.id,
                               "content": content})
    return AgentResult(answer="", transcript=transcript, stopped="max_turns")


def run_task(task: dict) -> AgentResult:
    """Run one Lab 12 task through the improved candidate's tool loop."""
    model = ScriptedModel(task["script"])
    return run_agent(model, TOOLS, task["question"])
