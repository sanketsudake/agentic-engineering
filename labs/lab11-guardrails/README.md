# Lab 11 — Guardrails and tool-permission design

**Goal:** stop 5 adversarial sessions — each one an injected instruction
inside tool output, followed by a dangerous call — by writing a layered
policy: permission rules, an egress allowlist, and output-pattern scans.
A provided rule engine proves whether each attack actually dies.

**Level:** L3 · **Stack:** plain Python · **Time:** ~60 min · offline, no
model

**Offline mode (default, no keys, no model at all):**

```bash
uv sync
uv run pytest                      # 7 red tests are your task list
```

**Reference check:**

```bash
LAB_TARGET=solution uv run pytest  # the reference policy passing
```

This lab needs no model. Whether a policy stops an attack is a fact about
the policy, not about anything a model generates — so it is testable
offline, deterministically, every time.

## Your task

1. Read each session in `attacks/`: five adversarial transcripts, each one
   a tool result carrying an injected instruction, followed by the
   assistant attempting a dangerous call. Read `legit/` too: three
   sessions of real work the policy must not break.
2. Open `starter/guard/engine.py` and read it. It is provided and
   working — your task is not to write the engine, it is to write a
   policy for it. Three functions matter:
   - `evaluate()` — the permission layer: deny -> ask -> allow, first
     match wins (same semantics as Lab 9, Trace 18).
   - `check_egress(command, allowlist)` — the network layer: extracts the
     hostname(s) a Bash command would contact and checks them against an
     allowlist.
   - `scan_output(text, patterns)` — the output layer: scans text for
     secret-shaped regexes and returns what matched.
3. Edit `starter/guard/policy.json`:
   `{"permissions": {"deny": [...], "ask": [...]}, "egress_allowlist": [...], "output_patterns": [...]}`.
   Write the narrowest rules that stop each attack, in the syntax `Tool`
   or `Tool(specifier)` (a trailing `*` is a prefix match). Keep every
   legit call in `legit/` working — a rule that blocks those fails the
   lab, even if it also stops an attack.

**Done means:** `uv run pytest` is fully green against `starter/`.

## What this proves

Trace 29 (Chapter 11) walks a prompt injection arriving inside tool
output; Trace 30 walks an agent trying to exfiltrate data. This lab puts
you on the defending side of both: three independent layers, so that
removing any one leg of the trifecta is what it takes to make an attack
succeed, not a single missed rule.

Attack 1 (the ssh-key curl) is built to require two layers at once: the
permission rule asks before any `curl` runs, and even if that rule were
missing or misconfigured, the egress allowlist still refuses a host
nobody approved. Prompt injection defeats "ask the model nicely not to"
every time, because the instruction arrives after the model's own
instructions, inside data it was told to trust. A layered policy does not
care where the instruction came from — it evaluates the call itself,
every time, the same way.

The failure mode to avoid is the blanket ban: denying all of `Bash` or
all of `Read` stops every attack and every legitimate use in the same
stroke. A policy an operator cannot ship is not a policy — it is a
different way of not doing the work.
