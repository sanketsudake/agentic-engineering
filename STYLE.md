# STYLE.md — rules every chapter, lab, and exam must follow

**What this document is:** the contract for writing the "Agentic Engineering Worksheet".
Follow it exactly so all chapters read as one book,
all labs check the same way,
and all exams grade the same way.

## Audience and voice

- Reader: an engineer at any level, junior through principal, building or operating AI agents.
- Simple technical English. Short sentences (aim ≤ 20 words). One idea per paragraph. Paragraphs ≤ 4 sentences.
- Define every piece of jargon at first use, in one clause: "the harness (the runtime that owns the loop, context assembly, and gating)".
- High signal, low noise: no filler ("It is important to note that…"), no marketing tone, no repetition of what another section already said — cross-reference instead ("see Trace 2").
- Present tense. Active voice. "The harness appends the tool result" not "The tool result is appended".
- Never invent facts. Version-sensitive claims (model names, API features, SDK behavior, prices) MUST match `notes/research-notes.md`. Baseline is August 2026.

## Levels

The book uses one level scheme everywhere:

| Tag | Name | Claim |
|---|---|---|
| L1 | Builder | Can explain the mechanism and build a working agent. |
| L2 | Operator | Can debug, eval, and productionize an agent. |
| L3 | Architect | Can judge: commit to positions, design org-scale systems. |

Rules:

- Tag syntax `[L1]`, `[L2]`, `[L3]` is allowed in exactly three places: the level line at the end of "Why this chapter", lab callouts, and exam section headings.
- Question tiers carry the levels; individual questions are never tagged. The mapping (Tier 1 → L1, Tier 2–3 → L2, Tier 4 → L3) is stated once, in Appendix C.
- An architect-only section gets a heading suffix: `### Context isolation across subagents (L3)`. That is the whole inline-tag surface — no per-paragraph badges.

## File format

- One markdown file per chapter: `chapters/chNN.md` (`ch01.md` … `ch14.md`, `appendices.md`).
- Start with `# Chapter N — Title`. Use `##` for sections, `###` for traces and questions. No deeper nesting.
- No HTML in the markdown. Tables in GitHub style. Code in fenced blocks with language tag (`python`, `json`, `bash`).
- Exam files (`exams/l*/exam.md`) MUST start with `# Title` on line 1, with no frontmatter — the build crashes otherwise.

## Chapter shape (Chapters 1–12, in this order)

1. **Opening ("Why this chapter")** — 3–6 sentences: what a strong engineer must hold in their head, and the one mental model. End with a level line: `Level emphasis: L1–L2; the (L3) sections are optional on first read.`
2. **Concepts** — the minimum background needed to follow the traces. Keep short; teach details inside the traces. Ends with the mandatory `### In other stacks` box (below).
3. **Traces** — the heart of the chapter (format below).
4. **Questions** — tiered Q&A (format below).
5. **Common mistakes & red flags** — 4–8 bullets: wrong things engineers often say or build, each with the correction.

Lab callouts (format below) sit inside sections, immediately after the material the lab exercises.

## Trace format (strict)

Each trace is a `###` section titled: `### Trace N: What happens when <event>` (N = the global trace number from `TRACES.md`).

Contents, in order:

