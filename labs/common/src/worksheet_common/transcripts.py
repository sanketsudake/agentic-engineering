"""Load/assert helpers for recorded session transcripts.

Coding-agent labs analyze committed transcripts instead of driving a live
harness. Minimal in Phase 1; grows with labs 08-10.
"""
from __future__ import annotations

import json
from pathlib import Path


def load_transcript(path: str | Path) -> list[dict]:
    """Load a JSONL transcript: one message dict per line."""
    lines = Path(path).read_text().splitlines()
    return [json.loads(line) for line in lines if line.strip()]


def tool_results(transcript: list[dict]) -> list[dict]:
    return [m for m in transcript if m.get("role") == "tool"]


def assistant_turns(transcript: list[dict]) -> list[dict]:
    return [m for m in transcript if m.get("role") == "assistant"]
