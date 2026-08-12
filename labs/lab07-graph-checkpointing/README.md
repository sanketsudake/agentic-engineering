# Lab 7 — Stateful graph agent with checkpointing

**Goal:** build `build_graph()` — a LangGraph agent whose conversation state survives a process restart.
You wire the graph;
LangGraph's checkpointer does the persistence.

**Level:** L2 · **Stack:** LangGraph · **Time:** ~60 min

**Offline mode (default, no keys):**

```bash
uv sync
uv run pytest                      # 5 red tests are your task list
```

**Reference check:**

```bash
LAB_TARGET=solution uv run pytest  # the reference implementation passing
```

## Your task

1. Open `starter/graphagent/build.py`.
   The docstring on `build_graph()` is the full spec: one model node over `MessagesState`, compiled with the checkpointer you are given.
2. Make the 5 tests in `tests/test_lab.py` pass.
   Each test names one thing a stateful harness must get right: a single turn answers, a second turn on the same thread sees the first, a brand-new graph over the same sqlite file resumes a thread after a "restart," a different thread_id stays isolated, and the checkpointer actually wrote to disk.

**Done means:** `uv run pytest` is fully green against `starter/`.

Model access is a scripted fake chat model from `langchain_core` (`FakeMessagesListChatModel`) — zero network, zero keys.
There is no live mode for this lab on purpose: the point is the checkpointer, not the model.

## What this proves

Persistence is a harness feature, not a model feature.
Trace 13 (Chapter 5) shows the ordinary path: memory writes happen at a clean session end, so a crashed session loses everything it learned.
A LangGraph checkpointer takes a different path: it persists state at every superstep, and a `thread_id` in the invocation config resumes it — no clean shutdown required.
The restart test in this lab (`test_new_graph_over_same_file_resumes_the_thread`) builds a completely fresh graph and model over the same sqlite file and shows the prior turns are still there.
That is the mechanism Chapter 5 calls out in its "In other stacks" box for LangGraph.
