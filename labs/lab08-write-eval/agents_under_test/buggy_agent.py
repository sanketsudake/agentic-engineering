"""The planted-bug variant: identical to `good_agent`, with one line changed.

A tool exception becomes a silent "" instead of "error: <message>". The
harness never crashes and the transcript stays well-formed — the loop
"works". But the model never learns the tool failed, so on any task where
the first tool call is wrong, this agent confidently answers as if it had
succeeded. That silent difference is exactly what Lab 8's graders must
catch (Trace 10; Trace 27).
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
                except Exception:  # BUG: swallowed — the model sees "",
                    content = ""  # indistinguishable from an empty success
            transcript.append({"role": "tool", "tool_call_id": call.id,
                               "content": content})
    return AgentResult(answer="", transcript=transcript, stopped="max_turns")


def run_task(task: dict) -> AgentResult:
    """Run one Lab 8 task through the buggy tool loop."""
    model = ScriptedModel(task["script"])
    return run_agent(model, TOOLS, task["question"])
