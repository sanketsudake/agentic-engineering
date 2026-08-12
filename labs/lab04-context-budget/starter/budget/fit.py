"""Lab 4 — your task: keep a transcript under a token budget without losing
the task.

You are the compactor the harness calls before every model turn: given the
running transcript and a hard token budget, return a transcript that still
fits — and still lets the model finish the job.
"""
from __future__ import annotations

from .tokens import message_tokens

TOOL_TRUNCATE_TOKENS = 600  # a tool message over this many tokens gets cut
TRUNCATE_MARKER = "\n[truncated]"


def fit_context(messages: list[dict], budget: int) -> list[dict]:
    """Return a NEW transcript that fits in `budget` tokens, in priority order.

    `messages` is a transcript: dicts with `role` in {"system", "user",
    "assistant", "tool"} and a `content` string (an assistant message may
    also carry `tool_calls`; its `content` may be None). `messages[0]` is
    always the SYSTEM message. `messages[1]` is always the TASK — the first
    user message, the reason the session exists.

    The contract, in priority order:

    1. Never drop or alter the system message (`messages[0]`) or the task
       message (`messages[1]`). They are always the first two messages of
       the result, verbatim.
    2. Never exceed `budget`: the sum of `message_tokens(m)` (see
       `tokens.py`) over every message in the result — kept messages plus
       any inserted marker — must be <= `budget`.
    3. Truncate oversized TOOL results first, unconditionally — before
       looking at the total budget at all. Any message with
       `role == "tool"` whose `content` exceeds `TOOL_TRUNCATE_TOKENS`
       (600) tokens is cut to the first `TOOL_TRUNCATE_TOKENS * 4`
       characters, with `TRUNCATE_MARKER` ("\\n[truncated]") appended. This
       runs on every tool message in the transcript, even ones from
       `messages[2:]` in a session that ends up under budget overall — a
       6,000-character tool dump gets cut whether or not the session needs
       it, because the harness that calls this function cannot know in
       advance whether a later turn will blow the budget.
    4. If the transcript (after step 3) still exceeds `budget`, drop whole
       conversation TURNS, oldest-first, from *after* the task message.
       A turn is either:
         - an assistant message plus every tool message immediately
           following it (its tool results), or
         - a single user message.
       Drop entire turns only — never split a turn apart, and never touch
       `messages[0]` or `messages[1]`.
    5. The moment any message is dropped (step 4), insert exactly one marker
       message right after the task message:
       `{"role": "system", "content": "[context compacted: N messages
       dropped]"}`, where N is the total count of individual messages
       removed (not turns). This marker's own cost counts against
       `budget` too. If nothing is dropped, no marker is inserted.
    6. Keep the most recent turns intact (uncut) — turns are dropped
       oldest-first, so whatever survives is the tail of the session.
    7. If system + task + marker alone cannot fit in `budget`, raise
       `ValueError("budget too small")` — there is no valid result.

    Returns a NEW list. `messages` (and its message dicts) are never
    mutated — the harness may need the original transcript for logging.
    """
    raise NotImplementedError("your budgeter goes here")
