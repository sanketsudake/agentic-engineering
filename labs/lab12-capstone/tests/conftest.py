import importlib
import os

import pytest

TARGET = os.environ.get("LAB_TARGET", "starter")


@pytest.fixture(scope="session")
def gate():
    """The module under test: starter by default, solution in CI."""
    return importlib.import_module(f"{TARGET}.release.gate")


@pytest.fixture(scope="session")
def graders():
    """Lab 8's solution graders — provided infrastructure, not the exercise."""
    from provided.evalkit import graders
    return graders


@pytest.fixture(scope="session")
def tasks():
    """The 10 provided tasks — identical for starter and solution."""
    from provided.tasks import TASKS
    return TASKS


@pytest.fixture(scope="session")
def baseline_agent():
    """The agent already running in production."""
    from provided.baseline_agent import run_task
    return run_task


@pytest.fixture(scope="session")
def candidate_good():
    """A candidate with a harmless change: should not regress."""
    from provided.candidate_good import run_task
    return run_task


@pytest.fixture(scope="session")
def candidate_bad():
    """A candidate with a planted regression: should be blocked."""
    from provided.candidate_bad import run_task
    return run_task
