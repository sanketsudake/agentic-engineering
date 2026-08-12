"""The 10 questions the baseline and candidate agents both attempt
(vendored from Lab 12, originally Lab 8's `tasks.py`, unchanged).

Four tasks never hit a tool failure — `baseline_agent`, `candidate_good`,
and `candidate_bad` behave identically on those, byte for byte. Six tasks
(`*-err-*`) plant one: the first scripted tool call uses a slightly wrong
key and raises. What happens next depends on whether the model can SEE
that failure in the transcript — exactly the thing `baseline_agent` and
`candidate_bad` disagree about (Lab 3's error-surfacing contract; Trace 10).

`_reactive()` builds a `(check, response)` entry for `ScriptedModel`: the
`check` callable runs first and rewrites the shared `response` in place
before `ScriptedModel.complete()` returns it (see
`worksheet_common.scripted_model` — `check` may assert on the transcript,
or, as here, use it to pick a branch). An agent that surfaced
"error: ..." gets the `on_error` branch: retry with the corrected key. An
agent that swallowed the error as "" gets `on_silence`: a confident, wrong
final answer, no retry. `required_tools` for those tasks lists the retry
tool call too — an agent that surfaces the error makes it, `candidate_bad`
never does.
"""
from __future__ import annotations

from worksheet_common import ModelResponse, ToolCall


def _reactive(on_error: ModelResponse, on_silence: ModelResponse):
    """A ScriptedModel entry whose response depends on the prior tool result."""
    response = ModelResponse()

    def check(messages: list[dict]) -> None:
        last_content = messages[-1]["content"]
        source = on_error if last_content.startswith("error") else on_silence
        response.text = source.text
        response.tool_calls = source.tool_calls

    return (check, response)


TASKS = [
    # -- 4 clean tasks: no tool ever fails; all three agents behave identically.
    {
        "id": "calc-1",
        "question": "What is 15 * 3?",
        "script": [
            ModelResponse(tool_calls=[ToolCall("t1", "calculator", {"expr": "15 * 3"})]),
            ModelResponse(text="The answer is 45."),
        ],
        "expected_answer": "The answer is 45.",
        "required_tools": ["calculator"],
    },
    {
        "id": "wordcount-1",
        "question": "The note says 'agents need tests and evals'. How many words, times 10?",
        "script": [
            ModelResponse(tool_calls=[ToolCall("t1", "word_count",
                                                {"text": "agents need tests and evals"})]),
            ModelResponse(tool_calls=[ToolCall("t2", "calculator", {"expr": "5 * 10"})]),
            ModelResponse(text="There are 5 words, times 10 is 50."),
        ],
        "expected_answer": "There are 5 words, times 10 is 50.",
        "required_tools": ["word_count", "calculator"],
    },
    {
        "id": "price-clean-1",
        "question": "How much is a widget?",
        "script": [
            ModelResponse(tool_calls=[ToolCall("t1", "lookup_price", {"item": "widget"})]),
            ModelResponse(text="A widget costs $9.99."),
        ],
        "expected_answer": "A widget costs $9.99.",
        "required_tools": ["lookup_price"],
    },
    {
        "id": "weather-docs-1",
        "question": "What's the weather in Tokyo, and what are the support hours?",
        "script": [
            ModelResponse(tool_calls=[ToolCall("t1", "get_weather", {"city": "Tokyo"})]),
            ModelResponse(tool_calls=[ToolCall("t2", "search_docs", {"query": "hours"})]),
            ModelResponse(text="Tokyo is Rainy, 18C. Support hours are 9am-5pm ET."),
        ],
        "expected_answer": "Tokyo is Rainy, 18C. Support hours are 9am-5pm ET.",
        "required_tools": ["get_weather", "search_docs"],
    },

    # -- 6 error tasks: the first tool call uses a wrong key and raises.
    {
        "id": "price-err-1",
        "question": "How much does the gadget cost?",
        "script": [
            ModelResponse(tool_calls=[ToolCall("t1", "lookup_price", {"item": "gadgets"})]),
            _reactive(
                on_error=ModelResponse(
                    tool_calls=[ToolCall("t2", "lookup_price", {"item": "gadget"})]),
                on_silence=ModelResponse(text="A gadget costs $0.00."),
            ),
            ModelResponse(text="A gadget costs $14.99."),
        ],
        "expected_answer": "A gadget costs $14.99.",
        "required_tools": ["lookup_price", "lookup_price"],
    },
    {
        "id": "price-err-2",
        "question": "What's the price of the sensor?",
        "script": [
            ModelResponse(tool_calls=[ToolCall("t1", "lookup_price", {"item": "sensors"})]),
            _reactive(
                on_error=ModelResponse(
                    tool_calls=[ToolCall("t2", "lookup_price", {"item": "sensor"})]),
                on_silence=ModelResponse(text="The sensor costs $19.99."),
            ),
            ModelResponse(text="The sensor costs $29.99."),
        ],
        "expected_answer": "The sensor costs $29.99.",
        "required_tools": ["lookup_price", "lookup_price"],
    },
    {
        "id": "weather-err-1",
        "question": "What's the weather like in Cairo?",
        "script": [
            ModelResponse(tool_calls=[ToolCall("t1", "get_weather", {"city": "Cairoo"})]),
            _reactive(
                on_error=ModelResponse(
                    tool_calls=[ToolCall("t2", "get_weather", {"city": "Cairo"})]),
                on_silence=ModelResponse(text="Cairo is unknown; assuming Sunny, 20C."),
            ),
            ModelResponse(text="Cairo is Clear, 34C."),
        ],
        "expected_answer": "Cairo is Clear, 34C.",
        "required_tools": ["get_weather", "get_weather"],
    },
    {
        "id": "weather-err-2",
        "question": "What's the weather in Oslo?",
        "script": [
            ModelResponse(tool_calls=[ToolCall("t1", "get_weather", {"city": "Osloo"})]),
            _reactive(
                on_error=ModelResponse(
                    tool_calls=[ToolCall("t2", "get_weather", {"city": "Oslo"})]),
                on_silence=ModelResponse(text="Oslo is Sunny, 25C."),
            ),
            ModelResponse(text="Oslo is Cloudy, 9C."),
        ],
        "expected_answer": "Oslo is Cloudy, 9C.",
        "required_tools": ["get_weather", "get_weather"],
    },
    {
        "id": "docs-err-1",
        "question": "What is the refund policy?",
        "script": [
            ModelResponse(tool_calls=[ToolCall("t1", "search_docs", {"query": "refund policies"})]),
            _reactive(
                on_error=ModelResponse(
                    tool_calls=[ToolCall("t2", "search_docs", {"query": "refund policy"})]),
                on_silence=ModelResponse(text="There is no refund policy on file."),
            ),
            ModelResponse(text="Refunds within 30 days with receipt."),
        ],
        "expected_answer": "Refunds within 30 days with receipt.",
        "required_tools": ["search_docs", "search_docs"],
    },
    {
        "id": "docs-err-2",
        "question": "What is the warranty period?",
        "script": [
            ModelResponse(tool_calls=[ToolCall("t1", "search_docs", {"query": "warranty period"})]),
            _reactive(
                on_error=ModelResponse(
                    tool_calls=[ToolCall("t2", "search_docs", {"query": "warranty"})]),
                on_silence=ModelResponse(text="There is no warranty information available."),
            ),
            ModelResponse(text="The warranty is 1 year limited warranty."),
        ],
        "expected_answer": "The warranty is 1 year limited warranty.",
        "required_tools": ["search_docs", "search_docs"],
    },
]
