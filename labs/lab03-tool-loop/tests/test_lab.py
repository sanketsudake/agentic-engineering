"""Lab 3 checker: 7 tests define "done".

They run against starter/ by default (your task list) and against solution/
with LAB_TARGET=solution (the reference passing).
"""
from worksheet_common import ModelResponse, ScriptedModel, ToolCall


def happy_model(tmp_path_content_file):
    """Two tool calls, then a final answer."""
    return ScriptedModel([
        ModelResponse(tool_calls=[ToolCall("t1", "read_file", {"path": tmp_path_content_file})]),
        ModelResponse(tool_calls=[ToolCall("t2", "calculator", {"expr": "6 * 7"})]),
        ModelResponse(text="The answer is 42."),
    ])


def test_happy_path_answer(agent, tools, tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    (tmp_path / "notes.txt").write_text("six times seven")
    model = happy_model("notes.txt")
    result = agent.run_agent(model, tools, "compute the thing in notes.txt")
    assert result.stopped == "done"
    assert result.answer == "The answer is 42."


def test_tool_dispatched_with_parsed_args(agent, tools, tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    (tmp_path / "notes.txt").write_text("six times seven")
    model = happy_model("notes.txt")
    result = agent.run_agent(model, tools, "go")
    tool_msgs = [m for m in result.transcript if m["role"] == "tool"]
    assert tool_msgs[0]["content"] == "six times seven"   # read_file ran for real
    assert tool_msgs[1]["content"] == "42"                # calculator got expr="6 * 7"


def test_tool_results_appended_in_order(agent, tools, tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    (tmp_path / "notes.txt").write_text("x")
    model = happy_model("notes.txt")
    result = agent.run_agent(model, tools, "go")
    ids = [m["tool_call_id"] for m in result.transcript if m["role"] == "tool"]
    assert ids == ["t1", "t2"]


def test_unknown_tool_surfaces_as_error(agent, tools):
    model = ScriptedModel([
        ModelResponse(tool_calls=[ToolCall("t1", "send_email", {"to": "x"})]),
        ModelResponse(text="ok, no email tool here."),
    ])
    result = agent.run_agent(model, tools, "email someone")
    tool_msgs = [m for m in result.transcript if m["role"] == "tool"]
    assert len(tool_msgs) == 1
    assert "error" in tool_msgs[0]["content"].lower()
    assert "send_email" in tool_msgs[0]["content"]
    assert result.stopped == "done"


def test_malformed_args_surface_as_error(agent, tools):
    model = ScriptedModel([
        ModelResponse(tool_calls=[ToolCall("t1", "calculator", {"expression": "6*7"})]),
        ModelResponse(tool_calls=[ToolCall("t2", "calculator", {"expr": "6*7"})]),
        ModelResponse(text="42"),
    ])
    result = agent.run_agent(model, tools, "compute")
    tool_msgs = [m for m in result.transcript if m["role"] == "tool"]
    assert "error" in tool_msgs[0]["content"].lower()  # wrong kwarg name, surfaced
    assert tool_msgs[1]["content"] == "42"             # model corrected itself


def test_halts_at_max_turns(agent, tools):
    model = ScriptedModel(
        [ModelResponse(tool_calls=[ToolCall("t1", "calculator", {"expr": "1+1"})])],
        cycle=True)
    result = agent.run_agent(model, tools, "loop forever", max_turns=4)
    assert result.stopped == "max_turns"
    assert len(model.calls) == 4


def test_transcript_shape_is_valid(agent, tools, tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    (tmp_path / "notes.txt").write_text("x")
    model = happy_model("notes.txt")
    result = agent.run_agent(model, tools, "go")
    t = result.transcript
    assert t[0] == {"role": "user", "content": "go"}
    for i, m in enumerate(t):
        if m["role"] == "assistant" and m.get("tool_calls"):
            follow = t[i + 1: i + 1 + len(m["tool_calls"])]
            assert [f["role"] for f in follow] == ["tool"] * len(m["tool_calls"])
            assert [f["tool_call_id"] for f in follow] == [c["id"] for c in m["tool_calls"]]
    assert t[-1]["role"] == "assistant" and t[-1]["content"]
