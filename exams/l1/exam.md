# L1 Exam — The Builder

This exam verifies: you can explain the agent loop and build a working agent from parts.
Score yourself against `exams/l1/key.md` after finishing — not before.

**Time:** 2 hours (Section A closed-book, 75 min; Section B open-repo, 45 min).
**Materials:** Section A: nothing. Section B: this repo, no live model access needed.
**Total:** 100 points
**Pass:** at least 70 points overall.

## Section A — Written (70 points)

**E1.A1 (10 pts) — A teammate asks your agent to "rename the deploy flag and update its two call sites", presses Enter, and forty seconds later reads the answer. From memory, narrate everything that happened in between, step by step, naming the acting component at each step?**

**E1.A2 (10 pts) — You are adding a `search_tickets` tool to an agent. List every part its definition must contain, say who reads each part — the model, the harness, or the provider — and explain what goes wrong when the description says only what the tool does?**

**E1.A3 (10 pts) — After your agent's `read_file` tool runs, the model discusses the file's contents in its next response. A teammate concludes the provider stored the file server-side for the session. Correct them: explain what actually crosses the wire on the next request, and what that implies for a 40-turn session?**

**E1.A4 (10 pts) — Name the segments of the context window an agent turn carries, say what each one holds, and identify which segment comes to dominate a long agent session — with the token arithmetic that shows why?**

**E1.A5 (10 pts) — You register five new tools on an agent. A week of transcripts shows none of them was ever called, yet answers on old tasks got worse and cost per session rose. Explain both effects from the mechanism, and state what you would change?**

**E1.A6 (10 pts) — One team answers support questions over 200,000 policy documents; another builds a coding agent over a repository that changes hourly. One should use one-shot RAG, the other agentic search. Assign each and defend both choices from freshness, cost per query, and query shape?**

**E1.A7 (10 pts) — A dispatcher catches every tool exception, writes it to the operator log, and returns the string `"done"` to the loop. Predict the agent's downstream behavior when its `write_file` call fails, describe how the transcript ends, and explain why this failure class is the hardest to spot?**

## Section B — Practical (30 points)

Open `exams/l1/practical/` and follow its README:
assemble a working micro-agent by implementing `run_agent()` against a
provided dispatcher, a provided toolbox, and a scripted model.
Scored by pytest: 10 checks × 3 points. Paste your pytest output into the score sheet.

## Score sheet

| Section | Max | Your score |
|---|---|---|
| A — Written | 70 | |
| B — Practical | 30 | |
| **Total** | **100** | |
