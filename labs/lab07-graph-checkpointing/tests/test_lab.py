"""Lab 7 checker: state that survives a process restart, via a checkpointer.

They run against starter/ by default (your task list) and against solution/
with LAB_TARGET=solution (the reference passing). No network, no keys: the
model is a scripted fake from langchain_core.
"""
import sqlite3

from langchain_core.messages import AIMessage, HumanMessage
from langgraph.checkpoint.sqlite import SqliteSaver
from langchain_core.language_models.fake_chat_models import FakeMessagesListChatModel


def fake_model(*replies):
    """A deterministic chat model that returns `replies` in order, one per call."""
    return FakeMessagesListChatModel(responses=[AIMessage(r) for r in replies])


def open_checkpointer(sqlite_path):
    """A SqliteSaver over its own sqlite3 connection to `sqlite_path`.

    Each call opens a fresh connection, so callers can simulate a process
    restart by discarding the old checkpointer and calling this again over
    the same file.
    """
    conn = sqlite3.connect(str(sqlite_path), check_same_thread=False)
    return SqliteSaver(conn)


def test_answers_a_simple_turn(build_module, sqlite_path):
    model = fake_model("hi there")
    graph = build_module.build_graph(model, open_checkpointer(sqlite_path))
    config = {"configurable": {"thread_id": "t1"}}

    result = graph.invoke({"messages": [HumanMessage("hello")]}, config)

    assert result["messages"][-1].content == "hi there"


def test_second_turn_sees_first_turns_messages(build_module, memory_facts, sqlite_path):
    model = fake_model("nice to meet you", "yes, I remember")
    graph = build_module.build_graph(model, open_checkpointer(sqlite_path))
    config = {"configurable": {"thread_id": "t1"}}

    graph.invoke({"messages": [HumanMessage("my name is Ada")]}, config)
    result = graph.invoke({"messages": [HumanMessage("do you remember my name?")]}, config)

    contents = [m.content for m in result["messages"]]
    assert "my name is Ada" in contents
    assert memory_facts.extract_fact(result["messages"]) == "my name is Ada"
    assert result["messages"][-1].content == "yes, I remember"


def test_new_graph_over_same_file_resumes_the_thread(build_module, sqlite_path):
    """The restart test: fresh objects, same sqlite file, same thread_id."""
    config = {"configurable": {"thread_id": "t1"}}

    model_before = fake_model("got it")
    graph_before = build_module.build_graph(model_before, open_checkpointer(sqlite_path))
    graph_before.invoke({"messages": [HumanMessage("remember: the launch code is 4711")]}, config)
    del graph_before, model_before  # simulate the process ending

    model_after = fake_model("the launch code is 4711")
    graph_after = build_module.build_graph(model_after, open_checkpointer(sqlite_path))
    snapshot = graph_after.get_state(config)

    contents = [m.content for m in snapshot.values["messages"]]
    assert "remember: the launch code is 4711" in contents

    result = graph_after.invoke({"messages": [HumanMessage("what was the code?")]}, config)
    assert result["messages"][-1].content == "the launch code is 4711"


def test_a_different_thread_id_starts_empty(build_module, sqlite_path):
    model = fake_model("hello t1", "hello t2")
    checkpointer = open_checkpointer(sqlite_path)
    graph = build_module.build_graph(model, checkpointer)

    graph.invoke({"messages": [HumanMessage("hi, this is thread one")]},
                  {"configurable": {"thread_id": "t1"}})
    result = graph.invoke({"messages": [HumanMessage("hi, this is thread two")]},
                           {"configurable": {"thread_id": "t2"}})

    contents = [m.content for m in result["messages"]]
    assert contents == ["hi, this is thread two", "hello t2"]


def test_checkpointer_writes_to_the_sqlite_file(build_module, sqlite_path):
    assert not sqlite_path.exists()

    model = fake_model("saved")
    graph = build_module.build_graph(model, open_checkpointer(sqlite_path))
    graph.invoke({"messages": [HumanMessage("save this")]},
                  {"configurable": {"thread_id": "t1"}})

    assert sqlite_path.exists()
    assert sqlite_path.stat().st_size > 0
