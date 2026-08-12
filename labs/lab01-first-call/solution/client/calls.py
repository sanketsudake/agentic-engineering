"""Reference solution for Lab 1: first model call + structured output."""
from __future__ import annotations

import json

import anthropic

MODEL = "claude-mock"
MAX_TOKENS = 1024

_CONTACT_SCHEMA = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "email": {"type": "string"},
    },
    "required": ["name", "email"],
    "additionalProperties": False,
}


def make_client(base_url: str) -> anthropic.Anthropic:
    return anthropic.Anthropic(api_key="sk-ant-mock", base_url=base_url)


def _concat_text(response: anthropic.types.Message) -> str:
    return "".join(block.text for block in response.content if block.type == "text")


def ask(client: anthropic.Anthropic, question: str) -> str:
    response = client.messages.create(
        model=MODEL,
        max_tokens=MAX_TOKENS,
        messages=[{"role": "user", "content": question}],
    )
    return _concat_text(response)


def extract_contact(client: anthropic.Anthropic, text: str) -> dict:
    response = client.messages.create(
        model=MODEL,
        max_tokens=MAX_TOKENS,
        messages=[{
            "role": "user",
            "content": f"Extract the contact's name and email from this text:\n\n{text}",
        }],
        extra_body={
            "output_config": {
                "format": {"type": "json_schema", "schema": _CONTACT_SCHEMA},
            },
        },
    )
    contact = json.loads(_concat_text(response))
    for key in ("name", "email"):
        if not isinstance(contact.get(key), str):
            raise ValueError(f"missing key: {key}")
    return contact
