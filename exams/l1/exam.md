# L1 Exam — The Builder

This exam verifies: you can explain the agent loop and build a working agent from parts.
Score yourself against `exams/l1/key.md` after finishing — not before.

**Time:** 2 hours (Section A closed-book, 75 min; Section B open-repo, 45 min).
**Materials:** Section A: nothing. Section B: this repo, no live model access needed.
**Total:** 100 points
**Pass:** at least 70 points overall.

## Section A — Written (70 points)

**E1.A1 (10 pts) — Narrate every step between the request and the answer, and name the acting component at each step.**

A teammate asks your agent to rename the deploy flag and to update its two call sites.
The teammate presses Enter.
Forty seconds later the teammate reads the answer.
Work from memory.
Keep the steps in order.

**E1.A2 (10 pts) — Explain what a tool definition contains, who reads each part, and how a weak description fails.**

You add a `search_tickets` tool to an agent.

Your answer must:

- list every part that the definition must contain;
- name who reads each part — the model, the harness, or the provider;
- explain what goes wrong when the description says only what the tool does.

**E1.A3 (10 pts) — Correct a teammate who believes that the provider keeps your file server-side.**

Your agent runs its `read_file` tool.
In its next response, the model discusses the contents of the file.
A teammate concludes that the provider stored the file server-side for the session.

Your answer must:

- correct the teammate;
- explain what crosses the wire on the next request;
- explain what that means for a session of 40 turns.

**E1.A4 (10 pts) — Name the segments of the context window that an agent turn carries.**

Your answer must:

- name each segment, and say what it holds;
- identify the segment that comes to dominate a long agent session;
- show the token arithmetic that explains why.

**E1.A5 (10 pts) — Explain why five unused tools raise the cost and lower the answer quality.**

You register five new tools on an agent.
A week of transcripts shows that the agent called none of them.
But the answers to old tasks got worse, and the cost per session rose.
Explain both effects from the mechanism.
Then state what you change.

**E1.A6 (10 pts) — Assign one-shot RAG to one team and agentic search to the other, then defend both choices.**

One team answers support questions over 200,000 policy documents.
The other team builds a coding agent over a repository that changes every hour.
Defend each choice from freshness, cost per query, and the shape of the queries.

**E1.A7 (10 pts) — Predict what the agent does when its `write_file` call fails, and describe how the transcript ends.**

A dispatcher catches every tool exception.
It writes the exception to the operator log.
Then it returns the string `"done"` to the loop.

Your answer must:

- predict what the agent does downstream when the `write_file` call fails;
- describe how the transcript ends;
- explain why this failure class is the hardest one to find.

## Section B — Practical (30 points)

Open `exams/l1/practical/` and follow its README.
Assemble a working micro-agent: implement `run_agent()` against the dispatcher,
the toolbox, and the scripted model that the project provides.
Scored by pytest: 10 checks × 3 points. Paste your pytest output into the score sheet.

## Score sheet

| Section | Max | Your score |
|---|---|---|
| A — Written | 70 | |
| B — Practical | 30 | |
| **Total** | **100** | |
