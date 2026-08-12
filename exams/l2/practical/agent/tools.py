"""Tools for the L2 practical agent: a tiny read-only repo assistant.

Deterministic and in-process — the exam is about operating the agent, not
building interesting tools. `FILES` is the agent's whole world. Three of
the files are large on purpose: `logs/build.log`, `logs/deploy.log`, and
`reports/latency.csv` each run to a few thousand characters.
"""
from __future__ import annotations


def _padded(first_line: str, filler: str, lines: int = 120) -> str:
    """A file whose useful fact sits on line 1, followed by bulk."""
    body = "\n".join(f"{i:04d} {filler}" for i in range(lines))
    return f"{first_line}\n{body}\n"


FILES = {
    "notes/standup.txt": "Today: fix the flaky test.\nBlocked on CI quota.\n",
    "notes/oncall.txt": "Oncall this week: Priya.\nEscalation channel: #inc-agents.\n",
    "config/limits.ini": "max_turns = 8\nresult_budget = 400\n",
    "logs/build.log": _padded(
        "BUILD FAILED: missing dependency libfoo",
        "gcc -c module.c -o module.o ... ok"),
    "logs/deploy.log": _padded(
        "DEPLOY ROLLED BACK: healthcheck timed out after 300s",
        "pod agents-7f9d status=Running probe=pending"),
    "reports/latency.csv": _padded(
        "worst_p99_ms=842 region=eu-west",
        "row,p50_ms=120,p95_ms=340,region=us-east"),
}


def read_file(path: str) -> str:
    """Return the full content of `path`."""
    if path not in FILES:
        raise ValueError(f"no such file: {path}")
    return FILES[path]


def count_lines(path: str) -> str:
    """Return the number of lines in `path`."""
    if path not in FILES:
        raise ValueError(f"no such file: {path}")
    return str(len(FILES[path].splitlines()))


def list_files(prefix: str = "") -> str:
    """Return the paths under `prefix`, one per line, sorted."""
    matches = sorted(p for p in FILES if p.startswith(prefix))
    if not matches:
        raise ValueError(f"no files under: {prefix}")
    return "\n".join(matches)


TOOLS = {
    "read_file": read_file,
    "count_lines": count_lines,
    "list_files": list_files,
}
