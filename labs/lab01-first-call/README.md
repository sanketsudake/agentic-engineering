# Lab 1 — First model call and structured output

**Goal:** make one real `client.messages.create()` call, then a second call
that forces the response into a JSON shape you can parse without guessing.

**Level:** L1 · **Stack:** `anthropic` SDK (+ an `openai` twin) · **Time:** ~30 min

**Offline mode (default, no keys):**

```bash
uv sync
uv run pytest                      # 13 red tests are your task list
```

**Reference check:**

```bash
LAB_TARGET=solution uv run pytest  # the reference implementation passing
```

## Your task

1. Open `starter/client/calls.py`. Each function's docstring is the full
   spec — there is no separate spec document.
2. Implement `make_client()`: point an `anthropic.Anthropic` client at the
   mock server's `base_url`. Never read `ANTHROPIC_API_KEY` from the
   environment here — the mock does not check it, and a hardcoded dummy
   string is the correct answer.
3. Implement `ask()`: one call, one user message, concatenate every text
   block in the response.
4. Implement `extract_contact()`: put a JSON schema on the wire via
   `extra_body`, parse the result, and raise `ValueError` naming whichever
   required key is missing.
5. Make the 7 tests in `tests/test_lab.py` pass.
6. Open `starter/client/openai_calls.py` and repeat the same three
   functions in the OpenAI wire shape (`POST /v1/chat/completions`), until
   the 6 tests in `tests/test_lab_openai.py` pass. Watch what changes
   between the two providers (field names, where the schema goes) and what
   does not (one request, one response, a schema on the wire).

**Done means:** `uv run pytest` is fully green against `starter/`.

## What this proves

The wire shape of a model call — one request, one response, no loop — and
what "structured output" actually is: a schema attached to the request, not
a hope attached to the prompt (see Trace 1 and Trace 3). `tests/test_lab.py`
asserts on the request body your client sent, not just the value you
returned, because the two can disagree even when your code "looks right."

## Live mode (optional)

`tests/test_live.py` runs `ask()` against a real API instead of the mock —
same functions under test, real clients with no `base_url` override. The
tests are marked `@pytest.mark.live`, deselected by default
(`addopts = "-m 'not live'"` in `pyproject.toml`), and each one is skipped
outright when its provider's key is unset, so `uv sync && uv run pytest`
never needs a key or touches the network. Run them explicitly with a real
key — either provider works:

```bash
ANTHROPIC_API_KEY=sk-... uv run pytest -m live
OPENAI_API_KEY=sk-... OPENAI_LIVE_MODEL=<model-id> uv run pytest -m live
```

Both SDKs honor their base-url env vars (`ANTHROPIC_BASE_URL`,
`OPENAI_BASE_URL`), so any OpenAI-compatible endpoint — Ollama, vLLM,
OpenRouter — can serve the OpenAI live check.
