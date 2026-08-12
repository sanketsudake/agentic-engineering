"""Lab 10 — your task: cost a session, then cost a solve.

The taxonomy in classify.py tells you WHAT failed. This file answers the
question an operator actually gets asked: what did it cost us? Failures
still burn tokens — a team that only counts cost on successful sessions is
blind to the cost of a runaway loop or a swallowed error.
"""
from __future__ import annotations


def session_cost(transcript: list[dict], price_in: float, price_out: float) -> float:
    """Sum the token cost of one session.

    Walk every message with role "assistant". If it carries a `"usage"`
    dict (`{"input_tokens": N, "output_tokens": N}`), add
    `input_tokens * price_in + output_tokens * price_out` to the running
    total. Assistant messages with no `usage` dict contribute 0.

    `price_in` / `price_out` are USD per token (already divided down from
    a per-million-token quote — e.g. a $3/MTok input price is
    `price_in = 3.0 / 1_000_000`).

    Returns the total as a float.
    """
    raise NotImplementedError("sum usage tokens x price here")


def cost_per_solve(
    transcripts: dict[str, list[dict]],
    labels_or_classifier,
    price_in: float,
    price_out: float,
) -> float:
    """Total cost of ALL sessions, divided by the number of SUCCESS sessions.

    `transcripts` maps session id -> transcript (list of message dicts).

    `labels_or_classifier` is either:
    - a dict mapping session id -> class name (e.g. tests/labels.py's
      ground truth), or
    - a callable `classify(transcript) -> class_name`
      (e.g. `tracing.classify.classify`).

    Compute each session's cost with `session_cost`, sum them, then divide
    by the count of sessions whose class is "SUCCESS". This is the point
    of the whole exercise: failed sessions still cost money, so the true
    cost of getting one task done is total spend over solved tasks, not
    total spend over total requests.

    Raise `ValueError` if there are zero SUCCESS sessions (cost per solve
    is undefined — you cannot divide by zero solves).
    """
    raise NotImplementedError("total cost / number of SUCCESS sessions")
