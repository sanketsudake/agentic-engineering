"""CI hook: LAB_TARGET=solution swaps in the maintainer reference.

Candidates run plain `uv run pytest` and edit `assemble/agent.py` in
place. CI sets LAB_TARGET=solution to prove the practical is completable.
"""
import os
import sys

if os.environ.get("LAB_TARGET") == "solution":
    import reference.agent_ref as _ref

    sys.modules["assemble.agent"] = _ref
