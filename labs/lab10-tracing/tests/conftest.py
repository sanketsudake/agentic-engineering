import importlib
import os
from pathlib import Path

import pytest

from worksheet_common.transcripts import load_transcript

from labels import LABELS

TARGET = os.environ.get("LAB_TARGET", "starter")
LAB_ROOT = Path(__file__).resolve().parent.parent
TRANSCRIPTS = LAB_ROOT / "transcripts"


@pytest.fixture(scope="session")
def classify_mod():
    return importlib.import_module(f"{TARGET}.tracing.classify")


@pytest.fixture(scope="session")
def costs_mod():
    return importlib.import_module(f"{TARGET}.tracing.costs")


@pytest.fixture(scope="session")
def all_transcripts():
    """Every fixture, loaded: {session_id: transcript}."""
    return {sid: load_transcript(TRANSCRIPTS / f"{sid}.jsonl") for sid in LABELS}
