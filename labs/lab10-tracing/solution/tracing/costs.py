"""Reference solution for Lab 10: cost a session, then cost a solve.

See starter/tracing/costs.py for the full spec.
"""
from __future__ import annotations


def session_cost(transcript: list[dict], price_in: float, price_out: float) -> float:
    total = 0.0
    for m in transcript:
        if m.get("role") != "assistant":
            continue
        usage = m.get("usage") or {}
        total += usage.get("input_tokens", 0) * price_in
        total += usage.get("output_tokens", 0) * price_out
    return total


def cost_per_solve(
    transcripts: dict[str, list[dict]],
    labels_or_classifier,
    price_in: float,
    price_out: float,
) -> float:
    total = sum(
        session_cost(transcript, price_in, price_out)
        for transcript in transcripts.values()
    )

    if callable(labels_or_classifier):
        classes = {sid: labels_or_classifier(t) for sid, t in transcripts.items()}
    else:
        classes = labels_or_classifier

    successes = sum(1 for sid in transcripts if classes.get(sid) == "SUCCESS")
    if successes == 0:
        raise ValueError("no SUCCESS sessions: cost per solve is undefined")
    return total / successes
