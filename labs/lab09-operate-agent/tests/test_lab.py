"""Lab 9 checker: 7 tests define "done".

They load the three recorded transcripts and run every tool call in them
through `policy/engine.py` against your `policy/settings.json`. The engine
is provided and identical in starter/ and solution/ — your task is the
settings.json rules and the CLAUDE.md guidance, evaluated here.

Tests run against starter/ by default (your task list) and against
solution/ with LAB_TARGET=solution (the reference passing).
"""


def _find_call(transcript, name, **field):
    """Locate the tool_call in `transcript` with this name and input field."""
    (key, value), = field.items()
    for m in transcript:
        if m.get("role") != "assistant":
            continue
        for call in m.get("tool_calls", []):
            if call["name"] == name and call["input"].get(key) == value:
                return call
    raise AssertionError(f"expected {name} call with {key}={value!r} not found in transcript")


# ---------------------------------------------------------------------------
# Session 1: rm -rf on a directory, then a force-push over shared history.
# ---------------------------------------------------------------------------

def test_session1_destructive_calls_are_denied_or_asked(engine, permissions, session1):
    rm_call = _find_call(session1, "Bash", command="rm -rf build/")
    push_call = _find_call(session1, "Bash", command="git push --force origin main")
    assert engine.evaluate(permissions, *engine.call_signature(rm_call)) in ("deny", "ask")
    assert engine.evaluate(permissions, *engine.call_signature(push_call)) in ("deny", "ask")


# ---------------------------------------------------------------------------
# Session 2: reads .env, then pastes the secret into a source file.
# ---------------------------------------------------------------------------

def test_session2_secret_read_is_denied_or_asked(engine, permissions, session2):
    env_call = _find_call(session2, "Read", path=".env")
    assert engine.evaluate(permissions, *engine.call_signature(env_call)) in ("deny", "ask")


# ---------------------------------------------------------------------------
# Session 3: global package install, then an edit outside the repo.
# ---------------------------------------------------------------------------

def test_session3_destructive_calls_are_denied_or_asked(engine, permissions, session3):
    install_call = _find_call(session3, "Bash", command="npm install -g eslint")
    hosts_call = _find_call(session3, "Edit", path="/etc/hosts")
    assert engine.evaluate(permissions, *engine.call_signature(install_call)) in ("deny", "ask")
    assert engine.evaluate(permissions, *engine.call_signature(hosts_call)) in ("deny", "ask")


# ---------------------------------------------------------------------------
# The routine, legitimate calls in every session must keep working.
# ---------------------------------------------------------------------------

def test_legitimate_calls_remain_allowed(engine, permissions, session1):
    legitimate = [
        _find_call(session1, "Bash", command="git status"),
        _find_call(session1, "Bash", command="pytest -q"),
        _find_call(session1, "Read", path="src/main.py"),
        _find_call(session1, "Edit", path="src/main.py"),
    ]
    for call in legitimate:
        result = engine.evaluate(permissions, *engine.call_signature(call))
        assert result in ("allow", None), (
            f"legitimate call {call['name']}({call['input']}) was blocked "
            f"by a rule that is too broad: got {result!r}"
        )


# ---------------------------------------------------------------------------
# The rules must be scoped, not blanket bans on a whole tool.
# ---------------------------------------------------------------------------

def test_deny_list_has_no_blanket_bans(permissions):
    deny = permissions.get("deny", [])
    assert "Bash" not in deny, "a bare `Bash` deny blocks pytest and git status too — scope it"
    assert "Read" not in deny, "a bare `Read` deny blocks reading source files too — scope it"


# ---------------------------------------------------------------------------
# The .env rule must target .env specifically, not swallow ordinary reads.
# ---------------------------------------------------------------------------

def test_env_deny_is_specific_to_env_path(engine, permissions, session2):
    env_call = _find_call(session2, "Read", path=".env")
    src_call = _find_call(session2, "Read", path="src/main.py")
    assert engine.evaluate(permissions, *engine.call_signature(env_call)) in ("deny", "ask")
    assert engine.evaluate(permissions, *engine.call_signature(src_call)) in ("allow", None)


# ---------------------------------------------------------------------------
# CLAUDE.md must actually say something, not just carry TODO comments.
# ---------------------------------------------------------------------------

def test_claude_md_has_required_guidance(claude_md_text):
    assert claude_md_text.strip(), "CLAUDE.md is empty"
    headers = [ln for ln in claude_md_text.splitlines() if ln.strip().startswith("#")]
    assert len(headers) >= 3, "CLAUDE.md needs at least 3 markdown sections"
    lower = claude_md_text.lower()
    assert "force" in lower, "CLAUDE.md must state the force-push policy"
    assert "secret" in lower or ".env" in lower, "CLAUDE.md must state secrets handling"
    assert "install" in lower, "CLAUDE.md must state the dependency-install policy"
