"""CI hook: LAB_TARGET=solution swaps in the maintainer reference.

Candidates run plain `uv run pytest` and never set this — they edit
`agent/loop.py` and `evalsuite/tasks_regression.py` in place. CI sets
LAB_TARGET=solution to prove the practical is completable end to end;
the aliases below make the test module import the reference modules
instead of the shipped (buggy/empty) ones.
"""
import os
import sys

if os.environ.get("LAB_TARGET") == "solution":
    import reference.loop_fixed as _loop_fixed
    import reference.tasks_regression_ref as _tasks_reg

    sys.modules["agent.loop"] = _loop_fixed
    sys.modules["evalsuite.tasks_regression"] = _tasks_reg
