"""Lab 5 checker: each test names one bug and states the correct behavior.

Run against starter/ by default (your task list) and against solution/
with LAB_TARGET=solution (the reference passing).
"""
from worksheet_common import ModelResponse, ScriptedModel, ToolCall

MAX_RESULT_CHARS = 2000


def test_happy_path_still_works(agent, tools):
    """A tool call that succeeds cleanly still reaches a final answer."""
    model = ScriptedModel([
        ModelResponse(tool_calls=[ToolCall("t1", "slow_lookup", {"key": "fast"})]),
        ModelResponse(text="fast is ok."),
    ])
    result = agent.run_agent(model, tools, "look up fast")
    assert result.stopped == "done"
    assert result.answer == "fast is ok."


def test_long_tool_result_is_truncated(agent, tools):
    """Bug 1 — context flood: a huge tool result must be capped, with a
    trailing marker that names the original size."""
    model = ScriptedModel([
        ModelResponse(tool_calls=[ToolCall("t1", "dump_table", {"name": "orders"})]),
        ModelResponse(text="done."),
    ])
    result = agent.run_agent(model, tools, "dump orders")
    tool_msg = next(m for m in result.transcript if m["role"] == "tool")
    content = tool_msg["content"]
    assert content == "x" * MAX_RESULT_CHARS + "\n[truncated: result was 10000 chars]"


def test_timed_out_tool_runs_exactly_once(agent, tools, calls):
    """Bug 2 — non-idempotent retry: a timeout must not trigger a second
    execution of the tool."""
    model = ScriptedModel([
        ModelResponse(tool_calls=[ToolCall("t1", "slow_lookup", {"key": "slow"})]),
        ModelResponse(text="gave up after one try."),
    ])
    agent.run_agent(model, tools, "look up slow")
    assert calls["slow"] == 1


def test_timeout_surfaces_as_error(agent, tools):
    """Bug 2, other half: the model must see the timeout, not silence."""
    model = ScriptedModel([
        ModelResponse(tool_calls=[ToolCall("t1", "slow_lookup", {"key": "slow"})]),
        ModelResponse(text="ok."),
    ])
    result = agent.run_agent(model, tools, "look up slow")
    tool_msg = next(m for m in result.transcript if m["role"] == "tool")
    assert tool_msg["content"] == "error: timed out after 5s"


def test_raised_exception_surfaces_not_swallowed(agent, tools):
    """Bug 3 — swallowed error: a tool exception must become a visible
    error message, never an empty "success"."""
    model = ScriptedModel([
        ModelResponse(tool_calls=[ToolCall("t1", "slow_lookup", {"wrong_kwarg": "x"})]),
        ModelResponse(text="ok."),
    ])
    result = agent.run_agent(model, tools, "look up with bad args")
    tool_msg = next(m for m in result.transcript if m["role"] == "tool")
    assert tool_msg["content"] != ""
    assert "error" in tool_msg["content"].lower()


def test_transcript_shape_is_valid(agent, tools):
    """The fixes must not break the transcript's message shape."""
    model = ScriptedModel([
        ModelResponse(tool_calls=[ToolCall("t1", "slow_lookup", {"key": "fast"})]),
        ModelResponse(text="done."),
    ])
    result = agent.run_agent(model, tools, "go")
    t = result.transcript
    assert t[0] == {"role": "user", "content": "go"}
    for i, m in enumerate(t):
        if m["role"] == "assistant" and m.get("tool_calls"):
            follow = t[i + 1: i + 1 + len(m["tool_calls"])]
            assert [f["role"] for f in follow] == ["tool"] * len(m["tool_calls"])
            assert [f["tool_call_id"] for f in follow] == [c["id"] for c in m["tool_calls"]]
    assert t[-1]["role"] == "assistant" and t[-1]["content"]
