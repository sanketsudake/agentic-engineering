# The 35 traces

Every trace follows one event end to end —
from the message you send to the answer the agent returns,
through every component that touches it on the way.
The master trace is **Trace 2** (a user request becomes a finished task, Chapter 1);
Chapters 2–12 zoom into their segment of it,
and Part E traces run above it at org scale.

Traces link to their chapter as chapters ship; unlinked traces are planned.

## Part A — Foundations

**Chapter 1 — The Agent Loop: Big Picture**

1. [What happens when you send one message to a model](chapters/ch01.md#trace-1-what-happens-when-you-send-one-message-to-a-model) · L1
2. [What happens when a user request becomes a finished task](chapters/ch01.md#trace-2-what-happens-when-a-user-request-becomes-a-finished-task) · L1 · **master trace**

**Chapter 2 — Models & the API Surface** (zooms step 3 of Trace 2)

3. What happens when you demand output matching a schema · L1
4. What happens when the model decides to call a tool · L1
5. What happens when a response streams · L1
6. What happens when a prompt cache hits — and misses · L2

**Chapter 3 — Context Engineering** (zooms steps 2 and 6)

7. What happens when the context for a turn is assembled · L1
8. What happens when the context window fills · L2

## Part B — Capabilities

**Chapter 4 — Tool Design & MCP** (zooms steps 4–6)

9. What happens when a tool call executes end to end · L1
10. What happens when a tool call fails · L2
11. What happens when the agent calls an MCP server · L1

**Chapter 5 — Memory & State** (zooms steps 2 and 9)

12. What happens when an agent recalls a fact from memory · L2
13. What happens when a session ends and memory is written · L2

**Chapter 6 — Retrieval & RAG** (zooms steps 2 and 5)

14. What happens when a document becomes searchable · L1
15. What happens when a RAG query runs · L1
16. What happens when the agent searches instead · L2

## Part C — Coding agents

**Chapter 7 — Inside a Coding-Agent Harness** (zooms steps 1, 4, and 9)

17. What happens when a coding-agent session starts · L1
18. What happens when the harness gates a dangerous action · L1
19. What happens when a hook fires · L2
20. What happens when a skill or slash command is invoked · L2

**Chapter 8 — Operating Coding Agents: Workflows** (runs Trace 2 as a managed workflow)

21. What happens when a feature ships spec-first · L2
22. What happens when work is delegated to a subagent · L2
23. What happens when a CI agent handles a pull request · L2

## Part D — Systems

**Chapter 9 — Multi-Agent Orchestration** (runs many Trace 2s)

24. What happens when an orchestrator fans work out · L2
25. What happens when one agent hands off to another · L2
26. What happens when two agents write the same artifact · L3

**Chapter 10 — Evals** (measures Trace 2)

27. What happens when an eval suite runs · L2
28. What happens when an LLM judge grades a transcript · L2

**Chapter 11 — Safety & Guardrails** (gates steps 4–6)

29. What happens when a prompt injection arrives in tool output · L2
30. What happens when an agent tries to exfiltrate data · L3

**Chapter 12 — Production Ops, Cost & Latency** (operates Trace 2 at scale)

31. What happens when a production request fails over · L2
32. What happens when a bad session is traced · L2
33. What happens when the underlying model is upgraded · L3

## Part E — Judgment

**Chapter 13 — Architecture Judgment & Org Adoption** (above Trace 2, org scale)

34. What happens when an agent change ships across an organization · L3
35. What happens when a prompt-injection incident is triaged · L3

Chapter 14 carries no traces; it holds the lineage, the frontier bets, and the capstones.
