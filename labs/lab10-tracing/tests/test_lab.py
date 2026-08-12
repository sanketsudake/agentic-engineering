"""Lab 10 checker: ~6 tests define "done".

They run against starter/ by default (your task list) and against
solution/ with LAB_TARGET=solution (the reference passing).

Prices are Sonnet-class from notes/research-notes.md's pricing snapshot:
$3.00 / 1M input tokens, $15.00 / 1M output tokens.
"""
import pytest

from labels import LABELS, REPRESENTATIVE

PRICE_IN = 3.00 / 1_000_000
PRICE_OUT = 15.00 / 1_000_000


# ---------------------------------------------------------------------------
# One representative fixture per class: classify() must name it correctly.
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("expected_class,session_id", sorted(REPRESENTATIVE.items()))
def test_classify_matches_label_per_class(classify_mod, all_transcripts, expected_class, session_id):
    result = classify_mod.classify(all_transcripts[session_id])
    assert result == expected_class, (
        f"{session_id} is ground-truth {expected_class!r}, classifier said {result!r}"
    )


# ---------------------------------------------------------------------------
# Overall accuracy across all 20: the taxonomy has to work at scale, not
# just on the six easy examples above.
# ---------------------------------------------------------------------------

def test_overall_accuracy_at_least_90_percent(classify_mod, all_transcripts):
    correct = sum(
        1 for sid, transcript in all_transcripts.items()
        if classify_mod.classify(transcript) == LABELS[sid]
    )
    accuracy = correct / len(LABELS)
    assert accuracy >= 0.9, f"accuracy {accuracy:.2f} ({correct}/{len(LABELS)}) is below the 0.9 bar"


# ---------------------------------------------------------------------------
# The classifier is a set of detectors, not a model with an unknown output
# space — it must never raise, even under a mix it wasn't tuned for.
# ---------------------------------------------------------------------------

def test_classifier_never_raises_on_any_fixture(classify_mod, all_transcripts):
    for sid, transcript in all_transcripts.items():
        result = classify_mod.classify(transcript)
        assert result in classify_mod.CLASSES, f"{sid}: classify() returned unknown class {result!r}"


# ---------------------------------------------------------------------------
# session_cost: exact on a known fixture (prod001 — SUCCESS, 4 assistant
# turns, usage 2200 input / 440 output tokens total).
# ---------------------------------------------------------------------------

def test_session_cost_exact_on_known_fixture(costs_mod, all_transcripts):
    cost = costs_mod.session_cost(all_transcripts["prod001"], PRICE_IN, PRICE_OUT)
    assert cost == pytest.approx(0.0132)


# ---------------------------------------------------------------------------
# cost_per_solve: total spend across ALL 20 sessions / 6 SUCCESS sessions.
# Hand-computed constant: 39,800 input + 7,960 output tokens across every
# fixture, at Sonnet-class prices, divided by 6.
# ---------------------------------------------------------------------------

def test_cost_per_solve_matches_hand_computed_constant(costs_mod, all_transcripts):
    result = costs_mod.cost_per_solve(all_transcripts, LABELS, PRICE_IN, PRICE_OUT)
    assert result == pytest.approx(0.0398)


# ---------------------------------------------------------------------------
# cost_per_solve must accept a classifier callable too, not just the
# ground-truth dict — and get the same answer once the classifier is good.
# ---------------------------------------------------------------------------

def test_cost_per_solve_agrees_with_classifier(costs_mod, classify_mod, all_transcripts):
    by_labels = costs_mod.cost_per_solve(all_transcripts, LABELS, PRICE_IN, PRICE_OUT)
    by_classifier = costs_mod.cost_per_solve(all_transcripts, classify_mod.classify, PRICE_IN, PRICE_OUT)
    assert by_classifier == pytest.approx(by_labels)
