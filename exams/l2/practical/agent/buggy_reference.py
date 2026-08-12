"""A frozen agent variant that mishandles oversized tool results.

DO NOT EDIT OR DELETE THIS FILE, and do not import it from `agent/loop.py`.
It is deliberately self-contained: `tests/test_practical.py` re-plants the
bug class by running your regression task against this module. A
regression task that cannot fail this agent would not catch the bug class
if it ever returned to `agent/loop.py`.
"""
from __future__ import annotations

from dataclasses import dataclass, field

from worksheet_common import Model, ScriptedModel

from agent.tools import TOOLS

RESULT_BUDGET = 400  # characters per tool result


@dataclass
class AgentResult:
    answer: str
    transcript: list[dict] = field(default_factory=list)
    stopped: str = "done"  # "done" | "max_turns"


def run_agent(model: Model, tools: dict, user_msg: str, max_turns: int = 6) -> AgentResult:
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
                except Exception as exc:
                    content = f"error: {exc}"
            if len(content) > RESULT_BUDGET:
                continue  # the planted bug class: the result never reaches the model
            transcript.append({"role": "tool", "tool_call_id": call.id,
                               "content": content})
    return AgentResult(answer="", transcript=transcript, stopped="max_turns")


def run_task(task: dict) -> AgentResult:
    """Run one task through the frozen buggy loop."""
    model = ScriptedModel(task["script"], cycle=task.get("cycle", False))
    return run_agent(model, TOOLS, task["question"])
