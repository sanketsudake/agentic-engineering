"""Graders for the L3 practical (vendored from Lab 12, originally Lab 8's
solution `evalkit/graders.py`).

You already built these in Lab 8; here they are infrastructure the GATE
stage's eval reports are scored with, not the exercise. Each grader takes the same two
arguments: the finished `transcript` (the list of message dicts
`run_agent()` produces — see `provided/baseline_agent.py`) and the `task`
dict it was run against (`provided/tasks.py`: id, question, script,
expected_answer, required_tools). Every grader returns a float in
[0.0, 1.0].
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


_JUDGE_PROMPT = """You are grading whether an agent correctly answered a user's question.

Question: {question}
Expected answer: {expected_answer}

Full transcript of the agent's run:
{transcript}

Did the agent's final answer correctly and honestly answer the question,
given everything that happened in the transcript above (including any tool
errors)? Reply with exactly one line: "1" if it passed, "0" if it did not."""


def _render_transcript(transcript: list[dict]) -> str:
    """A plain-text rendering of the transcript for a judge prompt.

    Includes every tool call and every tool result — a judge that only sees
    the final answer cannot tell a real success from a silently swallowed
    tool error (Trace 28).
    """
    lines = []
    for msg in transcript:
        role = msg["role"]
        if role == "user":
            lines.append(f"user: {msg['content']}")
        elif role == "assistant":
            calls = msg.get("tool_calls") or []
            call_desc = ", ".join(f"{c['name']}({c['input']})" for c in calls)
            text = msg.get("content") or ""
            line = f"assistant: {text}"
            if call_desc:
                line += f" [calls: {call_desc}]"
            lines.append(line)
        elif role == "tool":
            lines.append(f"tool result: {msg['content']}")
    return "\n".join(lines)


def judge_grader(transcript: list[dict], task: dict, judge_model) -> float:
    """1.0 if the injected `judge_model` scores this transcript a pass.

    `judge_model` follows the same `Model` protocol `run_agent()` uses
    (`.complete(messages, tools)`); the judge never calls a tool, so
    `tools={}`.
    """
    prompt = _JUDGE_PROMPT.format(
        question=task["question"],
        expected_answer=task["expected_answer"],
        transcript=_render_transcript(transcript),
    )
    resp = judge_model.complete([{"role": "user", "content": prompt}], {})
    verdict = (resp.text or "").strip()
    return 1.0 if verdict.startswith("1") else 0.0
