# Lab 8 — Write an eval

**Goal:** write graders and a runner for an eval,
then prove it actually works —
your eval must score a working agent well and a broken one badly,
on the same 10 tasks.

**Level:** L2 · **Stack:** plain Python · **Time:** ~60 min

**Offline mode (default, no keys):**

```bash
uv sync
uv run pytest                      # 7 red tests are your task list
```

**Reference check:**

```bash
LAB_TARGET=solution uv run pytest  # the reference implementation passing
```

## Your task

1. Read `tasks.py` (provided, 10 tasks) and `agents_under_test/` (provided, two agents).
   `good_agent.py` is a vendored copy of Lab 3's solution loop.
   `buggy_agent.py` is the same loop with one except-branch changed: a tool exception becomes `""` instead of `"error: <message>"`.
   The harness never crashes and the transcript stays well-formed — the loop still "works".
2. Open `starter/evalkit/graders.py`.
   Implement three graders, each scoring one finished transcript against its task:
   - `exact_grader` — does the final answer match `expected_answer`?
   - `trajectory_grader` — were `required_tools` called, in order?
   - `judge_grader` — call the injected judge model with a rubric prompt that includes the FULL transcript, and parse its 0/1 verdict.
3. Open `starter/evalkit/runner.py`.
   Implement `run_eval(agent_fn, tasks, graders)`: run every task through the agent, score it with every grader, and return a report with per-task scores and an aggregate.
4. Make the 7 tests in `tests/test_lab.py` pass.
   The last two run your finished eval end to end, once against `good_agent` and once against `buggy_agent` — that pair is the point of the lab, not a formality.

**Done means:** `uv run pytest` is fully green against `starter/`,
and — this is the real bar — your eval scores the good agent's aggregate
`>= 0.8` and the buggy agent's `<= 0.5`,
on the same 10 tasks.

## What this proves

An eval that cannot catch a planted regression is decoration
(Trace 27, Trace 28; Chapter 10).
It is easy to write graders that look reasonable and pass every test you
hand-picked,
while never actually separating a working agent from a broken one.
This lab makes that failure mode impossible to miss:
you run your own eval against both agents and read the two numbers.

The bug itself is small on purpose —
one `except` clause that turns a tool failure into silence instead of a
visible error.
Six of the ten tasks plant that failure;
a working agent sees the error, retries with corrected arguments, and
answers right.
The buggy agent sees an empty string that looks like success, never
retries, and answers confidently wrong.
`exact_grader` catches the wrong answer.
`trajectory_grader` catches the missing retry call.
`judge_grader` catches it too, because it reads the WHOLE transcript —
including the swallowed tool result — not just the final answer
(Trace 28 is exactly this: what an LLM judge sees determines what it can
grade).

There is no live mode for this lab on purpose:
the scripted model and the scripted judge model both need to behave
deterministically for the pass/fail bar to mean anything run to run.
