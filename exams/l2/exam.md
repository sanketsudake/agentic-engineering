# L2 Exam — The Operator

This exam verifies: you can independently build, debug, and eval a production agent.
Score yourself against `exams/l2/key.md` after finishing — not before.

**Time:** 3 hours (Sections A–B closed-book, 90 min; Section C open-repo, 90 min).
**Materials:** Sections A–B: nothing. Section C: this repo, no live model access needed.
**Total:** 100 points
**Pass:** at least 70 points overall AND at least 18/30 on Section C.

## Section A — Written (60 points)

**E2.A1 (5 pts) — A model response ends with `stop_reason: "tool_use"`. Narrate, step by step and naming the acting component at each step, everything that happens between that response and the start of the next model call?**

**E2.A2 (5 pts) — An agent sends the same long system prompt and tool set twice within a minute, and the second request costs a fraction of the first. Explain the mechanism that makes the second request cheaper, and name the usage field that proves it worked?**

**E2.A3 (10 pts) — A teammate refactors your loop so that each of the model's three parallel tool calls gets its result sent back in its own separate message, "so the model sees results sooner". Predict what happens on the next request, and explain why all three results must return together in one message?**

**E2.A4 (10 pts) — A nightly reconciliation job runs five fixed steps: export, validate, transform, post to the billing system, notify. A team proposes replacing the pipeline with an agent that chooses its own steps. Argue the decision step by step using the cost of variance: where does the model choose, where does code choose, and why?**

**E2.A5 (10 pts) — Your team swaps a strict code grader for an LLM judge, and the suite's pass rate jumps from 62% to 84% overnight with no agent change. Why can you not report the 84%, and what work makes the judge's number admissible?**

**E2.A6 (10 pts) — An unattended agent ran a schema migration in production, and the migration was applied twice. Walk your diagnosis: what you read first, the hypotheses that separate a model re-request from a harness retry and the evidence that decides between them, and the fix that removes the whole failure class rather than this one incident?**

**E2.A7 (10 pts) — Your agent's eval suite is green on every run, yet this week users report confidently wrong answers. The suite has not changed in six weeks. Walk your diagnosis: what you compare first, and how you decide whether the suite, the graders, or the fleet is lying?**

## Section B — Code reading (10 points)

**E2.B1 (10 pts) — The snippet below has three planted bugs. Find each, explain its production impact, and rank the three by severity?**

The loop otherwise follows the Lab 3 pattern.
Exactly three bugs are planted.
The comments state guaranteed behavior:
`tools.dispatch` validates input, surfaces failures as `"error: ..."` text,
never raises, and never returns oversized text — do not report bugs inside it.

```python
import time


def build_system_prompt() -> str:
    return ("You are a code-reading assistant for one repository.\n"
            f"Current time: {time.time()}\n"
            "Use the read_file tool to inspect files before answering.")


def run_agent(client, tools, user_msg, max_turns=6):
    # tools.dispatch(call) validates the input and returns the tool's
    # output, or an "error: ..." string. It never raises, and it caps
    # oversized results itself.
    messages = [{"role": "user", "content": user_msg}]
    turns = 0
    while True:
        resp = client.complete(system=build_system_prompt(),
                               messages=messages,
                               tools=tools.schemas())
        messages.append({"role": "assistant", "content": resp.content})
        if not resp.tool_calls:
            return resp.text
        results = {}
        for call in resp.tool_calls:  # e.g. read_file on two paths at once
            results[call.name] = {"type": "tool_result",
                                  "tool_use_id": call.id,
                                  "content": tools.dispatch(call)}
        messages.append({"role": "user", "content": list(results.values())})
        turns += 1
        if turns > max_turns:
            return ""
```

3 points per bug found and explained; 1 point for a defensible severity ranking.

## Section C — Practical (30 points)

Open `exams/l2/practical/` and follow its README.
A vendored tool-loop agent fails 3 of the 10 tasks in the provided eval suite.
Run the eval, diagnose the failure from the transcripts, fix the agent,
then add a regression task in `evalsuite/tasks_regression.py`
that would catch the bug class if it ever returned.
Scored by pytest: 10 checks × 3 points. Paste your pytest output into the score sheet.

## Score sheet

| Section | Max | Your score |
|---|---|---|
| A — Written | 60 | |
| B — Code reading | 10 | |
| C — Practical | 30 | |
| **Total** | **100** | |
