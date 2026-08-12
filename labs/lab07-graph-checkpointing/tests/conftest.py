import importlib
import os

import pytest

TARGET = os.environ.get("LAB_TARGET", "starter")


@pytest.fixture(scope="session")
def build_module():
    """The module under test: starter by default, solution in CI."""
    return importlib.import_module(f"{TARGET}.graphagent.build")


@pytest.fixture(scope="session")
def memory_facts():
    return importlib.import_module(f"{TARGET}.graphagent.memory_facts")


@pytest.fixture
def sqlite_path(tmp_path):
    """A fresh sqlite file path for one test's checkpointer(s).

    A path, not a connection: tests open (and reopen) their own
    `sqlite3.Connection` against it, so a "restart" can be simulated by
    closing one connection and opening a new one over the same file.
    """
    return tmp_path / "checkpoints.sqlite"
