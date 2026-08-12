"""Lab 4 checker: 9 tests define "done".

They run against starter/ by default (your task list) and against solution/
with LAB_TARGET=solution (the reference passing).
"""
import copy

import pytest


def test_under_budget_returned_unchanged(fit_module, tokens_module, tiny_session):
    budget = tokens_module.total_tokens(tiny_session) + 100  # generous headroom
    result = fit_module.fit_context(tiny_session, budget)
    assert result == tiny_session
    assert result is not tiny_session  # a NEW list, per the contract
    assert not any("compacted" in (m.get("content") or "") for m in result)


def test_oversized_tool_result_truncated_even_under_budget(fit_module):
    system = {"role": "system", "content": "You are an agent."}
    task = {"role": "user", "content": "Summarize the log."}
    big = "x" * 5000  # 1,250 tokens of content, well over the 600-token cap
    messages = [
        system,
        task,
        {"role": "assistant", "content": None,
         "tool_calls": [{"id": "c1", "name": "read_log", "input": {}}]},
        {"role": "tool", "tool_call_id": "c1", "content": big},
        {"role": "assistant", "content": "Done.", "tool_calls": []},
    ]
    result = fit_module.fit_context(messages, budget=100_000)  # plenty of budget overall

    assert len(result) == len(messages)  # nothing dropped
    assert not any(
        m["role"] == "system" and "compacted" in m["content"] for m in result[2:]
    )
    tool_msg = next(m for m in result if m["role"] == "tool")
    expected = big[: fit_module.TOOL_TRUNCATE_TOKENS * 4] + fit_module.TRUNCATE_MARKER
    assert tool_msg["content"] == expected
    assert tool_msg["content"].endswith("[truncated]")


def test_over_budget_drops_oldest_turn_first(fit_module, tokens_module, coding_session):
    baseline = fit_module.fit_context(coding_session, budget=10 ** 9)  # nothing dropped
    full_cost = tokens_module.total_tokens(baseline)
    first_turn_cost = tokens_module.message_tokens(baseline[2]) + tokens_module.message_tokens(baseline[3])

    budget = full_cost - (first_turn_cost // 2)
    result = fit_module.fit_context(coding_session, budget)

    assert tokens_module.total_tokens(result) <= budget
    ids = [m.get("tool_call_id") for m in result if m["role"] == "tool"]
    assert "c1" not in ids  # the oldest turn (list_dir) is gone
    assert "c9" in ids      # the most recent tool turn survives
    assert result[2]["role"] == "system" and "compacted" in result[2]["content"]


def test_system_and_task_survive_extreme_budget(fit_module, tokens_module, coding_session):
    system, task = coding_session[0], coding_session[1]
    baseline = fit_module.fit_context(coding_session, budget=10 ** 9)
    total_msgs = len(baseline) - 2  # everything after system + task

    marker = {"role": "system", "content": f"[context compacted: {total_msgs} messages dropped]"}
    budget = (tokens_module.message_tokens(system)
              + tokens_module.message_tokens(task)
              + tokens_module.message_tokens(marker))

    result = fit_module.fit_context(coding_session, budget)

    assert result[0] == system
    assert result[1] == task
    assert len(result) == 3  # only system, task, marker survive
    assert result[2]["content"] == marker["content"]
    assert tokens_module.total_tokens(result) <= budget


def test_marker_inserted_exactly_once_with_correct_count(fit_module, tokens_module, coding_session):
    baseline = fit_module.fit_context(coding_session, budget=10 ** 9)
    full_cost = tokens_module.total_tokens(baseline)

    result = fit_module.fit_context(coding_session, budget=full_cost // 3)

    markers = [m for m in result if m["role"] == "system" and "compacted" in m.get("content", "")]
    assert len(markers) == 1
    assert result[2] is markers[0]  # right after the task message

    n_dropped = int(markers[0]["content"].split(":")[1].split()[0])
    kept_after_marker = len(result) - 3  # exclude system, task, marker
    assert n_dropped == (len(baseline) - 2) - kept_after_marker


def test_recent_turns_kept_intact(fit_module, tokens_module, coding_session):
    baseline = fit_module.fit_context(coding_session, budget=10 ** 9)
    base_cost = tokens_module.message_tokens(baseline[0]) + tokens_module.message_tokens(baseline[1])
    marker_guess = {"role": "system", "content": "[context compacted: 99 messages dropped]"}

    # Just enough for system + task + marker + the final (short) turn.
    budget = (base_cost
              + tokens_module.message_tokens(marker_guess)
              + tokens_module.message_tokens(baseline[-1])
              + 2)

    result = fit_module.fit_context(coding_session, budget)
    assert "compacted" in result[2]["content"]  # confirms a drop happened

    kept_portion = result[3:]  # everything after system, task, marker
    tail_of_baseline = baseline[-len(kept_portion):] if kept_portion else []
    assert kept_portion == tail_of_baseline


def test_large_fixture_result_stays_under_budget(fit_module, tokens_module, coding_session):
    budget = 400
    result = fit_module.fit_context(coding_session, budget)
    assert tokens_module.total_tokens(result) <= budget
    assert result[0] == coding_session[0]
    assert result[1] == coding_session[1]


def test_input_list_not_mutated(fit_module, coding_session):
    original = copy.deepcopy(coding_session)
    fit_module.fit_context(coding_session, budget=150)  # small enough to force truncation and drops
    assert coding_session == original


def test_raises_on_budget_too_small(fit_module, coding_session):
    with pytest.raises(ValueError):
        fit_module.fit_context(coding_session, budget=1)
