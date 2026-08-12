import importlib
import os

import pytest

TARGET = os.environ.get("LAB_TARGET", "starter")


@pytest.fixture(scope="session")
def agent():
    """The module under test: starter by default, solution in CI."""
    return importlib.import_module(f"{TARGET}.agent.loop")


@pytest.fixture(scope="session")
def _tools_module():
    return importlib.import_module(f"{TARGET}.agent.tools")


@pytest.fixture()
def tools(_tools_module):
    """TOOLS dict, with the call-count ledger reset before every test."""
    _tools_module.CALLS.clear()
    return _tools_module.TOOLS


@pytest.fixture()
def calls(_tools_module, tools):
    """The module-level call-count ledger, reset by the `tools` fixture."""
    return _tools_module.CALLS
