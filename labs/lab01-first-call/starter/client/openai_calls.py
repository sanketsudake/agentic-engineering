"""Lab 1, OpenAI twin — the same two calls in the OpenAI wire shape.

`calls.py` made these calls against `POST /v1/messages` (Anthropic). Here
you make them against `POST /v1/chat/completions` (OpenAI) — same mock
server, different wire shape. The point is to see what changes (field
names, where the schema goes) and what does not (one request, one
response, a schema on the wire).
"""
from __future__ import annotations

import json

import openai

MODEL = "gpt-mock"  # the mock server ignores this string; on a real
                    # endpoint it must be a real model id
MAX_TOKENS = 1024


def make_client(base_url: str) -> openai.OpenAI:
    """Build an OpenAI client pointed at `base_url` instead of the real API.

    Spec:
    - Return `openai.OpenAI(...)` configured with `base_url=base_url + "/v1"`.
      The OpenAI SDK appends "/chat/completions" itself, so its base_url
      must end in "/v1" — this is a real difference from the Anthropic SDK,
      which takes the bare server root.
    - Pass a dummy string for `api_key` — NEVER read `OPENAI_API_KEY` (or
      any other real credential) from the environment. The mock server does
      not check the key; a hardcoded placeholder such as "sk-mock" is
      correct.
    """
    raise NotImplementedError("build the client here")


def ask(client: openai.OpenAI, question: str) -> str:
    """Ask a single question and return the model's answer as plain text.

    Spec:
    - Make exactly one `client.chat.completions.create(...)` call:
        - `model=MODEL`
        - `max_completion_tokens=MAX_TOKENS`
        - `messages=[{"role": "user", "content": question}]` — a single user
          message, nothing else.
    - The answer text lives at `response.choices[0].message.content`. It can
      be `None` on tool-call turns; return `""` in that case, never `None`.
    - Return the answer string.
    """
    raise NotImplementedError("make the call here")


def extract_contact(client: openai.OpenAI, text: str) -> dict:
    """Ask the model to pull a contact's name and email out of `text`, as JSON.

    Spec:
    - Request JSON output by putting the schema on the wire, not just in the
      prompt: pass `response_format={"type": "json_schema", "json_schema":
      {"name": "contact", "schema": {...}, "strict": True}}` to
      `client.chat.completions.create(...)`. The schema must require two
      string properties: "name" and "email". (Compare `extract_contact` in
      `calls.py`: same idea, but Anthropic nests the schema under
      `output_config.format` while OpenAI nests it under `response_format`.
      The tests check the request body directly.)
    - Send one user message asking to extract the contact from `text`.
    - Read `response.choices[0].message.content` and parse it as JSON with
      `json.loads`.
    - Validate that both "name" and "email" are present and are strings. If
      a required key is missing, raise `ValueError` naming the missing key,
      e.g. `ValueError("missing key: email")`.
    - Return the parsed dict.
    """
    raise NotImplementedError("extract structured output here")
