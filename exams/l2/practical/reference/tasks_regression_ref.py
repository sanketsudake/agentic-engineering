"""Maintainer reference for the regression task (see MAINTAINERS.md).

Candidates never import this; CI does, via LAB_TARGET=solution, to prove
the practical is completable.
"""
from __future__ import annotations

from worksheet_common import ModelResponse, ToolCall

from evalsuite.tasks import reactive_entry

REGRESSION_TASKS: list[dict] = [
    {
        "id": "regress-big-result-1",
        "question": "Why was the last deploy rolled back?",
        "script": [
            ModelResponse(tool_calls=[ToolCall("t1", "read_file",
                                               {"path": "logs/deploy.log"})]),
            reactive_entry(
                on_result=ModelResponse(
                    text="The deploy rolled back: the healthcheck timed out after 300s."),
                on_missing=ModelResponse(
                    tool_calls=[ToolCall("t2", "read_file",
                                         {"path": "logs/deploy.log"})]),
            ),
        ],
        "cycle": True,
        "expected_answer": "The deploy rolled back: the healthcheck timed out after 300s.",
        "required_tools": ["read_file"],
    },
]
