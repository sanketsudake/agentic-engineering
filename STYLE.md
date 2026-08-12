# STYLE.md — rules every chapter, lab, and exam must follow

**What this document is:** the contract for writing the "Agentic Engineering Worksheet".
Follow it exactly so all chapters read as one book,
all labs check the same way,
and all exams grade the same way.

## Audience and voice

Reader: an engineer at any level, junior through principal, who builds or operates AI agents.
Many readers do not have English as a first language.
Reading fluency and comprehension come before every other quality in this book.

### Write in Simplified Technical English (ASD-STE100)

The book follows ASD-STE100, the controlled-English standard used for aerospace technical writing.
These are the rules that apply here:

- **One word, one meaning.** Each term keeps the same meaning everywhere in the book. Appendix B is the dictionary.
- **One meaning, one word.** Do not use synonyms for variety. If it is a "tool result", it is never a "tool response" or "tool output".
- **Short sentences.** Procedural sentences (trace steps, instructions): 20 words maximum. Descriptive sentences: 25 words maximum.
- **Short paragraphs.** 6 sentences maximum. One idea for each paragraph.
- **One instruction for each sentence.** Do not join two actions with "and" in a trace step.
- **Active voice.** "The harness appends the tool result", not "The tool result is appended".
- **Present tense** for how things work. Keep the tense simple.
- **Keep the articles.** Write "the harness reads the schema", not "harness reads schema".
- **Keep the relative pronouns.** Write "the result that the tool returned", not "the result the tool returned".
- **Noun clusters: 3 words maximum.** Break up "context window budget policy" into a phrase with a verb or a preposition.
- **No idioms, metaphors, jokes, or slang.** "The model gets confused" is not a mechanism; say what happens.
- **Positive statements.** Avoid double negatives. Write "surface every error", not "do not fail to surface errors".
- **Lists for sequences.** If the text has more than two steps, make it a numbered list.

Approved-word discipline in practice: prefer the simple verb.
Use "use" not "utilize", "start" not "initiate", "show" not "demonstrate", "before" not "prior to", "about" not "regarding", "if" not "in the event that".

### Cognitive flow

- **Answer first, detail second.** The first sentence of a section states the outcome. The mechanism follows.
- **Define a term before you use it.** Definitions come in one clause: "the harness (the runtime that owns the loop, context assembly, and gating)".
- **Never make the reader jump forward.** See the cross-reference rules below.
- High signal, low noise: no filler ("It is important to note that…"), no marketing tone, no repetition of what another section said.
- Never invent facts. Version-sensitive claims (model names, API features, SDK behavior, prices) must match the fact ledger the repository keeps for authors. Baseline is August 2026.
  Chapters never name that ledger or any other repository document that the PDF does not contain.

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
| `leader` | the component driving the loop (orchestrator, active agent) | `#0F766E` | `#115E59` |
| `standby` | idle worker, queued run, paused session | `#8B8177` | `#6B6259` |
| `lease` | gate, queue, lock, approval, eval gate | `#D97706` | `#B45309` |
| `resource` | the artifact acted on: context window, file, PR, dataset | `#BE123C` | `#9F1239` |
| `external` | provider API, third-party service | `#57534E` | `#44403C` |
| `process` | logic, decision, generic step | `#0369A1` | `#075985` |

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

The reader reads the book in order. A reference must never send them forward.

**Backward references only.** A chapter may point to itself and to every chapter before it.
It must not point to a later chapter, or to a trace that a later chapter carries.
When later material is genuinely out of scope, say so without a number and without a link:
"the policy questions come later in this book". The reader keeps reading.

One exception: Chapter 1 carries a `## How this book is organized` section.
That roadmap may name later chapters, because a map is not a jump.

**Hyperlink every cross-reference that leaves the current chapter.**
Plain-number references are for figures and questions only.

| Reference | Form | Example |
|---|---|---|
| Chapter | `[Chapter 3](ch03.md)` | link to the chapter file |
| Trace | `[Trace 9](ch04.md#trace-9-what-happens-when-a-tool-call-executes-end-to-end)` | link to the trace heading |
| Appendix | `[Appendix C](appendices.md#appendix-c--answer-quality-rubric)` | link to the appendix heading |
| Figure | `Figure 4.2` | plain text, same chapter only |
| Question | `Q 4.3` | plain text, same chapter only |
| Lab | `` `labs/lab08-write-eval/` `` | code span, never a link |

Anchors are the GitHub heading slugs, so the links work when a reader browses the repository.
`build/build.py` rewrites them to internal anchors when it builds the PDF, so the same links work there.
Do not hand-write the anchors: run `python3 build/linkify.py` and it inserts them.

Trace numbers are the permanent addressing scheme: labs and exams reference them ("builds on Trace 9").
Splitting a trace renumbers, and is a reviewed change.

## Length budgets (hard-ish)

- Ch 1: ~2,000 words · Ch 2: ~3,950 · Ch 3: ~3,500 · Ch 4: ~4,750
- Ch 5: ~2,650 · Ch 6: ~3,300 · Ch 7: ~4,150 · Ch 8: ~3,450
- Ch 9: ~3,200 · Ch 10: ~3,650 · Ch 11: ~3,250 · Ch 12: ~3,900
- Ch 13: ~3,450 · Ch 14: ~3,200 · Appendices: ~6,150
- Counting rule: `sed '/^```/,/^```/d' chapters/chNN.md | wc -w` — fenced blocks (diagrams and code) do not count.
- Over budget → cut noise, not traces. Budgets may be reset to shipped reality plus ~5% headroom if they drift; an unenforceable budget is worse than an honest one.
- (These budgets were reset in August 2026, after the book moved to Simplified Technical English.
  That style adds words on purpose: it splits long sentences, keeps every article and relative pronoun,
  and never compresses a phrase the reader would have to decode. Every chapter grew 4–10%.
  The old budgets would have forced the dense writing back in, so they were rebased instead.)

## Code-reading exercises (Chapter 4 only)

Three short Python snippets (15–35 lines each) building on the plain tool loop, each with 1–3 planted bugs.
Format: the snippet, then `**What's wrong?**`, then the answer explaining the bug, why it hurts in production, then `**Fix.**`.
Bugs must be realistic (an unbounded tool result that floods the context, a non-idempotent tool the loop retries, a swallowed tool error the model reads as success).

## Out of scope (do not smuggle in)

Fine-tuning and RL post-training (one Appendix D bet entry only), voice/realtime agents,
embedding-model training, agent product/UI design (one Chapter 13 mention).
