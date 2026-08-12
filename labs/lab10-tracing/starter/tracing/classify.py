"""Lab 10 — your task: classify a recorded session into a failure class.

You are the on-call engineer with 20 production transcripts and no time to
read them one by one. Write detectors, not a model: every class below has a
mechanical, checkable definition. Get 18/20 or better on the fixtures in
../transcripts/ (aim for 20/20 — you designed both sides).
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


def classify(transcript: list[dict]) -> str:
    """Classify `transcript` (a list of message dicts, see
    worksheet_common.transcripts.load_transcript) into one of CLASSES.

    Check in this order — first match wins. A transcript that matches
    none of the five failure definitions is SUCCESS.

    1. TRUNCATION — the transcript's last message has role "assistant",
       carries `"stop_reason": "max_tokens"`, and its `content` (stripped)
       does not end in one of `.`, `!`, `?` (or is empty).

    2. BAD_HANDOFF — some assistant tool_call has name "handoff", AND some
       message anywhere in the transcript (any role) has a `content` that
       contains the literal substring "SPECIALIST_MISMATCH".

    3. RUNAWAY_LOOP — the same tool call — identical `name` AND identical
       `input` (compare with `json.dumps(input, sort_keys=True)`) — appears
       3 or more times among the transcript's assistant tool_calls.

    4. CONTEXT_LOSS — both of:
       a. a tool call with name "Read" appears 2 or more times with the
          same `input` (a re-read of a file already read), AND
       b. some assistant message `content` that ends with "?" (after
          stripping whitespace) is identical, character for character, to
          another assistant message's `content` elsewhere in the
          transcript (the agent asks a question it already asked, i.e.
          already answered).

    5. SWALLOWED_ERROR — both of:
       a. some tool-result message's `content` contains the substring
          "error" (case-insensitive), AND
       b. the transcript's last assistant message's `content` contains
          "successfully" or "done" (case-insensitive).

    6. SUCCESS — none of the above matched.

    Never raise on a well-formed transcript: return your best guess even
    on ambiguous input, but the 20 fixtures are each designed to be
    unambiguous under this exact algorithm.
    """
    raise NotImplementedError("your classifier goes here")