1. One-sentence setup ("You ask the agent to fix a failing test.").
2. **Numbered steps.** Each step starts with the acting component in bold: `1. **Harness** assembles the system prompt …`. One actor-action per step. 6–15 steps. If a step hides depth that matters, add an indented sub-bullet, max one per step.
3. **A mermaid diagram** in a fenced ` ```mermaid ` block, immediately after the steps, followed by an italic caption line: `*Figure N.M — one line saying what to notice.*` (N = chapter, M = running count within chapter).
4. **Where this can fail** — 3–6 bullets: `- **Symptom:** … **Cause:** … **Where to look:** …`. "Where to look" means: the transcript, the tool results, the trace spans, the token counts.

The master trace is Trace 2 (user request → finished task, Chapter 1).
Chapters 2–12 zoom into their segment of it and say so in the opening ("This chapter zooms into steps 4–6 of Trace 2").
Part E chapters operate above it, at org scale.

## Mermaid rules (build breaks if you're clever)

- Allowed types only: `sequenceDiagram`, `flowchart TD` (preferred) / `flowchart LR`, `stateDiagram-v2`.
- Sequence diagrams for under-the-hood traces; flowcharts for decisions; state diagrams for lifecycles.
- Participant names short and consistent across ALL chapters: `User` (the human or calling app), `Harness` (the agent runtime), `LLM` (the provider model API), `Tools` (the local tool executor), `MCP` (an MCP server), `Mem` (the memory store), `Idx` (the retrieval index), `Env` (filesystem, shell, browser, external API), `Sub` (a subagent, drawn as one lane), `Guard` (a guardrail or approval gate), `Judge` (a grader), `Obs` (the telemetry sink), `CI` (the CI system).
- Keep it simple: no `%%{init}%%` directives, no `par`/`critical` blocks; `alt`/`opt`/`Note` are fine. Label every arrow with a short verb phrase.
- In node/edge labels avoid characters that break mermaid: `(){}[]<>"`; use plain words. No HTML anywhere in a diagram body.
- `sequenceDiagram`: start with `autonumber`. Message text ≤ 6 words. Prefer few participants, but do not drop a real actor to save width — the tuned layout config carries eight lanes within the gate.

### The size gate (this is a hard limit, not a preference)

The page gives a diagram **174 mm** of width and **150 mm** of height, and the image is scaled by
`min(174/W, 150/H)`. So a diagram that is too **tall** shrinks exactly like one that is too **wide**.
Mermaid's label font is ~16 px; below about 7 pt it is unreadable in print.

**Every diagram must print its labels at 7 pt or larger.** That is the gate `check_diagrams.py`
enforces, and it reports the figure. As a rough guide it means staying under ~1,100 px wide or
~960 px tall, whichever binds first — but the point size is the rule.

Check before you commit:

```bash
python3 build/check_diagrams.py chapters/ch01.md      # or chapters/*.md
```

Staying inside the gate:

- ≤ 12 nodes per diagram, ≤ 3 nodes per rank, ≤ 4 words per node or edge label.
- **Never drop a participant, node or edge to make a diagram fit.** Shorten the label text instead.
  A diagram that omits a real step is a worse defect than one that is hard to read.
- Prefer `flowchart TD`. Use `LR` only for genuinely short chains.
- Avoid subgraphs that carry edges to nodes outside themselves — the layout goes wide regardless.
- If a diagram cannot fit, it is usually making two points. Get the split reviewed —
  splitting adds a figure and **renumbers every later figure in the chapter**.

### Colour: class nodes by semantic role

Flowcharts and state diagrams carry a small semantic palette, so role reads at a glance.
`classDef` is **not supported in `sequenceDiagram`** — those use `autonumber` and stay uncoloured.

| Class | Use for | Fill | Stroke |
|---|---|---|---|
| `leader` | the component driving the loop (orchestrator, active agent) | `#10b981` | `#047857` |
| `standby` | idle worker, queued run, paused session | `#94a3b8` | `#475569` |
| `lease` | gate, queue, lock, approval, eval gate | `#f59e0b` | `#b45309` |
| `resource` | the artifact acted on: context window, file, PR, dataset | `#fb7185` | `#be123c` |
| `external` | provider API, third-party service | `#64748b` | `#334155` |
| `process` | logic, decision, generic step | `#38bdf8` | `#0369a1` |

All fills use `color:#fff`. Rules:

- Declare only the classes the diagram uses.
- Once you class one node, class **every** node — a half-coloured diagram looks broken.
- Put `classDef` and `class` lines at the bottom of the diagram body. Inside a subgraph, after the `end`.

### Caption coupling (silent failure if you get this wrong)

