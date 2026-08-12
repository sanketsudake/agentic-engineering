"""The working agent: a vendored copy of Lab 3's solution loop.

`run_task()` adapts it to Lab 8's tasks: build a `ScriptedModel` from the
task's script, run the loop against it, hand back the result. A tool
exception is surfaced to the model as "error: <message>" — the model can
only fix what it can see (Lab 3, Q 1.4).
"""
from __future__ import annotations

from dataclasses import dataclass, field

from worksheet_common import Model, ScriptedModel

from agents_under_test.tools import TOOLS


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
                except Exception as exc:  # surface, never crash: the model
                    content = f"error: {exc}"  # can only fix what it sees
            transcript.append({"role": "tool", "tool_call_id": call.id,
                               "content": content})
    return AgentResult(answer="", transcript=transcript, stopped="max_turns")


def run_task(task: dict) -> AgentResult:
    """Run one Lab 8 task through the working tool loop."""
    model = ScriptedModel(task["script"])
    return run_agent(model, TOOLS, task["question"])
