"""Deterministic token counting for Lab 4.

No real tokenizer: a fixed, auditable rule so every test result is exact and
reproducible offline. Identical in starter/ and solution/ — this file is
provided, not part of your task.
"""
from __future__ import annotations

OVERHEAD_TOKENS = 4  # fixed per-message role/framing overhead


def count_tokens(text: str) -> int:
    """Approximate token count for `text`: ~1 token per 4 characters, floor 1.

    The floor of 1 means even an empty string costs one token — there is no
    such thing as a free message.
    """
    return max(1, len(text) // 4)


def message_tokens(message: dict) -> int:
    """Total token cost of one transcript message: content tokens + overhead.

    `message["content"]` may be None (an assistant message that only carries
    tool_calls); that is treated as content="".
    """
    content = message.get("content") or ""
    return count_tokens(content) + OVERHEAD_TOKENS


def total_tokens(messages: list) -> int:
    """Sum of `message_tokens` over a list of messages."""
    return sum(message_tokens(m) for m in messages)
