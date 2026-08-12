"""Optional live check: same `ask()` against the real API.

Deselected by default (`addopts = "-m 'not live'"` in pyproject.toml) and
skipped outright with no ANTHROPIC_API_KEY, so `uv sync && uv run pytest`
never needs a key or a network call. Run explicitly with:

    ANTHROPIC_API_KEY=sk-... uv run pytest -m live
"""
import os

import anthropic
import pytest

pytestmark = [
    pytest.mark.live,
    pytest.mark.skipif(
        not os.environ.get("ANTHROPIC_API_KEY"),
        reason="set ANTHROPIC_API_KEY to run the live check",
    ),
]


def test_ask_against_real_api(calls, monkeypatch):
    # calls.MODEL is "claude-mock", which only the mock server understands.
    # Swap in a real model id for this one test; ask() resolves MODEL at
    # call time, so patching the module attribute is enough.
    monkeypatch.setattr(calls, "MODEL", "claude-opus-5")
    client = anthropic.Anthropic()  # real base_url, real ANTHROPIC_API_KEY
    answer = calls.ask(client, "Reply with exactly one word: hello")
    assert isinstance(answer, str) and answer.strip()
