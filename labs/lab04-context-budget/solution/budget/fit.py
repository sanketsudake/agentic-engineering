"""Reference solution for Lab 4: keep a transcript under a token budget."""
from __future__ import annotations

from .tokens import message_tokens

TOOL_TRUNCATE_TOKENS = 600  # a tool message over this many tokens gets cut
TRUNCATE_MARKER = "\n[truncated]"


def _truncate_tool_messages(messages: list[dict]) -> list[dict]:
    """Return a copy of `messages` with oversized tool results cut.

    Unconditional: runs before any budget check (rule 3).
    """
    out = []
    limit_chars = TOOL_TRUNCATE_TOKENS * 4
    for m in messages:
        if m.get("role") == "tool":
            content = m.get("content") or ""
            if len(content) // 4 > TOOL_TRUNCATE_TOKENS:
                m = {**m, "content": content[:limit_chars] + TRUNCATE_MARKER}
        out.append(m)
    return out


def _segment_turns(rest: list[dict]) -> list[list[dict]]:
    """Group messages after the task into turns.

    A turn is an assistant message plus the tool messages immediately
    following it, or a single user message.
    """
    turns: list[list[dict]] = []
    i, n = 0, len(rest)
    while i < n:
        m = rest[i]
        if m.get("role") == "assistant":
            turn = [m]
            j = i + 1
            while j < n and rest[j].get("role") == "tool":
                turn.append(rest[j])
                j += 1
            turns.append(turn)
            i = j
        else:
            turns.append([m])
            i += 1
    return turns


def _marker(n_dropped: int) -> dict:
    return {"role": "system", "content": f"[context compacted: {n_dropped} messages dropped]"}


def fit_context(messages: list[dict], budget: int) -> list[dict]:
    system, task = messages[0], messages[1]
    rest = _truncate_tool_messages(messages[2:])
    turns = _segment_turns(rest)

    base_cost = message_tokens(system) + message_tokens(task)

    def turns_cost(turn_list: list[list[dict]]) -> int:
        return sum(message_tokens(m) for t in turn_list for m in t)

    # Try with everything kept, no marker (rule 1: nothing dropped yet).
    if base_cost + turns_cost(turns) <= budget:
        return [system, task, *(m for t in turns for m in t)]

    # Drop turns oldest-first until system + task + marker + kept turns fit.
    kept = list(turns)
    total_msgs = sum(len(t) for t in turns)
    while kept:
        n_dropped = total_msgs - sum(len(t) for t in kept)
        marker = _marker(n_dropped)
        cost = base_cost + message_tokens(marker) + turns_cost(kept)
        if cost <= budget:
            return [system, task, marker, *(m for t in kept for m in t)]
        kept.pop(0)  # drop the oldest surviving turn

    # Nothing left but system + task + marker.
    marker = _marker(total_msgs)
    if base_cost + message_tokens(marker) <= budget:
        return [system, task, marker]

    raise ValueError("budget too small")
