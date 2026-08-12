"""L1 practical checker: 10 checks × 3 points, self-scoring.

Run with `uv run pytest`. As shipped, every check fails on
NotImplementedError — that is the exam. Done means all 10 pass WITHOUT
editing this file, `parts/dispatcher.py`, or `parts/toolbox.py`.
"""
from __future__ import annotations

import copy

from worksheet_common import ModelResponse, ScriptedModel, ToolCall

from assemble.agent import run_agent
from parts.dispatcher import dispatch_tool_call
from parts.toolbox import RUNBOOKS, make_toolbox


def _happy_script():
    """One read, then a final answer."""
    return [
        ModelResponse(tool_calls=[ToolCall("t1", "read_runbook",
                                           {"name": "api-restart"})]),
        ModelResponse(text="Drain, SIGTERM, restart — three steps."),
    ]


def _tool_messages(result):
    return [m for m in result.transcript if m["role"] == "tool"]


def test_happy_path_returns_answer():
    """The loop runs one tool turn and returns the model's final text."""
    model = ScriptedModel(_happy_script())
    result = run_agent(model, dispatch_tool_call, make_toolbox(),
                       "How do I restart the api?")
    assert result.answer == "Drain, SIGTERM, restart — three steps."
    assert result.stopped == "done"


def test_dispatcher_is_actually_used():
    """Every tool result is exactly what the injected dispatcher returned."""
    seen = []

    def spy(call, toolbox):
        seen.append(call.name)
        return f"spy-result:{call.id}"

    model = ScriptedModel(_happy_script())
    result = run_agent(model, spy, make_toolbox(), "How do I restart the api?")
    assert seen == ["read_runbook"], "route every call through the dispatcher"
    tool_msgs = _tool_messages(result)
    assert tool_msgs and tool_msgs[0]["content"] == "spy-result:t1", \
        "the tool result must be the dispatcher's return value, unmodified"


def test_results_appended_in_order_with_matching_ids():
    """Three parallel calls: results keep the model's order, ids match."""
    script = [
        ModelResponse(tool_calls=[
            ToolCall("t1", "count_steps", {"name": "db-failover"}),
            ToolCall("t2", "read_runbook", {"name": "cache-flush"}),
            ToolCall("t3", "list_runbooks", {}),
        ]),
        ModelResponse(text="ok"),
    ]
    result = run_agent(ScriptedModel(script), dispatch_tool_call,
                       make_toolbox(), "Compare the runbooks.")
    tool_msgs = _tool_messages(result)
    assert [m["tool_call_id"] for m in tool_msgs] == ["t1", "t2", "t3"]
    assert tool_msgs[0]["content"] == "4"
    assert tool_msgs[1]["content"] == RUNBOOKS["cache-flush"]
    assert tool_msgs[2]["content"] == "\n".join(sorted(RUNBOOKS))


def test_unknown_tool_error_surfaced():
    """A hallucinated tool name becomes dispatcher error text the model reads."""
    script = [
        ModelResponse(tool_calls=[ToolCall("t1", "delete_runbook",
                                           {"name": "api-restart"})]),
        ModelResponse(text="That tool does not exist; nothing was deleted."),
    ]
    result = run_agent(ScriptedModel(script), dispatch_tool_call,
                       make_toolbox(), "Delete the restart runbook.")
    tool_msgs = _tool_messages(result)
    assert tool_msgs and tool_msgs[0]["content"] == "error: unknown tool delete_runbook"
    assert result.answer == "That tool does not exist; nothing was deleted."


def test_malformed_args_error_surfaced():
    """A schema-invalid call becomes dispatcher error text, not a crash."""
    script = [
        ModelResponse(tool_calls=[ToolCall("t1", "read_runbook",
                                           {"path": "api-restart"})]),
        ModelResponse(text="Let me correct the argument name."),
    ]
    result = run_agent(ScriptedModel(script), dispatch_tool_call,
                       make_toolbox(), "Read the restart runbook.")
    tool_msgs = _tool_messages(result)
    assert tool_msgs and tool_msgs[0]["content"] == "error: missing required argument name"


def test_done_marker_stops_early():
    """DONE: wins over tool calls: nothing dispatched, the suffix returned."""
    script = [
        ModelResponse(
            text="I have enough. DONE: run api-restart, steps 1 to 3.",
            tool_calls=[ToolCall("t9", "read_runbook", {"name": "api-restart"})],
        ),
    ]
    model = ScriptedModel(script)
    result = run_agent(model, dispatch_tool_call, make_toolbox(),
                       "How do I restart the api?")
    assert result.answer == "run api-restart, steps 1 to 3."
    assert result.stopped == "done"
    assert _tool_messages(result) == [], \
        "DONE: means stop now — the response's tool calls are not dispatched"
    assert len(model.calls) == 1


def test_max_turns_halts_with_stopped_state():
    """A model that never stops calling tools hits the cap, marked as such."""
    script = [ModelResponse(tool_calls=[ToolCall("t1", "list_runbooks", {})])]
    model = ScriptedModel(script, cycle=True)
    result = run_agent(model, dispatch_tool_call, make_toolbox(),
                       "Loop forever.", max_turns=3)
    assert result.stopped == "max_turns"
    assert result.answer == ""
    assert len(model.calls) == 3, "the cap bounds model calls, not tool calls"


def test_transcript_shape_is_valid():
    """The transcript follows the documented message shapes, start to end."""
    result = run_agent(ScriptedModel(_happy_script()), dispatch_tool_call,
                       make_toolbox(), "How do I restart the api?")
    t = result.transcript
    assert t[0] == {"role": "user", "content": "How do I restart the api?"}
    assert [m["role"] for m in t] == ["user", "assistant", "tool", "assistant"]
    for m in t:
        if m["role"] == "assistant":
            assert isinstance(m["tool_calls"], list)
            for c in m["tool_calls"]:
                assert set(c) == {"id", "name", "input"}
        if m["role"] == "tool":
            assert isinstance(m["content"], str)
            assert m["tool_call_id"] == "t1"


def test_model_called_expected_number_of_times():
    """Two tool turns plus a final answer is exactly three model calls."""
    script = [
        ModelResponse(tool_calls=[ToolCall("t1", "list_runbooks", {})]),
        ModelResponse(tool_calls=[ToolCall("t2", "read_runbook",
                                           {"name": "db-failover"})]),
        ModelResponse(text="Freeze writes, then promote the replica."),
    ]
    model = ScriptedModel(script)
    result = run_agent(model, dispatch_tool_call, make_toolbox(),
                       "How does the db failover work?")
    assert len(model.calls) == 3
    assert result.answer == "Freeze writes, then promote the replica."


def test_toolbox_not_mutated():
    """The toolbox is an input, not scratch space: identical after the run."""
    toolbox = make_toolbox()
    snapshot = {"tool_defs": copy.deepcopy(toolbox["tool_defs"]),
                "registry": dict(toolbox["registry"])}
    run_agent(ScriptedModel(_happy_script()), dispatch_tool_call, toolbox,
              "How do I restart the api?")
    assert set(toolbox) == {"tool_defs", "registry"}
    assert toolbox["tool_defs"] == snapshot["tool_defs"]
    assert toolbox["registry"] == snapshot["registry"]
