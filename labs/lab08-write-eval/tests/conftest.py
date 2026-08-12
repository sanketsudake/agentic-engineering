import importlib
import os

import pytest

TARGET = os.environ.get("LAB_TARGET", "starter")


@pytest.fixture(scope="session")
def graders():
    """The module under test: starter by default, solution in CI."""
    return importlib.import_module(f"{TARGET}.evalkit.graders")


@pytest.fixture(scope="session")
def runner():
    return importlib.import_module(f"{TARGET}.evalkit.runner")


@pytest.fixture(scope="session")
def tasks():
    """The 10 provided tasks — identical for starter and solution."""
    from tasks import TASKS
    return TASKS


@pytest.fixture(scope="session")
def good_agent():
    from agents_under_test.good_agent import run_task
    return run_task


@pytest.fixture(scope="session")
def buggy_agent():
    from agents_under_test.buggy_agent import run_task
    return run_task
