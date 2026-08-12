"""The 10 provided tasks. Frozen — do not edit; extend in `tasks_regression.py`.

Seven tasks are small: every tool result fits comfortably in the agent's
result budget. Three tasks (`build-log-1`, `deploy-log-1`,
`latency-report-1`) each read a file that runs to a few thousand
characters; the useful fact is on the file's first line.

The big tasks use `reactive_entry()`: a `ScriptedModel` entry whose
response depends on the transcript at call time (see
`worksheet_common.scripted_model` — a `(check, response)` tuple whose
`check` runs first and rewrites the shared response in place). A model
that just received a tool result answers from it; a model whose tool call
got no visible answer does the only sensible thing and asks again. The
big tasks set `"cycle": True` so that an agent stuck re-asking exhausts
its `max_turns`, not the script.
"""
from __future__ import annotations

from worksheet_common import ModelResponse, ToolCall


def reactive_entry(on_result: ModelResponse, on_missing: ModelResponse):
    """A ScriptedModel entry that branches on whether the previous tool
    call's result actually reached the transcript.

    `on_result` plays when the last message is a tool result — the model
    saw its tool's output. `on_missing` plays when it is not — the model
    asked for a tool and never saw an answer, so it asks again.
    """
    response = ModelResponse()

    def check(messages: list[dict]) -> None:
        source = on_result if messages[-1]["role"] == "tool" else on_missing
        response.text = source.text
        response.tool_calls = source.tool_calls

    return (check, response)


TASKS = [
    # -- 7 small tasks: every tool result fits the result budget.
    {
        "id": "standup-1",
        "question": "What is blocking today?",
        "script": [
            ModelResponse(tool_calls=[ToolCall("t1", "read_file",
                                               {"path": "notes/standup.txt"})]),
            ModelResponse(text="Today's work is blocked on CI quota."),
        ],
        "expected_answer": "Today's work is blocked on CI quota.",
        "required_tools": ["read_file"],
    },
    {
        "id": "oncall-1",
        "question": "Who is oncall this week?",
        "script": [
            ModelResponse(tool_calls=[ToolCall("t1", "read_file",
                                               {"path": "notes/oncall.txt"})]),
            ModelResponse(text="Priya is oncall this week."),
        ],
        "expected_answer": "Priya is oncall this week.",
        "required_tools": ["read_file"],
    },
    {
        "id": "limits-1",
        "question": "What is max_turns set to?",
        "script": [
            ModelResponse(tool_calls=[ToolCall("t1", "read_file",
                                               {"path": "config/limits.ini"})]),
            ModelResponse(text="max_turns is set to 8."),
        ],
        "expected_answer": "max_turns is set to 8.",
        "required_tools": ["read_file"],
    },
    {
        "id": "count-standup-1",
        "question": "How many lines does notes/standup.txt have?",
        "script": [
            ModelResponse(tool_calls=[ToolCall("t1", "count_lines",
                                               {"path": "notes/standup.txt"})]),
            ModelResponse(text="notes/standup.txt has 2 lines."),
        ],
        "expected_answer": "notes/standup.txt has 2 lines.",
        "required_tools": ["count_lines"],
    },
    {
        "id": "count-limits-1",
        "question": "How many lines does config/limits.ini have?",
        "script": [
            ModelResponse(tool_calls=[ToolCall("t1", "count_lines",
                                               {"path": "config/limits.ini"})]),
            ModelResponse(text="config/limits.ini has 2 lines."),
        ],
        "expected_answer": "config/limits.ini has 2 lines.",
        "required_tools": ["count_lines"],
    },
    {
        "id": "list-notes-1",
        "question": "Which files are under notes/?",
        "script": [
            ModelResponse(tool_calls=[ToolCall("t1", "list_files",
                                               {"prefix": "notes/"})]),
            ModelResponse(text="The notes are notes/oncall.txt and notes/standup.txt."),
        ],
        "expected_answer": "The notes are notes/oncall.txt and notes/standup.txt.",
        "required_tools": ["list_files"],
    },
    {
        "id": "oncall-limits-1",
        "question": "Who is oncall, and what is max_turns set to?",
        "script": [
            ModelResponse(tool_calls=[ToolCall("t1", "read_file",
                                               {"path": "notes/oncall.txt"})]),
            ModelResponse(tool_calls=[ToolCall("t2", "read_file",
                                               {"path": "config/limits.ini"})]),
            ModelResponse(text="Priya is oncall, and max_turns is set to 8."),
        ],
        "expected_answer": "Priya is oncall, and max_turns is set to 8.",
        "required_tools": ["read_file", "read_file"],
    },

    # -- 3 big tasks: the tool result exceeds the agent's result budget.
    {
        "id": "build-log-1",
        "question": "Why did the last build fail?",
        "script": [
            ModelResponse(tool_calls=[ToolCall("t1", "read_file",
                                               {"path": "logs/build.log"})]),
            reactive_entry(
                on_result=ModelResponse(
                    text="The build failed: missing dependency libfoo."),
                on_missing=ModelResponse(
                    tool_calls=[ToolCall("t2", "read_file",
                                         {"path": "logs/build.log"})]),
            ),
        ],
        "cycle": True,
        "expected_answer": "The build failed: missing dependency libfoo.",
        "required_tools": ["read_file"],
    },
    {
        "id": "deploy-log-1",
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
    {
        "id": "latency-report-1",
        "question": "What is the worst p99 latency, and where?",
        "script": [
            ModelResponse(tool_calls=[ToolCall("t1", "read_file",
                                               {"path": "reports/latency.csv"})]),
            reactive_entry(
                on_result=ModelResponse(
                    text="The worst p99 is 842 ms, in eu-west."),
                on_missing=ModelResponse(
                    tool_calls=[ToolCall("t2", "read_file",
                                         {"path": "reports/latency.csv"})]),
            ),
        ],
        "cycle": True,
        "expected_answer": "The worst p99 is 842 ms, in eu-west.",
        "required_tools": ["read_file"],
    },
]

BIG_TASK_IDS = {"build-log-1", "deploy-log-1", "latency-report-1"}
