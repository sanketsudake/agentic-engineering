# Lab 9 — Operate a coding agent

**Goal:** study three recorded sessions where a coding agent did real damage,
then write the permission rules and operating instructions that would have
stopped each one — a provided rule engine proves it.

**Level:** L2 · **Stack:** plain Python · **Time:** ~45 min · offline, no model

**Offline mode (default, no keys, no model at all):**

```bash
uv sync
uv run pytest                      # 7 red tests are your task list
```

**Reference check:**

```bash
LAB_TARGET=solution uv run pytest  # the reference rules and CLAUDE.md passing
```

This lab needs no model.
Whether a policy blocks the right calls is a fact about the policy, not
about anything a model generates —
so it is testable offline, deterministically, every time.

## Your task

1. Read each transcript in `transcripts/`: `session1.jsonl`, `session2.jsonl`,
   `session3.jsonl`.
Each one is a recorded session, one JSON message per line
   (see `worksheet_common.transcripts.load_transcript`).
Find the incident in each: the tool call that caused damage.
2. Open `starter/policy/engine.py` and read it.
It is provided and working —
   your task is not to write a rule engine, it is to write rules for it.
`call_signature()` shows you exactly what a rule matches against:
   a Bash rule matches the command string; a Read/Write/Edit rule matches
   the path.
3. Edit `starter/policy/settings.json`.
Add the narrowest deny or ask rule
   that stops each incident, in the syntax `Tool` or `Tool(specifier)`
   (a trailing `*` is a prefix match) —
   see `notes/research-notes.md` under "Harness facts (Claude Code)" for
   the exact rule syntax and the deny → ask → allow evaluation order this
   engine mirrors.
Keep the legitimate calls in each transcript working:
   `Read(src/main.py)`, `Bash(pytest -q)`, `Edit(src/main.py)`,
   `Bash(git status)`.
A rule that blocks those fails the lab, even if it also stops the incident.
4. Edit `starter/policy/CLAUDE.md`.
Write the operating guidance a human
   reviewer would want next to the rules: why each rule exists, and what to
   do instead.

**Done means:** `uv run pytest` is fully green against `starter/`.

## What this proves

Trace 18 (Chapter 7) walks a dangerous call through the gate: hook, then
deny, then ask, then allow, then the mode default —
first match wins, and specificity does not matter.
This lab puts you on the other side of that gate: the operator who writes
the rules, not the harness that runs them.

Chapter 8 makes the point this lab is built to demonstrate: operating a
coding agent is a policy job, not a babysitting job.
An operator who reads every transcript and approves every call by hand
does not scale past one agent.
An operator who turns each incident into a scoped, tested rule does.

The three incidents cover the recurring damage classes from real coding-agent
use: an unscoped destructive command, a secret leaving its file, and a
change that reaches outside the project's boundary.
The same three rules, once written, keep stopping the same three mistakes —
across every future session, without anyone re-reading a transcript.
