"""Lab 1 checker: 7 tests define "done".

They run against starter/ by default (your task list) and against solution/
with LAB_TARGET=solution (the reference passing). Everything here is
offline — worksheet_common.mockllm stands in for the real API on
localhost only.
"""
import pytest

from worksheet_common.mockllm import MockLLM, anthropic_text_response


def test_ask_returns_scripted_text(calls):
    with MockLLM([anthropic_text_response("Paris is the capital of France.")]) as mock:
        client = calls.make_client(mock.base_url)
        answer = calls.ask(client, "What is the capital of France?")
    assert answer == "Paris is the capital of France."


def test_ask_sends_expected_request_shape(calls):
    with MockLLM([anthropic_text_response("hi")]) as mock:
        client = calls.make_client(mock.base_url)
        calls.ask(client, "hello there")
    assert len(mock.requests) == 1
    body = mock.requests[0]["body"]
    assert body["model"] == calls.MODEL
    assert body["max_tokens"] == calls.MAX_TOKENS
    assert body["messages"] == [{"role": "user", "content": "hello there"}]


def test_ask_concatenates_multiple_text_blocks(calls):
    with MockLLM([anthropic_text_response(["Part one. ", "Part two."])]) as mock:
        client = calls.make_client(mock.base_url)
        answer = calls.ask(client, "go")
    assert answer == "Part one. Part two."


def test_extract_contact_parses_valid_json(calls):
    scripted = anthropic_text_response('{"name": "Ada Lovelace", "email": "ada@example.com"}')
    with MockLLM([scripted]) as mock:
        client = calls.make_client(mock.base_url)
        contact = calls.extract_contact(client, "Ada Lovelace <ada@example.com>")
    assert contact == {"name": "Ada Lovelace", "email": "ada@example.com"}


def test_extract_contact_request_carries_json_schema_output_config(calls):
    scripted = anthropic_text_response('{"name": "Ada", "email": "ada@example.com"}')
    with MockLLM([scripted]) as mock:
        client = calls.make_client(mock.base_url)
        calls.extract_contact(client, "Ada <ada@example.com>")
    body = mock.requests[0]["body"]
    assert body["output_config"]["format"]["type"] == "json_schema"


def test_extract_contact_raises_on_missing_key(calls):
    scripted = anthropic_text_response('{"name": "Ada Lovelace"}')  # no email
    with MockLLM([scripted]) as mock:
        client = calls.make_client(mock.base_url)
        with pytest.raises(ValueError, match="email"):
            calls.extract_contact(client, "Ada Lovelace, no email given")


def test_client_never_reads_api_key_from_env(calls, monkeypatch):
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    monkeypatch.delenv("ANTHROPIC_AUTH_TOKEN", raising=False)  # SDK's next fallback
    with MockLLM([anthropic_text_response("still works")]) as mock:
        client = calls.make_client(mock.base_url)
        answer = calls.ask(client, "does this work with no env key?")
    assert answer == "still works"
