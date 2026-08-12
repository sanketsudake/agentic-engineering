# L2 Exam — The Operator

This exam verifies: you can independently build, debug, and eval a production agent.
Score yourself against `exams/l2/key.md` after finishing — not before.

**Time:** 3 hours (Sections A–B closed-book, 90 min; Section C open-repo, 90 min).
**Materials:** Sections A–B: nothing. Section C: this repo, no live model access needed.
**Total:** 100 points
**Pass:** at least 70 points overall AND at least 18/30 on Section C.

## Section A — Written (60 points)

**E2.A1 (5 pts) — Narrate every step between a `tool_use` response and the start of the next model call.**

A model response ends with `stop_reason: "tool_use"`.
Name the acting component at each step.
Keep the steps in order.

**E2.A2 (5 pts) — Explain why the second request costs less, and name the usage field that proves it.**

An agent sends the same long system prompt and the same tool set twice within one minute.
The second request costs a fraction of the first.

**E2.A3 (10 pts) — Predict what happens on the next request, and explain why all three results must return in one message.**

The model emits three parallel tool calls.
A teammate refactors your loop so that each result returns in its own separate message,
"so the model sees results sooner".

**E2.A4 (10 pts) — Decide whether an agent replaces the pipeline, and argue the decision from the cost of variance.**

A nightly reconciliation job runs five fixed steps:
export, validate, transform, post to the billing system, notify.
A team proposes to replace the pipeline with an agent that chooses its own steps.

Your answer must:

- argue the decision one step at a time;
- say where the model chooses;
- say where code chooses;
- give the reason in each case.

**E2.A5 (10 pts) — Explain why you cannot report the new pass rate, and name the work that makes the judge's number admissible.**

Your team replaces a strict code grader with an LLM judge.
Overnight the pass rate of the suite goes from 62% to 84%.
The agent did not change.

**E2.A6 (10 pts) — Walk your diagnosis of a schema migration that ran twice.**

An unattended agent ran a schema migration in production.
The migration was applied twice.

Your answer must:

- say what you read first;
- give the hypotheses that separate a model re-request from a harness retry;
- name the evidence that decides between them;
- give the fix that removes the whole failure class, not only this one incident.

**E2.A7 (10 pts) — Walk your diagnosis of an eval suite that stays green while production fails.**

Your agent's eval suite is green on every run.
This week users report confidently wrong answers.
The suite has not changed for six weeks.

Your answer must:

- say what you compare first;
- explain how you decide which one is wrong: the suite, the graders, or the fleet.

## Section B — Code reading (10 points)

**E2.B1 (10 pts) — Find the three planted bugs in the snippet below, explain the production impact of each, and rank the three by severity.**

The loop follows the Lab 3 pattern in every other respect.
Exactly three bugs are planted.
The comments state guaranteed behavior:
`tools.dispatch` validates its input, returns failures as `"error: ..."` text,
never raises an exception, and never returns oversized text.
Do not report bugs inside `tools.dispatch`.

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
A vendored tool-loop agent fails 3 of the 10 tasks in the eval suite that the project provides.

1. Run the eval.
2. Diagnose the failure from the transcripts.
3. Fix the agent.
4. Add a regression task in `evalsuite/tasks_regression.py` that catches the bug class if it returns.

Scored by pytest: 10 checks × 3 points. Paste your pytest output into the score sheet.

## Score sheet

| Section | Max | Your score |
|---|---|---|
| A — Written | 60 | |
| B — Code reading | 10 | |
| C — Practical | 30 | |
| **Total** | **100** | |
