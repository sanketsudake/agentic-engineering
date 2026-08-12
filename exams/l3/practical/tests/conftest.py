"""CI hook: LAB_TARGET=solution swaps in the maintainer reference.

Candidates run plain `uv run pytest` and never set this — they implement
`rollout/engine.py` in place. CI sets LAB_TARGET=solution to prove the
practical is completable end to end; the alias below makes the test module
import the reference engine instead of the shipped (NotImplementedError)
one.
"""
import os
import sys

if os.environ.get("LAB_TARGET") == "solution":
    import reference.engine_ref as _engine_ref

    sys.modules["rollout.engine"] = _engine_ref
