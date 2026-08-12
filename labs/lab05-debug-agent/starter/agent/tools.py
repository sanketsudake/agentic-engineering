"""Tools for Lab 5's agent loop.

slow_lookup simulates a lookup that times out for one particular key —
real backends do this under load. CALLS records how many times each key
was looked up, so a test can prove whether the loop retried a timed-out
call instead of just trusting the loop's own bookkeeping.

dump_table simulates a tool that returns far more data than should ever
land raw in a model's context window.
"""
from __future__ import annotations

CALLS: dict[str, int] = {}

_RECORDS = {
    "fast": "ok",
    "widgets": "42 widgets in stock",
}


def slow_lookup(key: str) -> str:
    """Look up a key in the record store. The key "slow" times out."""
    CALLS[key] = CALLS.get(key, 0) + 1
    if key == "slow":
        raise TimeoutError(f"lookup for {key!r} did not respond in time")
    return _RECORDS.get(key, f"no record for {key!r}")


def dump_table(name: str) -> str:
    """Return the full contents of a table. Some tables are huge."""
    return "x" * 10_000


TOOLS = {
    "slow_lookup": slow_lookup,
    "dump_table": dump_table,
}
