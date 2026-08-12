"""Reference solution for Lab 7: a checkpointed graph (Trace 13, Chapter 5)."""
from __future__ import annotations

from langchain_core.language_models import BaseChatModel
from langgraph.checkpoint.base import BaseCheckpointSaver
from langgraph.graph import END, START, MessagesState, StateGraph
from langgraph.graph.state import CompiledStateGraph


def build_graph(model: BaseChatModel, checkpointer: BaseCheckpointSaver) -> CompiledStateGraph:
    """Build and compile a one-node chat graph backed by `checkpointer`.

    See the starter docstring for the full spec.
    """

    def call_model(state: MessagesState) -> dict:
        response = model.invoke(state["messages"])
        return {"messages": [response]}

    graph = StateGraph(MessagesState)
    graph.add_node("model", call_model)
    graph.add_edge(START, "model")
    graph.add_edge("model", END)
    return graph.compile(checkpointer=checkpointer)
