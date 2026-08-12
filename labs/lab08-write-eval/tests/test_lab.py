"""Lab 8 checker: 7 tests define "done".

They run against starter/ by default (your task list) and against solution/
with LAB_TARGET=solution (the reference passing). `agents_under_test/` and
`tasks.py` are provided and identical either way.
"""
from worksheet_common import ModelResponse, ScriptedModel

# The 6 tasks (of 10) whose script plants a tool error — see tasks.py.
ERROR_TASK_IDS = {
    "price-err-1", "price-err-2",
    "weather-err-1", "weather-err-2",
    "docs-err-1", "docs-err-2",
}


def _transcript(final_text, tool_calls_and_results=()):
    """A minimal transcript: a user turn, one assistant+tool pair per
    (name, args, result) triple, then a final assistant answer."""
    t = [{"role": "user", "content": "go"}]
    for i, (name, args, result) in enumerate(tool_calls_and_results):
        call_id = f"t{i}"
        t.append({"role": "assistant", "content": None,
                  "tool_calls": [{"id": call_id, "name": name, "input": args}]})
        t.append({"role": "tool", "tool_call_id": call_id, "content": result})
    t.append({"role": "assistant", "content": final_text, "tool_calls": []})
    return t


def _judge_for(task_ids, correct_ids):
    """A scripted judge that gives an honest verdict per task, in task
    order: "1" for a task the agent actually got right, "0" for one it
    didn't."""
    return ScriptedModel([
        ModelResponse(text="1" if tid in correct_ids else "0") for tid in task_ids
    ])


def _graders_for(judge_model, graders):
    return {
        "exact": graders.exact_grader,
        "trajectory": graders.trajectory_grader,
        "judge": lambda transcript, task: graders.judge_grader(transcript, task, judge_model),
    }


def test_exact_grader_scores_matching_and_mismatched_answers(graders):
    task = {"id": "t", "expected_answer": "42"}
    assert graders.exact_grader(_transcript("42"), task) == 1.0
    assert graders.exact_grader(_transcript("43"), task) == 0.0


def test_exact_grader_handles_no_final_answer(graders):
    """A transcript that hit max_turns has no trailing text — score 0.0,
    never crash."""
    task = {"id": "t", "expected_answer": "42"}
    transcript = [
        {"role": "user", "content": "go"},
        {"role": "assistant", "content": None,
         "tool_calls": [{"id": "t1", "name": "x", "input": {}}]},
        {"role": "tool", "tool_call_id": "t1", "content": "r"},
    ]
    assert graders.exact_grader(transcript, task) == 0.0


def test_trajectory_grader_checks_ordered_subsequence(graders):
    task = {"id": "t", "required_tools": ["search", "calculator"]}
    in_order = _transcript("ans", [("search", {}, "r1"), ("extra", {}, "r2"),
                                    ("calculator", {}, "r3")])
    out_of_order = _transcript("ans", [("calculator", {}, "r1"), ("search", {}, "r2")])
    missing = _transcript("ans", [("search", {}, "r1")])
    assert graders.trajectory_grader(in_order, task) == 1.0
    assert graders.trajectory_grader(out_of_order, task) == 0.0
    assert graders.trajectory_grader(missing, task) == 0.0


def test_judge_grader_parses_verdict_and_sees_full_transcript(graders):
    task = {"id": "t", "question": "How much does the gadget cost?",
            "expected_answer": "A gadget costs $14.99."}
    transcript = _transcript(
        "A gadget costs $0.00.",
        [("lookup_price", {"item": "gadgets"}, "error: no such item: gadgets")],
    )

    fail_judge = ScriptedModel([ModelResponse(text="0")])
    assert graders.judge_grader(transcript, task, fail_judge) == 0.0
    prompt = fail_judge.calls[-1][0]["content"]
    assert "error: no such item: gadgets" in prompt  # the tool failure, not just the answer
    assert "A gadget costs $0.00." in prompt          # the (wrong) final answer too

    pass_judge = ScriptedModel([ModelResponse(text="1")])
    assert graders.judge_grader(transcript, task, pass_judge) == 1.0


def test_runner_builds_per_task_report_and_aggregate(runner):
    class FakeResult:
        def __init__(self, transcript):
            self.transcript = transcript

    def agent_fn(task):
        return FakeResult(transcript=[{"role": "user", "content": task["question"]}])

    tasks = [{"id": "a", "question": "q1"}, {"id": "b", "question": "q2"}]
    graders = {
        "always_one": lambda transcript, task: 1.0,
        "always_zero": lambda transcript, task: 0.0,
    }
    report = runner.run_eval(agent_fn, tasks, graders)
    assert set(report["per_task"]) == {"a", "b"}
    for task_id in ("a", "b"):
        scores = report["per_task"][task_id]
        assert scores["always_one"] == 1.0
        assert scores["always_zero"] == 0.0
        assert scores["mean"] == 0.5
    assert report["aggregate"] == 0.5


def test_good_agent_clears_the_bar(runner, graders, tasks, good_agent):
    """The regression test, half 1: a working agent scores >= 0.8."""
    task_ids = [t["id"] for t in tasks]
    judge = _judge_for(task_ids, correct_ids=set(task_ids))  # good gets everything right
    report = runner.run_eval(good_agent, tasks, _graders_for(judge, graders))
    assert report["aggregate"] >= 0.8


def test_buggy_agent_misses_the_bar(runner, graders, tasks, buggy_agent):
    """The regression test, half 2: the planted-bug agent scores <= 0.5.

    An eval that cannot tell these two apart is decoration, not an eval.
    """
    task_ids = [t["id"] for t in tasks]
    correct_ids = set(task_ids) - ERROR_TASK_IDS
    judge = _judge_for(task_ids, correct_ids=correct_ids)
    report = runner.run_eval(buggy_agent, tasks, _graders_for(judge, graders))
    assert report["aggregate"] <= 0.5
