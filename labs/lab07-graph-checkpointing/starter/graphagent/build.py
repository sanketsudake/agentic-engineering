"""Lab 7 — your task: wire a checkpointed graph (Trace 13, Chapter 5).

You are the harness. LangGraph is the loop; you own how state gets in and
out of the checkpointer.
"""
from __future__ import annotations

from langchain_core.language_models import BaseChatModel
from langgraph.checkpoint.base import BaseCheckpointSaver
from langgraph.graph.state import CompiledStateGraph


def build_graph(model: BaseChatModel, checkpointer: BaseCheckpointSaver) -> CompiledStateGraph:
    """Build and compile a one-node chat graph backed by `checkpointer`.

    State is `MessagesState`: a dict with one key, `"messages"`, reduced by
    LangGraph's `add_messages` (new messages append; they never overwrite).

    The graph:

    1. One node, e.g. named "model", whose function reads
       `state["messages"]`, calls `model.invoke(state["messages"])`, and
       returns `{"messages": [response]}` — the reducer appends the
       response for you.
    2. An edge from START to that node, and from that node to END: one
       model call per invocation, no tool loop.
    3. Compiled with `checkpointer=checkpointer` — this is what makes state
       durable. Without it, `.invoke()` still works but nothing survives
       the process.

    Callers invoke the returned graph like this:

        graph.invoke({"messages": [HumanMessage("hi")]},
                      {"configurable": {"thread_id": "some-id"}})

    `thread_id` is the checkpointer's key: every call with the same
    `thread_id` reads the prior state first, so the message list keeps
    growing across turns, and across process restarts once a new graph is
    built over the same checkpointer storage (Trace 13's "session" becomes
    a `thread_id`; the checkpointer writes at every superstep instead of
    only at a clean end).

    Returns the compiled graph. Do not call `.invoke()` here — that is the
    caller's job.
    """
    raise NotImplementedError("build the graph here")
