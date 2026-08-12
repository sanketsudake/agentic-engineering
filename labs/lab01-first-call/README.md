# Lab 1 — First model call and structured output

**Goal:** make one real `client.messages.create()` call, then a second call
that forces the response into a JSON shape you can parse without guessing.

**Level:** L1 · **Stack:** `anthropic` SDK · **Time:** ~30 min

**Offline mode (default, no keys):**

```bash
uv sync
uv run pytest                      # 7 red tests are your task list
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

**Done means:** `uv run pytest` is fully green against `starter/`.

## What this proves

The wire shape of a model call — one request, one response, no loop — and
what "structured output" actually is: a schema attached to the request, not
a hope attached to the prompt (see Trace 1 and Trace 3). `tests/test_lab.py`
asserts on the request body your client sent, not just the value you
returned, because the two can disagree even when your code "looks right."

## Live mode (optional)

`tests/test_live.py` runs `ask()` against the real API instead of the mock —
same function under test, `anthropic.Anthropic()` with no `base_url`
override. It is marked `@pytest.mark.live`, deselected by default
(`addopts = "-m 'not live'"` in `pyproject.toml`), and additionally skipped
outright when `ANTHROPIC_API_KEY` is unset, so `uv sync && uv run pytest`
never needs a key or touches the network. Run it explicitly with a real key:

```bash
ANTHROPIC_API_KEY=sk-... uv run pytest -m live
```
