"""Lab 6 checker: 5 tests define "done".

They run against starter/ by default (your task list) and against solution/
with LAB_TARGET=solution (the reference passing). Everything here is
offline — worksheet_common.mockllm stands in for the model API, reached
through the OpenAI Agents SDK's own client plumbing, on localhost only.
"""
from agents import Handoff

from wire import mock_provider, openai_text_response, openai_tool_call_response


def test_refund_question_gets_the_refunds_answer(handoff):
    """The model chooses the refund handoff tool; the refunds agent answers."""
    _triage, refunds, _tech = handoff.build_agents()
    transfer_tool = Handoff.default_tool_name(refunds)
    turns = [
        openai_tool_call_response(transfer_tool, {}),
        openai_text_response("Refunds land back in 3-5 business days."),
    ]
    with mock_provider(turns):
        result = handoff.run_triage("I want a refund for my last order")
    assert result.final_output == "Refunds land back in 3-5 business days."


def test_handoff_transfers_ownership_to_refunds(handoff):
    """The SECOND request carries the refunds agent's own instructions —
    proof the conversation's owner actually changed, not just its reply."""
    _triage, refunds, _tech = handoff.build_agents()
    transfer_tool = Handoff.default_tool_name(refunds)
    turns = [
        openai_tool_call_response(transfer_tool, {}),
        openai_text_response("Refunds land back in 3-5 business days."),
    ]
    with mock_provider(turns) as mock:
        result = handoff.run_triage("I want a refund for my last order")
    assert result.last_agent.name == refunds.name
    second_request_system = mock.requests[1]["body"]["messages"][0]
    assert second_request_system == {"role": "system", "content": refunds.instructions}


def test_tech_question_routes_to_tech_support(handoff):
    """Same mechanism, the other specialist: routing isn't refunds-specific."""
    _triage, _refunds, tech = handoff.build_agents()
    transfer_tool = Handoff.default_tool_name(tech)
    turns = [
        openai_tool_call_response(transfer_tool, {}),
        openai_text_response("Try force-quitting and reopening the app."),
    ]
    with mock_provider(turns) as mock:
        result = handoff.run_triage("The app crashes every time I open it")
    assert result.final_output == "Try force-quitting and reopening the app."
    assert result.last_agent.name == tech.name
    assert mock.requests[1]["body"]["messages"][0] == {
        "role": "system",
        "content": tech.instructions,
    }


def test_question_triage_can_answer_directly_has_no_handoff(handoff):
    """No specialist needed -> one request, triage stays the owner."""
    turns = [openai_text_response("2 + 2 is 4.")]
    with mock_provider(turns) as mock:
        result = handoff.run_triage("what is 2 + 2?")
    assert len(mock.requests) == 1
    assert result.last_agent.name == "Triage"
    assert result.final_output == "2 + 2 is 4."


def test_first_request_declares_both_transfer_tools(handoff):
    """Handoffs are declared to the model as tools before it ever chooses one."""
    _triage, refunds, tech = handoff.build_agents()
    turns = [openai_text_response("no handoff needed for this one")]
    with mock_provider(turns) as mock:
        handoff.run_triage("just checking something trivial")
    declared = {t["function"]["name"] for t in mock.requests[0]["body"]["tools"]}
    assert declared == {
        Handoff.default_tool_name(refunds),
        Handoff.default_tool_name(tech),
    }
