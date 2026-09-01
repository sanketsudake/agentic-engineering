"""Optional live checks: same `ask()` against a real API, either provider.

Deselected by default (`addopts = "-m 'not live'"` in pyproject.toml) and
each test skips outright when its provider's key is unset, so
`uv sync && uv run pytest` never needs a key or a network call. Run
explicitly with a real key:

    ANTHROPIC_API_KEY=sk-... uv run pytest -m live
    OPENAI_API_KEY=sk-... OPENAI_LIVE_MODEL=<model-id> uv run pytest -m live

The OpenAI test takes its model id from `OPENAI_LIVE_MODEL` instead of
hardcoding one, and both SDKs honor their base-url env vars
(`ANTHROPIC_BASE_URL`, `OPENAI_BASE_URL`) — so any OpenAI-compatible
endpoint (Ollama, vLLM, OpenRouter, ...) can serve the OpenAI live check.
"""
import os

import anthropic
import openai
import pytest

pytestmark = [pytest.mark.live]


@pytest.mark.skipif(
    not os.environ.get("ANTHROPIC_API_KEY"),
    reason="set ANTHROPIC_API_KEY to run the Anthropic live check",
)
def test_ask_against_real_api(calls, monkeypatch):
    # calls.MODEL is "claude-mock", which only the mock server understands.
    # Swap in a real model id for this one test; ask() resolves MODEL at
    # call time, so patching the module attribute is enough.
    monkeypatch.setattr(calls, "MODEL", "claude-opus-5")
    client = anthropic.Anthropic()  # real base_url, real ANTHROPIC_API_KEY
    answer = calls.ask(client, "Reply with exactly one word: hello")
    assert isinstance(answer, str) and answer.strip()


@pytest.mark.skipif(
    not (os.environ.get("OPENAI_API_KEY") and os.environ.get("OPENAI_LIVE_MODEL")),
    reason="set OPENAI_API_KEY and OPENAI_LIVE_MODEL (a real model id) to run the OpenAI live check",
)
def test_ask_against_real_openai_api(openai_calls, monkeypatch):
    # Same swap as above: "gpt-mock" only means something to the mock server.
    monkeypatch.setattr(openai_calls, "MODEL", os.environ["OPENAI_LIVE_MODEL"])
    client = openai.OpenAI()  # real base_url, real OPENAI_API_KEY
    answer = openai_calls.ask(client, "Reply with exactly one word: hello")
    assert isinstance(answer, str) and answer.strip()
