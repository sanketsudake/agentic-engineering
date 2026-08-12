"""A stdlib HTTP server with OpenAI- and Anthropic-shaped endpoints.

For labs whose framework insists on an HTTP provider client: point the SDK's
`base_url` here and serve scripted turns. No network beyond localhost.

`base_url` is the server root (e.g. "http://127.0.0.1:54321") — pass it
straight to `anthropic.Anthropic(base_url=...)`, which appends "/v1/messages"
itself. Every request is recorded in `self.requests` (path + parsed JSON
body) so tests can assert on exactly what a client sent, not just what it
got back. `anthropic_text_response()` and `anthropic_tool_use_response()`
build minimally-valid response bodies for the scripted `turns` list.
"""
from __future__ import annotations

import json
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

# Paths this server understands. Anything else gets a 404 — a lab whose
# client is misconfigured (wrong base_url, wrong SDK) fails loudly instead
# of the mock silently answering on a path the real API would never serve.
_KNOWN_PATHS = ("/v1/messages", "/v1/chat/completions")


def anthropic_text_response(
    text: str | list[str],
    *,
    id: str = "msg_mock",
    model: str = "claude-mock",
    stop_reason: str = "end_turn",
    input_tokens: int = 10,
    output_tokens: int = 10,
) -> dict:
    """Build a minimally-valid Anthropic `/v1/messages` response with text content.

    `text` is either a single string (one text block) or a list of strings
    (multiple text blocks — a response may legally carry more than one, and
    a client that only reads `content[0]` is a bug this exists to catch).
    """
    texts = [text] if isinstance(text, str) else list(text)
    return {
        "id": id,
        "type": "message",
        "role": "assistant",
        "model": model,
        "content": [{"type": "text", "text": t} for t in texts],
        "stop_reason": stop_reason,
        "stop_sequence": None,
        "usage": {"input_tokens": input_tokens, "output_tokens": output_tokens},
    }


def anthropic_tool_use_response(
    name: str,
    tool_input: dict,
    *,
    tool_use_id: str = "toolu_mock",
    id: str = "msg_mock",
    model: str = "claude-mock",
    text: str | None = None,
    input_tokens: int = 10,
    output_tokens: int = 10,
) -> dict:
    """Build a minimally-valid Anthropic `/v1/messages` response with a tool_use block.

    Pass `text` to prepend a text block before the tool_use block (some
    turns narrate before calling a tool).
    """
    content: list[dict] = []
    if text is not None:
        content.append({"type": "text", "text": text})
    content.append({"type": "tool_use", "id": tool_use_id, "name": name, "input": tool_input})
    return {
        "id": id,
        "type": "message",
        "role": "assistant",
        "model": model,
        "content": content,
        "stop_reason": "tool_use",
        "stop_sequence": None,
        "usage": {"input_tokens": input_tokens, "output_tokens": output_tokens},
    }


class MockLLM:
    """Serves scripted responses on /v1/messages (Anthropic-shaped) and
    /v1/chat/completions (OpenAI-shaped). `turns` is a list of dicts already
    in the wire shape of the endpoint the lab uses; they are served in order,
    one per request, regardless of which known path they arrive on.

    Every request (path + parsed JSON body) is recorded in `self.requests`,
    in arrival order, so a test can assert on what the client actually sent.
    """

    def __init__(self, turns: list[dict]):
        self._turns = list(turns)
        self._i = 0
        self._lock = threading.Lock()
        self.requests: list[dict] = []
        outer = self

        class Handler(BaseHTTPRequestHandler):
            def do_POST(self):  # noqa: N802 (stdlib API)
                length = int(self.headers.get("Content-Length", 0))
                raw = self.rfile.read(length)
                try:
                    parsed_body = json.loads(raw) if raw else {}
                except json.JSONDecodeError:
                    parsed_body = {"_raw": raw.decode("utf-8", "replace")}
                path = self.path.split("?", 1)[0]

                with outer._lock:
                    outer.requests.append({"path": path, "body": parsed_body})

                    if path not in _KNOWN_PATHS:
                        self._reply(404, {"error": f"mockllm: unknown path {path}"})
                        return

                    if outer._i >= len(outer._turns):
                        self._reply(500, {"error": "mockllm script exhausted"})
                        return

                    body = outer._turns[outer._i]
                    outer._i += 1

                self._reply(200, body)

            def _reply(self, status: int, payload: dict) -> None:
                data = json.dumps(payload).encode()
                self.send_response(status)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(data)))
                self.end_headers()
                self.wfile.write(data)

            def log_message(self, *args):  # silence request logging in tests
                pass

        self._server = HTTPServer(("127.0.0.1", 0), Handler)
        self._thread = threading.Thread(target=self._server.serve_forever, daemon=True)

    @property
    def base_url(self) -> str:
        host, port = self._server.server_address
        return f"http://{host}:{port}"

    def __enter__(self) -> "MockLLM":
        self._thread.start()
        return self

    def __exit__(self, *exc) -> None:
        self._server.shutdown()
        self._server.server_close()
