"""Lab 1 — your task: make your first model call, then get structured output.

You are the reader here, not the harness: no loop, no tools, just the wire
shape of `POST /v1/messages` (Trace 1) and a schema-constrained response
(Trace 3). Every function below runs against `worksheet_common.mockllm`, so
there is nothing to install beyond `uv sync` and no key to hold.
"""
from __future__ import annotations

import json

import anthropic

MODEL = "claude-mock"  # the mock server ignores this string; on a real
                        # endpoint it must be a real model id, e.g. "claude-opus-5"
MAX_TOKENS = 1024


def make_client(base_url: str) -> anthropic.Anthropic:
    """Build an Anthropic client pointed at `base_url` instead of the real API.

    Spec:
    - Return `anthropic.Anthropic(...)` configured with `base_url=base_url`.
    - Pass a dummy string for `api_key` — NEVER read `ANTHROPIC_API_KEY` (or
      any other real credential) from the environment. The mock server does
      not check the key; a hardcoded placeholder such as "sk-ant-mock" is
      correct, and is exactly what lets the tests run with no account and no
      network.
    """
    raise NotImplementedError("build the client here")


def ask(client: anthropic.Anthropic, question: str) -> str:
    """Ask a single question and return the model's answer as plain text.

    Spec:
    - Make exactly one `client.messages.create(...)` call:
        - `model=MODEL`
        - `max_tokens=MAX_TOKENS`
        - `messages=[{"role": "user", "content": question}]` — a single user
          message, nothing else.
    - `response.content` is a list of content blocks. Iterate it, check
      `block.type == "text"`, and concatenate the `.text` of every text
      block in order. A response may legally carry more than one text
      block — do not assume there is exactly one and do not just read
      `content[0]`.
    - Return the concatenated string.
    """
    raise NotImplementedError("make the call here")


def extract_contact(client: anthropic.Anthropic, text: str) -> dict:
    """Ask the model to pull a contact's name and email out of `text`, as JSON.

    Spec:
    - Request JSON output by putting the schema on the wire, not just in the
      prompt: pass `extra_body={"output_config": {"format": {"type":
      "json_schema", "schema": {...}}}}` to `client.messages.create(...)`.
      The schema must require two string properties: "name" and "email".
      (Trace 3 is about this exact wire shape — the tests check the request
      body directly, not just the parsed result.)
    - Send one user message asking to extract the contact from `text`.
    - Read the response text the same way `ask()` does (concatenate every
      text block), then parse it as JSON with `json.loads`.
    - Validate that both "name" and "email" are present and are strings. If
      a required key is missing, raise `ValueError` naming the missing key,
      e.g. `ValueError("missing key: email")`.
    - Return the parsed dict.
    """
    raise NotImplementedError("extract structured output here")
