import importlib
import os

import pytest

TARGET = os.environ.get("LAB_TARGET", "starter")


@pytest.fixture(scope="session")
def calls():
    """The module under test: starter by default, solution in CI."""
    return importlib.import_module(f"{TARGET}.client.calls")
