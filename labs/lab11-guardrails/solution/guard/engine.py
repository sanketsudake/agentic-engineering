"""Mini permission-rule engine (PROVIDED — read it, do not edit it).

Copied from Lab 9's `policy/engine.py` and extended for guardrail design:
`scan_output()` and `check_egress()` are new, both provided and working.
Identical in starter/ and solution/ — your task in this lab is
`policy.json`, not this file.

- `evaluate()` mirrors the real semantics recorded in
  notes/research-notes.md under "Harness facts (Claude Code)" and walked
  in Trace 18 (Chapter 7): rules name a tool, or a tool with a specifier
  (`Tool` or `Tool(specifier)`); evaluation order is deny -> ask -> allow,
  first match wins, specificity is irrelevant.
- `check_egress()` is the second layer: even a call the permission rules
  allow can still try to talk to a host that was never approved.
- `scan_output()` is the third layer: even a call that passes both gates
  can still be about to leak something that looks like a secret.

Trace 29 and Trace 30 (Chapter 11) are about exactly this: an instruction
arriving inside tool output, and an agent trying to get data out. No
single layer here is sufficient by itself — that is the lab.
"""
from __future__ import annotations

import re

# Which key of a tool_call's "input" dict the rule specifier matches against.
_INPUT_KEY = {
    "Bash": "command",
    "Read": "path",
    "Write": "path",
    "Edit": "path",
    "send_email": "attachment",
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

    `rules` has the shape {"deny": [...], "ask": [...], "allow": [...]}
    (the "allow" list is optional; Lab 11's policy.json omits it).

    Returns "deny", "ask", or "allow" for the first list with a matching
    rule, or None if nothing matched (the mode default would decide next —
    out of scope for this lab; treat None the same as "allow").
    """
    for level in ("deny", "ask", "allow"):
        for rule in rules.get(level, []):
            if _rule_matches(rule, tool_name, input_str):
                return level
    return None


# ---------------------------------------------------------------------------
# check_egress: the second layer. A Bash call the permission rules allow
# can still reach out to a host nobody approved.
# ---------------------------------------------------------------------------

_HOST_URL_RE = re.compile(r'https?://([^/\s?"\']+)')


def _extract_hosts(command: str) -> list[str]:
    """Pull the hostnames a shell command would contact.

    Handles explicit http(s) URLs (curl, wget) and infers the implicit
    GitHub hosts a `gh` subcommand talks to. Commands with no network
    call (most Bash calls) yield an empty list.
    """
    hosts = [m.group(1).split(":")[0] for m in _HOST_URL_RE.finditer(command)]
    if re.search(r"(?:^|\s)gh\s+gist\s+create\b", command):
        hosts.append("gist.github.com")
    elif re.search(r"(?:^|\s)gh\s+", command):
        hosts.append("github.com")
    return hosts


def check_egress(command: str, allowlist: list[str]) -> bool:
    """Return True if every host `command` would contact is on `allowlist`.

    A command that touches no network host always passes (returns True).
    A command that reaches even one host outside the allowlist fails.
    """
    hosts = _extract_hosts(command)
    return all(host in allowlist for host in hosts)


# ---------------------------------------------------------------------------
# scan_output: the third layer. Even an allowed, egress-clean call can
# still be about to move a secret-shaped string out of the session.
# ---------------------------------------------------------------------------

def scan_output(text: str, patterns: list[str]) -> list[str]:
    """Scan `text` for exfiltration-shaped patterns.

    `patterns` is a list of regexes (policy.json's "output_patterns"),
    each meant to match something secret-shaped: an API key, a private
    key header, a credential assignment. Returns the subset of `patterns`
    that matched somewhere in `text`, in the order given. An empty list
    means nothing matched.
    """
    return [pattern for pattern in patterns if re.search(pattern, text)]
