"""A stdlib HTTP server with OpenAI- and Anthropic-shaped endpoints.

For labs whose framework insists on an HTTP provider client: point the SDK's
`base_url` here and serve scripted turns. No network beyond localhost.

Minimal in Phase 1; hardened in Phase 3 when the framework labs land.
"""
from __future__ import annotations

import json
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer


class MockLLM:
    """Serves scripted responses on /v1/messages (Anthropic-shaped) and
    /v1/chat/completions (OpenAI-shaped). `turns` is a list of dicts already
    in the wire shape of the endpoint the lab uses; they are served in order.
    """

    def __init__(self, turns: list[dict]):
        self._turns = list(turns)
        self._i = 0
        self._lock = threading.Lock()
        outer = self

        class Handler(BaseHTTPRequestHandler):
            def do_POST(self):  # noqa: N802 (stdlib API)
                length = int(self.headers.get("Content-Length", 0))
                self.rfile.read(length)
                with outer._lock:
                    if outer._i >= len(outer._turns):
                        self.send_response(500)
                        self.end_headers()
                        self.wfile.write(b'{"error": "mockllm script exhausted"}')
                        return
                    body = json.dumps(outer._turns[outer._i]).encode()
                    outer._i += 1
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)

            def log_message(self, *args):  # silence request logging in tests
                pass

        self._server = HTTPServer(("127.0.0.1", 0), Handler)
        self._thread = threading.Thread(target=self._server.serve_forever, daemon=True)

    @property
    def base_url(self) -> str:
        host, port = self._server.server_address
        return f"http://{host}:{port}/v1"

    def __enter__(self) -> "MockLLM":
        self._thread.start()
        return self

    def __exit__(self, *exc) -> None:
        self._server.shutdown()
        self._server.server_close()
