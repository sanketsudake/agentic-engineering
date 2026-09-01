"""Lab 1 checker, OpenAI twin: 6 tests define "done" for openai_calls.py.

Same drill as test_lab.py, against the OpenAI wire shape. The mock serves
`/v1/chat/completions` next to `/v1/messages`; every test here also asserts
the request PATH, because the mock answers scripted turns on either known
path — the path is what proves the client was actually pointed at the
OpenAI-shaped endpoint.
"""
import pytest

from worksheet_common.mockllm import MockLLM, openai_text_response

CHAT_PATH = "/v1/chat/completions"


def test_ask_returns_scripted_text(openai_calls):
    with MockLLM([openai_text_response("Paris is the capital of France.")]) as mock:
        client = openai_calls.make_client(mock.base_url)
        answer = openai_calls.ask(client, "What is the capital of France?")
    assert answer == "Paris is the capital of France."
    assert mock.requests[0]["path"] == CHAT_PATH


def test_ask_sends_expected_request_shape(openai_calls):
    with MockLLM([openai_text_response("hi")]) as mock:
        client = openai_calls.make_client(mock.base_url)
        openai_calls.ask(client, "hello there")
    assert len(mock.requests) == 1
    assert mock.requests[0]["path"] == CHAT_PATH
    body = mock.requests[0]["body"]
    assert body["model"] == openai_calls.MODEL
    assert body["max_completion_tokens"] == openai_calls.MAX_TOKENS
    assert body["messages"] == [{"role": "user", "content": "hello there"}]


def test_extract_contact_parses_valid_json(openai_calls):
    scripted = openai_text_response('{"name": "Ada Lovelace", "email": "ada@example.com"}')
    with MockLLM([scripted]) as mock:
        client = openai_calls.make_client(mock.base_url)
        contact = openai_calls.extract_contact(client, "Ada Lovelace <ada@example.com>")
    assert contact == {"name": "Ada Lovelace", "email": "ada@example.com"}
    assert mock.requests[0]["path"] == CHAT_PATH


def test_extract_contact_request_carries_json_schema_response_format(openai_calls):
    scripted = openai_text_response('{"name": "Ada", "email": "ada@example.com"}')
    with MockLLM([scripted]) as mock:
        client = openai_calls.make_client(mock.base_url)
        openai_calls.extract_contact(client, "Ada <ada@example.com>")
    body = mock.requests[0]["body"]
    assert body["response_format"]["type"] == "json_schema"
    assert body["response_format"]["json_schema"]["schema"]["required"] == ["name", "email"]


def test_extract_contact_raises_on_missing_key(openai_calls):
    scripted = openai_text_response('{"name": "Ada Lovelace"}')  # no email
    with MockLLM([scripted]) as mock:
        client = openai_calls.make_client(mock.base_url)
        with pytest.raises(ValueError, match="email"):
            openai_calls.extract_contact(client, "Ada Lovelace, no email given")


def test_client_never_reads_api_key_from_env(openai_calls, monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    with MockLLM([openai_text_response("still works")]) as mock:
        client = openai_calls.make_client(mock.base_url)
        answer = openai_calls.ask(client, "does this work with no env key?")
    assert answer == "still works"
