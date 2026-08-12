import importlib
import json
import os
from pathlib import Path

import pytest

from worksheet_common.transcripts import load_transcript

TARGET = os.environ.get("LAB_TARGET", "starter")
LAB_ROOT = Path(__file__).resolve().parent.parent
TRANSCRIPTS = LAB_ROOT / "transcripts"


@pytest.fixture(scope="session")
def engine():
    """The rule engine: identical code in starter/ and solution/ — provided, not the task."""
    return importlib.import_module(f"{TARGET}.policy.engine")


@pytest.fixture(scope="session")
def permissions():
    """The reader's settings.json permissions block: this IS the task."""
    path = LAB_ROOT / TARGET / "policy" / "settings.json"
    settings = json.loads(path.read_text())
    return settings["permissions"]


@pytest.fixture(scope="session")
def claude_md_text():
    """The reader's operating instructions: this IS the task."""
    path = LAB_ROOT / TARGET / "policy" / "CLAUDE.md"
    return path.read_text()


@pytest.fixture(scope="session")
def session1():
    return load_transcript(TRANSCRIPTS / "session1.jsonl")


@pytest.fixture(scope="session")
def session2():
    return load_transcript(TRANSCRIPTS / "session2.jsonl")


@pytest.fixture(scope="session")
def session3():
    return load_transcript(TRANSCRIPTS / "session3.jsonl")
