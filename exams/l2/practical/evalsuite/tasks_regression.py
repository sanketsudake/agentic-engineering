"""Your regression task goes here — README, step 3.

`tasks.py` is frozen; the eval grows here, so the diff that fixes the
agent and the diff that guards the fix stay separate.

A regression task is a normal task dict, plus `"cycle": True`. Build it
so that an agent which silently loses an oversized tool result CANNOT
score 1.0: plant one tool call whose result exceeds
`agent.loop.RESULT_BUDGET`, and use `reactive_entry` so the scripted
model gives the correct final answer only after a tool result actually
reaches the transcript. `tests/test_practical.py` runs your task against
both your fixed agent (must score 1.0) and the frozen
`agent/buggy_reference.py` (must score below 1.0).

Template — fill in the blanks and add the dict to `REGRESSION_TASKS`:

    {
        "id": "regress-big-result-1",
        "question": "<a question whose answer needs a big file>",
        "script": [
            ModelResponse(tool_calls=[ToolCall("t1", "read_file",
                                               {"path": "<a big file>"})]),
            reactive_entry(
                on_result=ModelResponse(text="<the correct final answer>"),
                on_missing=ModelResponse(
                    tool_calls=[ToolCall("t2", "read_file",
                                         {"path": "<the same big file>"})]),
            ),
        ],
        "cycle": True,  # the buggy loop re-asks forever; the script must not run out
        "expected_answer": "<the correct final answer>",
        "required_tools": ["read_file"],
    }
"""
from __future__ import annotations

from worksheet_common import ModelResponse, ToolCall

from evalsuite.tasks import reactive_entry

# Replace the empty list with at least one task built from the template above.
REGRESSION_TASKS: list[dict] = []
