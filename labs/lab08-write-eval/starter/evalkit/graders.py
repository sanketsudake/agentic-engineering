"""Lab 8 — your task: write the graders (Trace 27, Trace 28; Chapter 10).

Each grader takes the same two arguments: the finished `transcript` (the
list of message dicts `run_agent()` produces — see Lab 3) and the `task`
dict it was run against (`tasks.py`: id, question, script, expected_answer,
required_tools). Every grader returns a float in [0.0, 1.0].
"""
from __future__ import annotations


def exact_grader(transcript: list[dict], task: dict) -> float:
    """1.0 if the agent's final answer equals `task["expected_answer"]`, else 0.0.

    The final answer is the `content` of the transcript's last assistant
    message that has one (an assistant turn with only `tool_calls` has
    `content=None` — see Lab 3's `run_agent()` contract). If the agent
    never produced a final answer (it hit `max_turns`), score 0.0.
    """
    raise NotImplementedError("compare the final answer to task['expected_answer']")


def trajectory_grader(transcript: list[dict], task: dict) -> float:
    """1.0 if `task["required_tools"]` were called, in that order, else 0.0.

    "In that order" means a subsequence match: other tool calls may appear
    between the required ones, but the required names must show up in the
    same relative order somewhere among the transcript's tool calls.
    """
    raise NotImplementedError("check required_tools as an ordered subsequence")


def judge_grader(transcript: list[dict], task: dict, judge_model) -> float:
    """1.0 if the injected `judge_model` scores this transcript a pass.

    Build a rubric prompt that includes the FULL transcript (not just the
    final answer — a judge that only sees the answer cannot catch a
    silently swallowed tool error; Trace 28). Call
    `judge_model.complete(messages, tools)` the same way `run_agent()`
    calls a model (`tools={}` is fine — the judge never calls a tool
    itself). Parse the reply for a "1"/"0" verdict.
    """
    raise NotImplementedError("prompt the judge with the full transcript, parse its verdict")