`build/build.py` matches a diagram with the regex ` ```mermaid … ``` ` followed by **only whitespace**
and then the `*Figure N.M — caption*` line. Put anything else between them and the match fails: the build
still exits 0 and raw mermaid source lands in the PDF. Keep the caption immediately after the closing
fence, on its own line, as plain italic text with no internal `**bold**`.

## Question format (strict)

Section `## Questions`. Chapters 1–12: three subsections `### Tier 1 — Explain`, `### Tier 2 — Reason`, `### Tier 3 — Design & Debug`. Part E chapters (13–14): `### Tier 2 — Reason`, `### Tier 3 — Design & Debug`, `### Tier 4 — Judge` — no Tier 1; mechanism recall belongs to Chapters 1–12.

Each question:

```
**Q N.M — Question text?**

**Answer.** 5–15 lines. Direct answer first, then mechanism.

*Strong answers also mention:* one or two things that distinguish a great engineer.
```

Number questions `N.M` per chapter (chapter.number, continuous across tiers). Chapters 1–12: 3–4 Tier 1, 3–4 Tier 2, 2–3 Tier 3. Part E: 3–4 Tier 2, 2–3 Tier 3, 2–3 Tier 4. Tier 3 questions are scenarios: a symptom to debug or a system to design — the answer walks the reasoning, not just the conclusion. Tier 4 questions demand a committed position: the answer names assumptions and kill-criteria, argues the strongest counter-position, then decides (the Appendix C Tier-4 row is the rubric).

## Answer markers (closed registry)

The candidate edition strips model answers programmatically.
These are the only answer-shaped markers, and each strips to its stated boundary:

| Marker | Strips |
|---|---|
| `**Answer.**` | from the marker to the next `**Q` line or heading |
| `*Strong answers also mention:*` | from the marker to the next `**Q` line or heading |
| `**What's wrong?**` | the prompt line stays; everything under it goes, to the next heading |
| `**Fix.**` | from the marker to the next heading |
| `**Critique.**` | from the marker to the next heading |
| `**What reviewers look for.**` | from the marker to the next heading |

Adding a new marker requires updating `strip_answers()` in `build/build.py`
and the strip-integrity rule in `build/check_book.py` in the same commit.

## Lab callout format (strict)

A lab is referenced from exactly one chapter, as a blockquote placed right after the section that teaches the mechanism:

```markdown
> **Lab 3 — Build the tool loop.** `labs/lab03-tool-loop/` · [L1] · ~45 min · offline.
> You implement `run_agent()` against a scripted model; 7 tests define done.
```

The opener must be exactly `**Lab N — title.**` — the build renders it as a callout box
and collects a Labs index; a malformed opener silently renders as a plain quote
(`check_book.py` catches it).

## Lab authoring contract

- Directory: `labs/labNN-slug/` with `README.md`, `pyproject.toml` + committed `uv.lock`, `starter/`, `solution/`, `tests/`.
- The same tests run against starter or solution: `LAB_TARGET=starter` (default) or `solution`, wired in `tests/conftest.py`.
- **Offline by default, zero API keys.** Model access always goes through injection (a `Model` protocol / `ScriptedModel`) or a `base_url` pointed at `worksheet_common.mockllm` — never a hardcoded provider client.
- Live tests are optional, marked `@pytest.mark.live`, and deselected by default (`addopts = "-m 'not live'"`).
- README states: goal, level tag, stack, time estimate, what "done" means, offline and live commands.
- Dependencies pinned via the lockfile. Shared helpers come from `labs/common` (`worksheet_common`) as an editable path dependency.
- Chapter code and lab code default to plain Python + the Anthropic SDK ("no-framework first"). A framework (OpenAI Agents SDK, LangGraph) appears only in the lab where it earns its keep.

## Exam format (strict)

