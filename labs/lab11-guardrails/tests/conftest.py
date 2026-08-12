import importlib
import json
import os
from pathlib import Path

import pytest

from worksheet_common.transcripts import load_transcript

TARGET = os.environ.get("LAB_TARGET", "starter")
LAB_ROOT = Path(__file__).resolve().parent.parent
ATTACKS_DIR = LAB_ROOT / "attacks"
LEGIT_DIR = LAB_ROOT / "legit"

ATTACK_IDS = [
    "attack1_ssh_exfil",
    "attack2_env_gist",
    "attack3_email_exfil",
    "attack4_disable_linter",
    "attack5_chmod_root",
]
LEGIT_IDS = [
    "legit1_pytest",
    "legit2_git_status",
    "legit3_edit_docs",
]


@pytest.fixture(scope="session")
def engine():
    """The rule engine: identical code in starter/ and solution/ — provided, not the task."""
    return importlib.import_module(f"{TARGET}.guard.engine")


@pytest.fixture(scope="session")
def policy():
    """The reader's policy.json: this IS the task."""
    path = LAB_ROOT / TARGET / "guard" / "policy.json"
    return json.loads(path.read_text())


@pytest.fixture(scope="session")
def attacks():
    return {aid: load_transcript(ATTACKS_DIR / f"{aid}.jsonl") for aid in ATTACK_IDS}


@pytest.fixture(scope="session")
def legit_sessions():
    return {lid: load_transcript(LEGIT_DIR / f"{lid}.jsonl") for lid in LEGIT_IDS}
