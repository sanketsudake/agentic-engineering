"""Reference solution for Lab 10: classify a session into a failure class.

See starter/tracing/classify.py for the full spec — the six mechanical
definitions this function implements, in priority order.
"""
from __future__ import annotations

import json

CLASSES = (
    "SUCCESS",
    "RUNAWAY_LOOP",
    "SWALLOWED_ERROR",
    "CONTEXT_LOSS",
    "BAD_HANDOFF",
    "TRUNCATION",
)


def _assistant_messages(transcript):
    return [m for m in transcript if m.get("role") == "assistant"]


def _tool_calls(transcript):
    calls = []
    for m in _assistant_messages(transcript):
        calls.extend(m.get("tool_calls") or [])
    return calls


def _call_key(call):
    return (call["name"], json.dumps(call.get("input", {}), sort_keys=True))


def _is_truncated(transcript) -> bool:
    if not transcript:
        return False
    last = transcript[-1]
    if last.get("role") != "assistant" or last.get("stop_reason") != "max_tokens":
        return False
    text = (last.get("content") or "").strip()
    return not text.endswith((".", "!", "?"))


def _is_bad_handoff(transcript) -> bool:
    has_handoff = any(c["name"] == "handoff" for c in _tool_calls(transcript))
    if not has_handoff:
        return False
    return any("SPECIALIST_MISMATCH" in (m.get("content") or "") for m in transcript)


def _is_runaway_loop(transcript) -> bool:
    counts: dict[tuple, int] = {}
    for call in _tool_calls(transcript):
        key = _call_key(call)
        counts[key] = counts.get(key, 0) + 1
    return any(n >= 3 for n in counts.values())


def _is_context_loss(transcript) -> bool:
    read_counts: dict[tuple, int] = {}
    for call in _tool_calls(transcript):
        if call["name"] == "Read":
            key = _call_key(call)
            read_counts[key] = read_counts.get(key, 0) + 1
    duplicate_read = any(n >= 2 for n in read_counts.values())
    if not duplicate_read:
        return False

    questions = [
        m["content"] for m in _assistant_messages(transcript)
        if m.get("content") and m["content"].strip().endswith("?")
    ]
    repeated_question = len(questions) != len(set(questions))
    return repeated_question


def _is_swallowed_error(transcript) -> bool:
    has_tool_error = any(
        m.get("role") == "tool" and "error" in (m.get("content") or "").lower()
        for m in transcript
    )
    if not has_tool_error:
        return False
    assistants = _assistant_messages(transcript)
    if not assistants:
        return False
    final_text = (assistants[-1].get("content") or "").lower()
    return "successfully" in final_text or "done" in final_text


def classify(transcript: list[dict]) -> str:
    if _is_truncated(transcript):
        return "TRUNCATION"
    if _is_bad_handoff(transcript):
        return "BAD_HANDOFF"
    if _is_runaway_loop(transcript):
        return "RUNAWAY_LOOP"
    if _is_context_loss(transcript):
        return "CONTEXT_LOSS"
    if _is_swallowed_error(transcript):
        return "SWALLOWED_ERROR"
    return "SUCCESS"
