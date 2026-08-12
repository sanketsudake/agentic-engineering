"""Lab 4 fixtures.

LAB_TARGET pattern from Lab 3: tests import `starter.budget.*` by default,
or `solution.budget.*` when LAB_TARGET=solution is set in the environment
(the reference check).
"""
import importlib
import os

import pytest

TARGET = os.environ.get("LAB_TARGET", "starter")


@pytest.fixture(scope="session")
def fit_module():
    """The module under test: starter by default, solution in CI."""
    return importlib.import_module(f"{TARGET}.budget.fit")


@pytest.fixture(scope="session")
def tokens_module():
    return importlib.import_module(f"{TARGET}.budget.tokens")


def _assistant(text=None, tool_calls=None):
    return {"role": "assistant", "content": text, "tool_calls": tool_calls or []}


def _tool(call_id, content):
    return {"role": "tool", "tool_call_id": call_id, "content": content}


def _user(text):
    return {"role": "user", "content": text}


@pytest.fixture
def coding_session():
    """The shared fixture: a realistic 22-message coding-agent session.

    system, task, nine assistant+tool turns (one carrying a 5,000-character
    tool dump), a mid-session user interruption, and a short final answer.
    This is the transcript every compaction test in this file works against.
    """
    system = {
        "role": "system",
        "content": (
            "You are a coding agent. You have tools: list_dir, read_file, "
            "grep, run_tests, edit_file. Work step by step and verify your "
            "fix with a test run before answering."
        ),
    }
    task = _user(
        "The test test_refund_rounds_correctly is failing in "
        "payment_service.py. Find the bug, fix it, and make sure the "
        "whole suite passes."
    )

    messages = [system, task]

    messages.append(_assistant(tool_calls=[
        {"id": "c1", "name": "list_dir", "input": {"path": "."}},
    ]))
    messages.append(_tool("c1", "payment_service.py\ntest_payment_service.py\nlegacy_billing.py\n"))

    messages.append(_assistant(tool_calls=[
        {"id": "c2", "name": "read_file", "input": {"path": "payment_service.py"}},
    ]))
    messages.append(_tool("c2", "def refund(amount):\n    return round(amount * 0.9, 2)\n"))

    messages.append(_assistant(tool_calls=[
        {"id": "c3", "name": "read_file", "input": {"path": "test_payment_service.py"}},
    ]))
    messages.append(_tool(
        "c3",
        "def test_refund_rounds_correctly():\n"
        "    assert refund(19.995) == 18.0\n",
    ))

    # A 5,000-character tool dump: every caller of refund() in the repo.
    grep_hits = "legacy_billing.py:%d: total += refund(amount)\n"
    big_dump = "payment_service.py:2:def refund(amount):\n" + (grep_hits % 1) * 200
    messages.append(_assistant(tool_calls=[
        {"id": "c4", "name": "grep", "input": {"pattern": "refund("}},
    ]))
    messages.append(_tool("c4", big_dump))

    messages.append(_assistant(tool_calls=[
        {"id": "c5", "name": "run_tests", "input": {}},
    ]))
    messages.append(_tool(
        "c5",
        "FAILED test_payment_service.py::test_refund_rounds_correctly\n"
        "AssertionError: 17.996 != 18.0",
    ))

    messages.append(_assistant(tool_calls=[
        {"id": "c6", "name": "edit_file",
         "input": {"path": "payment_service.py", "old": "amount * 0.9", "new": "amount * 0.90"}},
    ]))
    messages.append(_tool("c6", "edit applied to payment_service.py"))

    messages.append(_assistant(tool_calls=[
        {"id": "c7", "name": "run_tests", "input": {}},
    ]))
    messages.append(_tool(
        "c7",
        "FAILED test_payment_service.py::test_refund_negative_amount\n"
        "AssertionError: refund(-10) did not raise ValueError",
    ))

    # Mid-session user interruption.
    messages.append(_user("Also make sure refund() rejects negative amounts."))

    messages.append(_assistant(tool_calls=[
        {"id": "c8", "name": "edit_file",
         "input": {"path": "payment_service.py", "old": "def refund(amount):",
                    "new": "def refund(amount):\n    if amount < 0:\n        raise ValueError('amount must be non-negative')"}},
    ]))
    messages.append(_tool("c8", "edit applied to payment_service.py"))

    messages.append(_assistant(tool_calls=[
        {"id": "c9", "name": "run_tests", "input": {}},
    ]))
    messages.append(_tool("c9", "3 passed in 0.12s"))

    messages.append(_assistant(text="Fixed the rounding bug and added a negative-amount guard. All 3 tests pass."))

    return messages


@pytest.fixture
def tiny_session():
    """A short session, well under any generous budget, no oversized tool result."""
    system = {"role": "system", "content": "You are a helpful coding agent."}
    task = _user("What does 2 + 2 equal?")
    return [
        system,
        task,
        _assistant(tool_calls=[{"id": "c1", "name": "calculator", "input": {"expr": "2+2"}}]),
        _tool("c1", "4"),
        _assistant(text="2 + 2 is 4."),
    ]
