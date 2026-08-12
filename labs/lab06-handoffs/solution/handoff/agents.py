"""Reference solution for Lab 6: multi-agent handoffs (OpenAI Agents SDK)."""
from __future__ import annotations

from agents import Agent, RunResult, Runner


def build_agents() -> tuple[Agent, Agent, Agent]:
    refunds = Agent(
        name="Refunds",
        instructions=(
            "You are the refunds specialist. Answer refund and billing "
            "questions briefly and directly."
        ),
    )
    tech = Agent(
        name="Tech Support",
        instructions=(
            "You are the tech support specialist. Answer technical and "
            "product questions briefly and directly."
        ),
    )
    triage = Agent(
        name="Triage",
        instructions=(
            "You triage customer messages. Hand off refund or billing "
            "questions to the Refunds agent, and technical or product "
            "questions to the Tech Support agent. Answer directly only "
            "when no specialist is needed."
        ),
        handoffs=[refunds, tech],
    )
    return triage, refunds, tech


def run_triage(question: str) -> RunResult:
    triage, _refunds, _tech = build_agents()
    return Runner.run_sync(triage, question)
