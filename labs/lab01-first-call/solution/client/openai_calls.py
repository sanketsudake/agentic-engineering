"""Reference solution for Lab 1's OpenAI twin: same two calls, OpenAI wire shape."""
from __future__ import annotations

import json

import openai

MODEL = "gpt-mock"
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


def make_client(base_url: str) -> openai.OpenAI:
    return openai.OpenAI(api_key="sk-mock", base_url=base_url + "/v1")


def ask(client: openai.OpenAI, question: str) -> str:
    response = client.chat.completions.create(
        model=MODEL,
        max_completion_tokens=MAX_TOKENS,
        messages=[{"role": "user", "content": question}],
    )
    return response.choices[0].message.content or ""


def extract_contact(client: openai.OpenAI, text: str) -> dict:
    response = client.chat.completions.create(
        model=MODEL,
        max_completion_tokens=MAX_TOKENS,
        messages=[{
            "role": "user",
            "content": f"Extract the contact's name and email from this text:\n\n{text}",
        }],
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "contact",
                "schema": _CONTACT_SCHEMA,
                "strict": True,
            },
        },
    )
    contact = json.loads(response.choices[0].message.content or "")
    for key in ("name", "email"):
        if not isinstance(contact.get(key), str):
            raise ValueError(f"missing key: {key}")
    return contact
