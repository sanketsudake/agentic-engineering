"""Lab 6 — your task: wire a triage agent that hands off to two specialists.

You are not writing the loop this time (Lab 3 did that). The OpenAI Agents
SDK's `Runner` owns the loop. Your job is to declare the agents and their
handoff relationships correctly — the SDK turns `handoffs=[...]` into tool
calls the model can choose, and `Runner` transfers the conversation to
whichever agent the model picked.
"""
from __future__ import annotations

from agents import Agent, RunResult, Runner


def build_agents() -> tuple[Agent, Agent, Agent]:
    """Build a triage agent that can hand off to two specialists.

    Returns `(triage, refunds, tech)`:

    - `refunds`: name it `"Refunds"`. Short instructions describing it as the
      agent that handles refund questions.
    - `tech`: name it `"Tech Support"`. Short instructions describing it as
      the agent that handles technical/product questions.
    - `triage`: name it `"Triage"`. Instructions telling it to route refund
      questions to `refunds`, technical questions to `tech`, and to answer
      directly when the question needs no specialist. Its `handoffs=` list
      must include both specialists, so the SDK generates a transfer tool
      for each (`transfer_to_refunds`, `transfer_to_tech_support`) and
      declares them to the model as part of `Agent(..., handoffs=[refunds, tech])`.

    Each agent's `instructions` become that agent's system prompt for every
    turn it owns — including turns after a handoff. That is how the tests
    detect a handoff actually happened: the request right after one carries
    the specialist's instructions, not the triage agent's.
    """
    raise NotImplementedError("build the triage, refunds, and tech agents")


def run_triage(question: str) -> RunResult:
    """Run the triage agent (and whichever specialist it hands off to) on `question`.

    Build fresh agents with `build_agents()`, then run the triage agent with
    `Runner.run_sync(triage, question)` and return the `RunResult` unchanged.

    The caller (a test, or your own code) reads:

    - `result.final_output` — the text the *last* agent to own the turn
      produced, whether that was `triage` itself or a specialist it handed
      off to.
    - `result.last_agent` — which `Agent` produced that final output. If a
      handoff happened, this is the specialist, not `triage` — that is the
      whole point of a handoff: it transfers ownership, not just a reply.

    Do not build the client here. `Runner` reads the SDK's default OpenAI
    client, which the caller (a test, via `set_default_openai_client`) has
    already pointed at the mock.
    """
    raise NotImplementedError("run the triage agent and return the RunResult")
