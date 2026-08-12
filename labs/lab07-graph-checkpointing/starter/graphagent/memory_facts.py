"""Lab 7 helper: pull the fact under test out of a message list.

Provided and working — this lab is about the graph, not this helper. Tests
use it so assertions read "the fact from turn one is still there" instead
of reaching into message internals directly.
"""
from __future__ import annotations

from langchain_core.messages import BaseMessage


def extract_fact(messages: list[BaseMessage]) -> str | None:
    """Return the content of the first human message, or None if there is none.

    A stand-in for the real extraction step in Trace 13 (harness sends the
    transcript to the LLM, gets back candidate facts). Here it is a plain
    lookup: enough to prove, in a test, that a fact from an earlier turn
    round-tripped through the checkpointer.
    """
    for message in messages:
        if getattr(message, "type", None) == "human":
            return str(message.content)
    return None
