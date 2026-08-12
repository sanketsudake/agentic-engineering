"""Provided graders (Lab 8's shape; Chapter 10). Working — do not edit.

Each grader takes the finished `transcript` (the list of message dicts
`run_agent()` produces) and the `task` dict it was run against, and
returns a float in [0.0, 1.0]. Two are outcome-level (`exact`,
`trajectory`); one is transcript-level (`paired`). The suite is
deterministic, so no LLM judge is needed here.
"""
from __future__ import annotations


def _final_answer(transcript: list[dict]) -> str:
    """The text of the transcript's last assistant message."""
    for msg in reversed(transcript):
        if msg["role"] == "assistant" and msg.get("content"):
            return msg["content"]
    return ""


def _tool_call_names(transcript: list[dict]) -> list[str]:
    """Every tool name the agent called, in call order."""
    names: list[str] = []
    for msg in transcript:
        if msg["role"] == "assistant":
            names.extend(call["name"] for call in msg.get("tool_calls") or [])
    return names


def _is_subsequence(required: list[str], actual: list[str]) -> bool:
    """True if `required` appears in `actual`, in order (gaps allowed)."""
    pos = 0
    for name in actual:
        if pos < len(required) and name == required[pos]:
            pos += 1
    return pos == len(required)


def exact_grader(transcript: list[dict], task: dict) -> float:
    """1.0 if the agent's final answer equals `task["expected_answer"]`."""
    return 1.0 if _final_answer(transcript) == task["expected_answer"] else 0.0


def trajectory_grader(transcript: list[dict], task: dict) -> float:
    """1.0 if `task["required_tools"]` were called, in order, as a subsequence."""
    return 1.0 if _is_subsequence(task["required_tools"], _tool_call_names(transcript)) else 0.0


def paired_results_grader(transcript: list[dict], task: dict) -> float:
    """Transcript-level check (Chapter 10): every tool call the agent made
    has a matching tool result somewhere in the transcript.

    An unmatched call means the model acted without ever seeing what its
    tool did — the transcript shape itself is the evidence, whatever the
    final answer says.
    """
    called: set[str] = set()
    answered: set[str] = set()
    for msg in transcript:
        if msg["role"] == "assistant":
            called.update(call["id"] for call in msg.get("tool_calls") or [])
        elif msg["role"] == "tool":
            answered.add(msg["tool_call_id"])
    return 1.0 if called <= answered else 0.0


def default_graders() -> dict:
    """The grader set every eval run in this practical uses."""
    return {
        "exact": exact_grader,
        "trajectory": trajectory_grader,
        "paired": paired_results_grader,
    }
