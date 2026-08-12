"""Ground truth for the 20 fixtures in ../transcripts/. Tests only —
the reader's classifier never imports this file.
"""

LABELS = {
    "prod001": "SUCCESS",
    "prod002": "SUCCESS",
    "prod003": "SUCCESS",
    "prod004": "SUCCESS",
    "prod005": "SUCCESS",
    "prod006": "SUCCESS",
    "prod007": "RUNAWAY_LOOP",
    "prod008": "RUNAWAY_LOOP",
    "prod009": "RUNAWAY_LOOP",
    "prod010": "RUNAWAY_LOOP",
    "prod011": "SWALLOWED_ERROR",
    "prod012": "SWALLOWED_ERROR",
    "prod013": "SWALLOWED_ERROR",
    "prod014": "CONTEXT_LOSS",
    "prod015": "CONTEXT_LOSS",
    "prod016": "CONTEXT_LOSS",
    "prod017": "BAD_HANDOFF",
    "prod018": "BAD_HANDOFF",
    "prod019": "TRUNCATION",
    "prod020": "TRUNCATION",
}

# One representative fixture per class, for the per-class spot-check test.
REPRESENTATIVE = {
    "SUCCESS": "prod001",
    "RUNAWAY_LOOP": "prod007",
    "SWALLOWED_ERROR": "prod011",
    "CONTEXT_LOSS": "prod014",
    "BAD_HANDOFF": "prod017",
    "TRUNCATION": "prod019",
}
