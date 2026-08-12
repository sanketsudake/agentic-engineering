# MAINTAINERS — L1 practical reference notes

Maintainer-only.
Candidates: reading this file before finishing is scoring against the key mid-exam —
close it and go read the docstring spec in `assemble/agent.py`.

## The shipped state

The repo ships with `run_agent()` raising `NotImplementedError`,
so all 10 checks fail: `10 failed`.
That is intentional — the candidate assembles the loop.

## The reference implementation (the candidate's job)

Replace the `raise NotImplementedError(...)` line in
`assemble/agent.py` (keep the docstring) with:

```python
    transcript: list[dict] = [{"role": "user", "content": user_msg}]
    for _ in range(max_turns):
        resp = model.complete(transcript, toolbox["tool_defs"])
        transcript.append({
            "role": "assistant",
            "content": resp.text,
            "tool_calls": [{"id": c.id, "name": c.name, "input": c.input}
                           for c in resp.tool_calls],
        })
        if resp.text and DONE_MARKER in resp.text:
            answer = resp.text.split(DONE_MARKER, 1)[1].strip()
            return AgentResult(answer=answer, transcript=transcript,
                               stopped="done")
        if not resp.tool_calls:
            return AgentResult(answer=resp.text or "", transcript=transcript,
                               stopped="done")
        for call in resp.tool_calls:
            transcript.append({"role": "tool", "tool_call_id": call.id,
                               "content": dispatcher(call, toolbox)})
    return AgentResult(answer="", transcript=transcript, stopped="max_turns")
```

With the edit applied: `10 passed`.

Note the fresh-variant deltas from Lab 3's solution —
a copy-paste of that loop fails 3 of the 10 checks:
results must come from the injected `dispatcher(call, toolbox)`
(not a direct registry call),
and the `DONE:` marker stops the loop before any dispatch,
returning only the suffix.

## Re-verifying both states

```bash
cd exams/l1/practical
uv sync
uv run pytest            # shipped: 10 failed
# apply the reference edit above
uv run pytest            # fixed: 10 passed
# revert to the NotImplementedError line; leave the repo in the shipped state
uv run pytest            # back to 10 failed
```

`build/check_book.py` (repo root) checks the exam's
"10 checks × 3 points" line against the test count in `tests/test_practical.py` —
keep exactly 10 `def test_` functions in that one file.

## CI verification (reference/ + LAB_TARGET)

`reference/agent_ref.py` carries the reference implementation as an
importable module. `tests/conftest.py` aliases it over `assemble.agent`
when `LAB_TARGET=solution`, so the labs CI workflow proves the practical
is completable without shipping the answer in the candidate's path.
Keep it in sync with the reference edit above.
