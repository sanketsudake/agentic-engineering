import importlib
import os

import pytest

TARGET = os.environ.get("LAB_TARGET", "starter")


@pytest.fixture(scope="session")
def schemas():
    return importlib.import_module(f"{TARGET}.toolkit.schemas")


@pytest.fixture(scope="session")
def dispatch_mod():
    return importlib.import_module(f"{TARGET}.toolkit.dispatch")


@pytest.fixture(autouse=True)
def fresh_store():
    impl = importlib.import_module(f"{TARGET}.toolkit.impl")
    impl.reset()
    yield