- Files: `exams/l{1,2,3}/exam.md` (questions + blank score sheet; rendered into the PDF), `key.md` (grading key; repo-only), `practical/` (a lab-shaped uv project, pytest-scored, offline).
- `key.md` is never referenced from any file that renders into the PDF.
- `exam.md` header states: the claim the exam verifies, time budget, materials allowed, total points, and the pass bar.
- Question IDs: `**E<level>.<section><n> (<pts> pts) — text?**` (e.g. `**E2.A3 (10 pts) — …?**`). The key mirrors every ID with `**Award.**` criteria: "award 3 pts if the answer names the acting component; …".
- Practical sections are scored as N pytest checks × fixed points each; the score sheet totals them. No judgment needed to grade a practical.

## Multi-framework code rules

- Prose, traces, and diagrams are framework-neutral: participants are roles (`Harness`, `LLM`), never SDK class names.
- Inline chapter code: plain Python + Anthropic SDK, ≤ 2 snippets per chapter (Chapter 4's code-reading exercises exempt), ≤ 40 lines per snippet.
- Every Chapter 1–12 chapter ends its Concepts section with `### In other stacks`: 3–6 bullets naming behavior/naming deltas in the OpenAI Agents SDK and LangGraph. Nothing else framework-specific appears inline.
- Appendix E (Framework Rosetta) owns the cross-stack concept table. Frameworks pin versions in lab lockfiles; prose pins facts in `notes/research-notes.md`.

## Part E chapters (judgment format)

Chapters 13–14 target architect-level judgment and relax the Chapters 1–12 shape:

1. **Opening ("Why this chapter")** — same as Chapters 1–12.
2. **Concepts** — may carry most of the chapter.
3. **Traces** — optional. When present, the strict trace format and all mermaid rules apply unchanged.
4. **Scenario sections** — `### Scenario: <title>`: a presented architecture or plan in 3–6 sentences, then `**Critique.**` — an 8–15 line model answer naming what is wrong, what is right, and what to ask next.
5. **Capstone sections** — `### Capstone: <title>`: an exercise prompt, a model artifact or answer, then `**What reviewers look for.**` mapped to the Appendix C Tier-4 row.
6. **Questions** — Tiers 2/3/4 as above.
7. **Common mistakes & red flags** — same as Chapters 1–12.

Diagrams are optional in Part E; every mermaid rule applies when one appears.

## Cross-references

- Refer to traces by global number ("Trace 9"), figures by "Figure 4.2", chapters by "Chapter 5", labs by "Lab 8", questions by "Q 4.3".
- Trace numbers are the permanent addressing scheme: labs and exams reference them ("builds on Trace 9"). Splitting a trace renumbers, and is a reviewed change.

## Length budgets (hard-ish)

- Ch 1: ~2,000 words · Ch 2: ~3,600 · Ch 3: ~3,200 · Ch 4: ~4,200
- Ch 5: ~2,400 · Ch 6: ~3,000 · Ch 7: ~3,800 · Ch 8: ~3,000
- Ch 9: ~2,800 · Ch 10: ~3,200 · Ch 11: ~2,800 · Ch 12: ~3,400
- Ch 13: ~3,000 · Ch 14: ~2,600 · Appendices: ~4,200
- Counting rule: `sed '/^```/,/^```/d' chapters/chNN.md | wc -w` — fenced blocks (diagrams and code) do not count.
- Over budget → cut noise, not traces. Budgets may be reset to shipped reality plus ~5% headroom if they drift; an unenforceable budget is worse than an honest one.

## Code-reading exercises (Chapter 4 only)

Three short Python snippets (15–35 lines each) building on the plain tool loop, each with 1–3 planted bugs.
Format: the snippet, then `**What's wrong?**`, then the answer explaining the bug, why it hurts in production, then `**Fix.**`.
Bugs must be realistic (an unbounded tool result that floods the context, a non-idempotent tool the loop retries, a swallowed tool error the model reads as success).

## Out of scope (do not smuggle in)

Fine-tuning and RL post-training (one Appendix D bet entry only), voice/realtime agents,
embedding-model training, agent product/UI design (one Chapter 13 mention).
