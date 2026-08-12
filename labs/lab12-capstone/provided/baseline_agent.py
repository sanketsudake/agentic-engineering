"""The release baseline: a vendored copy of Lab 3's solution loop, adapted
to Lab 8's tasks (Lab 8's `good_agent.py`, renamed).

`run_task()` builds a `ScriptedModel` from the task's script, runs the loop
against it, hands back the result. A tool exception is surfaced to the
model as "error: <message>" — the model can only fix what it can see
(Lab 3, Q 1.4). This is the agent already running in production; the gate
in `release/gate.py` decides whether a candidate may replace it.
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
                except Exception as exc:  # surface, never crash: the model
                    content = f"error: {exc}"  # can only fix what it sees
            transcript.append({"role": "tool", "tool_call_id": call.id,
                               "content": content})
    return AgentResult(answer="", transcript=transcript, stopped="max_turns")


def run_task(task: dict) -> AgentResult:
    """Run one Lab 12 task through the baseline tool loop."""
    model = ScriptedModel(task["script"])
    return run_agent(model, TOOLS, task["question"])
