"""Mini permission-rule engine (PROVIDED — read it, do not edit it).

Mirrors the real semantics recorded in notes/research-notes.md under
"Harness facts (Claude Code)" and walked in Trace 18 (Chapter 7):

- Rules name a tool, or a tool with a specifier: `Tool` or `Tool(specifier)`.
- Rules live in three lists: `deny`, `ask`, `allow`.
- Evaluation order is deny -> ask -> allow. First match wins.
  Specificity is irrelevant: a broad deny beats a precise allow.
- A bare `Tool` rule (no parentheses) matches every use of that tool.
- A specifier ending in `*` is a prefix match; anything else is an exact match.

Your task in this lab is `starter/policy/settings.json` and
`starter/policy/CLAUDE.md`, not this file.
"""
from __future__ import annotations

# Which key of a tool_call's "input" dict the rule specifier matches against.
_INPUT_KEY = {
    "Bash": "command",
    "Read": "path",
    "Write": "path",
    "Edit": "path",
}


def call_signature(tool_call: dict) -> tuple[str, str]:
    """Map a transcript tool_call dict to (tool_name, input_str).

    `tool_call` looks like {"id": "t1", "name": "Bash", "input": {"command": "..."}}
    (the same shape `run_agent()` writes into a transcript in Lab 3).
    """
    name = tool_call["name"]
    key = _INPUT_KEY.get(name)
    input_dict = tool_call.get("input", {}) or {}
    input_str = input_dict.get(key, "") if key else str(input_dict)
    return name, input_str


def _parse_rule(rule: str) -> tuple[str, str | None]:
    """Split 'Bash(rm *)' into ('Bash', 'rm *'); bare 'Bash' into ('Bash', None)."""
    if "(" in rule and rule.endswith(")"):
        name, _, rest = rule.partition("(")
        return name, rest[:-1]
    return rule, None


def _rule_matches(rule: str, tool_name: str, input_str: str) -> bool:
    name, specifier = _parse_rule(rule)
    if name != tool_name:
        return False
    if specifier is None:
        return True  # bare Tool matches every use of the tool
    if specifier.endswith("*"):
        return input_str.startswith(specifier[:-1])
    return input_str == specifier


def evaluate(rules: dict, tool_name: str, input_str: str) -> str | None:
    """Evaluate deny -> ask -> allow against `rules` (a permissions dict).

    `rules` has the shape {"deny": [...], "ask": [...], "allow": [...]},
    same as `settings.json`'s "permissions" object.

    Returns "deny", "ask", or "allow" for the first list with a matching
    rule, or None if nothing matched (the mode default would decide next —
    out of scope for this lab).
    """
    for level in ("deny", "ask", "allow"):
        for rule in rules.get(level, []):
            if _rule_matches(rule, tool_name, input_str):
                return level
    return None
