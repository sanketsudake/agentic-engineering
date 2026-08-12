# Lab 10 — Tracing and failure taxonomy

**Goal:** classify 20 recorded production sessions into six failure
classes, then compute what each class actually costs — not per request,
but per solved task.

**Level:** L3 · **Stack:** plain Python · **Time:** ~60 min · offline, no
model

**Offline mode (default, no keys, no model at all):**

```bash
uv sync
uv run pytest                      # 6 red tests are your task list
```

**Reference check:**

```bash
LAB_TARGET=solution uv run pytest  # the reference detectors passing
```

This lab needs no model. Whether a transcript is a runaway loop or a
swallowed error is a fact about the transcript, not something a judge
model has to guess — so it is testable offline, deterministically, every
time.

## Your task

1. Read `transcripts/prod001.jsonl` through `prod020.jsonl`. Each is one
   recorded session, one JSON message per line (see
   `worksheet_common.transcripts.load_transcript`). Some assistant
   messages carry a `"usage"` dict: `{"input_tokens": N, "output_tokens": N}`.
2. Open `starter/tracing/classify.py`. The docstring on `classify()` is
   the full spec: six mechanical definitions, checked in priority order.
   Implement it. You are writing detectors, not training a model — every
   class has a precise, checkable rule.
3. Open `starter/tracing/costs.py`. Implement `session_cost()` (sum usage
   tokens times price) and `cost_per_solve()` (total spend across every
   session, divided by the count of SUCCESS sessions only).
4. Run `uv run pytest` until it is green.

**Done means:** `uv run pytest` is fully green against `starter/`, with at
least 90% classification accuracy across all 20 fixtures.

## What this proves

Trace 32 (Chapter 12) walks a bad session through a trace: the operator
does not read the transcript first, they read the classification. The
taxonomy is the backlog — an operator who reads twenty transcripts by hand
fixes twenty incidents. An operator who classifies them first fixes six
classes, and the fix for RUNAWAY_LOOP stops the next forty runaway loops
too, not just the one they happened to read.

Cost per solve is the other half of the point. A dashboard that reports
"average cost per request" hides the failures: a session that loops three
times before giving up costs three times as much and produced nothing.
Dividing total spend by SUCCESS count, not by request count, is the number
that tells you what a finished task actually costs — failures included,
because they are not free.
