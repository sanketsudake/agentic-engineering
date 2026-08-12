# Plan — Agentic Engineering Worksheet

## Context

Build a new handbook/worksheet repo at `/Users/sanketsudake/personal/agentic-engineering` (currently empty),
modeled on `/Users/sanketsudake/personal/k8s-worksheet`.
Goal: skill engineers at all levels (junior → staff/principal) in Agentic Engineering,
so they hold a concrete mental model of the domain,
can architect solutions,
and can solve problems intuitively.

User decisions (fixed):
- Scope: building agents end-to-end AND operating coding agents (Claude Code-style harnesses, workflows).
- Tests: all three forms — hands-on labs, tiered Q&A with rubric, per-level assessment exams.
- Stack: multi-framework (concepts neutral; examples across Anthropic SDK, OpenAI Agents SDK, LangGraph).
- Audience: one book, level-tagged for all levels.

What transfers from k8s-worksheet:
STYLE.md as an enforceable contract;
a globally numbered spine unit indexed in a root file;
fixed chapter shape;
mermaid diagrams with a 7pt-on-A4 size gate and caption coupling;
tiered Q&A + answer-quality rubric;
a normative fact ledger (`notes/research-notes.md`);
the ~150-line `build.py` (mermaid-cli + python-markdown + WeasyPrint → one A4 PDF);
one-workflow CI with release-on-tag.

## Reconciled design decisions

- **Spine unit:** `### Trace N: What happens when <event>` — same strict format as k8s "Flow"
  (setup sentence → 6–15 actor-first numbered steps → one mermaid diagram + `*Figure N.M — …*` caption → "Where this can fail" Symptom/Cause/Where-to-look bullets).
  Indexed in root `TRACES.md`. **Master trace = Trace 2** (full agent loop); every chapter states which Trace-2 steps it zooms into.
- **Levels:** `L1 Builder` (can build a working agent) / `L2 Operator` (can debug, eval, productionize) / `L3 Architect` (judgment, platform, economics).
  Question tiers carry the levels (Tier 1 → L1, Tier 2–3 → L2, Tier 4 → L3); chapters carry a level band in the opener + a Level column in TRACES.md; L3-only sections get an `(L3)` heading suffix.
  `[L1|L2|L3]` tag syntax allowed only on: chapter opener line, lab callouts, exam section heads.
- **Multi-framework (user-confirmed interpretation):** delivered as "primary + deltas", NOT parallel inline samples per stack.
  Prose/traces/diagrams framework-neutral (role names, never SDK classes).
  Inline code = plain Python + Anthropic SDK ("no-framework first"), ≤2 snippets/chapter, ≤40 lines each.
  A `### In other stacks` box (3–6 bullets, OpenAI Agents SDK + LangGraph) is MANDATORY in every Ch 1–12 chapter,
  plus dedicated framework labs (06 OpenAI Agents SDK, 07 LangGraph) and Appendix E "Framework Rosetta" table.
  Rationale: parallel examples roughly triple code maintenance; churn is quarantined to boxes + appendix + fact ledger, all dated.
- **Labs attach to chapters** as callout blockquotes (`> **Lab N — title.** \`labs/labNN-slug/\` · L2 · ~45 min · offline.`) placed after the section that teaches the mechanism.
  `build.py` renders these as styled boxes and collects a Labs index; `check_book.py` enforces every lab referenced from exactly one chapter.
- **Exams in PDF:** `exam.md` (questions + blank score sheet) renders as the final "Assessment" part; `key.md` is repo-only, never rendered.
- **Candidate edition:** actually build the answers-stripped PDF (`pdf-candidate` target) with a closed answer-marker registry + strip-integrity check.

## Book architecture (chapters/)

14 chapters + appendices, ~47K words (word counts exclude fenced blocks; k8s counting rule).
Chapter shape (Ch 1–12): Why this chapter → Concepts (+ `### In other stacks` box) → Traces → Questions (Tier 1/2/3) → Common mistakes & red flags.
Part E (Ch 13–14): judgment shape — Scenario→Critique, Capstone→"What reviewers look for", Tier 2/3/4 questions.

### Part A — Foundations: the loop and the model
| Ch | Title | Words | Levels | Scope |
|---|---|---|---|---|
| 1 | The Agent Loop: Big Picture | ~2,000 | L1–L2 | what an agent is (model+loop+tools+context); master trace; harness vs model; agents vs workflows |
| 2 | Models & the API Surface | ~3,600 | L1–L2 | tokens/sampling, messages/tool-use API, structured output, streaming, prompt caching, system prompts |
| 3 | Context Engineering | ~3,200 | L1–L3 | context anatomy, per-turn assembly, budgets/token math, compaction, context rot/poisoning, JIT vs preloaded, sub-context isolation |

### Part B — Capabilities: what the loop can reach
| Ch | Title | Words | Levels | Scope |
|---|---|---|---|---|
| 4 | Tool Design & MCP | ~4,200 | L1–L3 | schemas/descriptions as prompts, execution end-to-end, errors/idempotency/retries, result budgets, sandboxing mechanics, tool classes, MCP architecture. **Hosts the 3 code-reading exercises** (planted bugs: unbounded tool result, non-idempotent tool retried, swallowed error read as success) |
| 5 | Memory & State | ~2,400 | L2 | short vs long-term, session state, files-as-memory, write/consolidation, recall, persist vs recompute |
| 6 | Retrieval & RAG | ~3,000 | L1–L2 | ingest (chunk/embed/index), query-time RAG, hybrid search, agentic search alternative, long context vs retrieval |

### Part C — Coding agents: the harness and how to drive it
| Ch | Title | Words | Levels | Scope |
|---|---|---|---|---|
| 7 | Inside a Coding-Agent Harness | ~3,800 | L1–L2 | session startup (settings, memory files, skill discovery, MCP connect), permission model, hooks, skills/slash commands, sandbox boundaries. Claude Code = worked example, deltas boxed |
| 8 | Operating Coding Agents: Workflows | ~3,000 | L2 | spec-driven dev, plan-then-execute/decomposition (owner), subagent delegation mechanics, parallel worktrees, CI agents, review loops, steer vs let-run |

### Part D — Systems: production trust
| Ch | Title | Words | Levels | Scope |
|---|---|---|---|---|
| 9 | Multi-Agent Orchestration | ~2,800 | L2–L3 | orchestrator-worker, handoffs, shared artifacts/conflict, topologies, context isolation, A2A (brief), when 1 agent beats N |
| 10 | Evals | ~3,200 | L2–L3 | eval-driven dev, datasets, graders (code/LLM-judge/human), pass@k, judge calibration/bias, regression gates. Owns OFFLINE eval; Ch 12 owns online telemetry |
| 11 | Safety & Guardrails | ~2,800 | L2–L3 | threat model (injection via tool output, exfiltration, excessive agency), defense layers, lethal trifecta. Owns judgment layer; mechanics cross-ref Ch 4/7 |
| 12 | Production Ops, Cost & Latency | ~3,400 | L2–L3 | deployment shapes, observability/tracing, failure handling (timeout/retry/fallback), cost engineering (caching, tiering), latency anatomy (TTFT, tokens/s, iterations), config versioning, staged model upgrades |

### Part E — Judgment at staff/principal scale
| Ch | Title | Words | Levels | Scope |
|---|---|---|---|---|
| 13 | Architecture Judgment & Org Adoption | ~3,000 | L3 | build vs buy, framework selection, agents-vs-workflows decisions, eval-gated org rollout, incident response, team skilling, ROI. Scenario→Critique format |
| 14 | Lineage, Frontier & Capstones | ~2,600 | L3 | lineage (chatbots→RAG→tool-use→agents→harnesses), frontier bets with judgment, 2 capstones ("agent platform for a 200-engineer org"; "redesign the coding agent"). No traces (k8s Ch 12 precedent) |

Appendices ~4,200 words:
- **A** Quick-reference tables: context-budget math, cache economics, sampling params, tool-schema checklist, retry/timeout defaults, latency anatomy, model-selection dimensions, cross-chapter failure-mode grid, one dated model & pricing snapshot (only volatile-number location).
- **B** Glossary (one-liners).
- **C** Answer-quality rubric (per-tier strong/weak, one worked weak/strong/principal answer; tier→level map; "How to read at your level" table).
- **D** The architect's lens (per-chapter zoom-out; recurring bets: agents vs workflows, long context vs retrieval, single vs multi-agent, prompting vs fine-tuning, build vs buy, autonomy vs oversight; critique prompts).
- **E** Framework Rosetta (concept ↔ Anthropic/OpenAI Agents SDK/LangGraph table + "which stack when").
- **F** Further reading (dated).

Declared out of scope (stated in STYLE.md): fine-tuning/RL post-training (Appendix D bet only), voice/realtime agents, embedding-model training, agent product/UI design.

## Trace catalog (35 traces — the completeness checklist for TRACES.md)

- Ch1: **1** one message to a model (anchor); **2** user request → finished task (MASTER).
- Ch2 (zooms step 3): **3** output matching a schema; **4** model decides to call a tool (token-level); **5** a response streams; **6** prompt cache hits — and misses.
- Ch3 (steps 2,6): **7** context for a turn is assembled; **8** context window fills (compaction).
- Ch4 (steps 4–6): **9** tool call executes end-to-end; **10** tool call fails; **11** agent calls an MCP server.
- Ch5 (steps 2,9): **12** agent recalls a fact; **13** session ends and memory is written.
- Ch6 (steps 2,5): **14** document becomes searchable; **15** RAG query runs; **16** agent searches instead (agentic retrieval).
- Ch7 (steps 1,4,9): **17** coding-agent session starts; **18** harness gates a dangerous action; **19** a hook fires; **20** a skill/slash command is invoked.
- Ch8: **21** feature ships spec-first; **22** work delegated to a subagent; **23** CI agent handles a PR.
- Ch9: **24** orchestrator fans work out; **25** one agent hands off to another; **26** two agents write the same artifact (conflict).
- Ch10: **27** eval suite runs; **28** LLM judge grades a transcript.
- Ch11: **29** prompt injection arrives in tool output; **30** agent tries to exfiltrate data.
- Ch12: **31** production request fails over; **32** bad session is traced; **33** underlying model is upgraded.
- Ch13 (org scale): **34** agent change ships across an org; **35** injection incident is triaged.

## Diagram strategy

All k8s mermaid rules inherit unchanged (types, autonumber, ≤6-word messages, size gate, ≤12 nodes, caption coupling, all-or-nothing classing).
Fixed participant vocabulary (all chapters): `User`, `Harness`, `LLM`, `Tools`, `MCP`, `Mem`, `Idx`, `Env`, `Sub`, `Guard`, `Judge`, `Obs`, `CI`. ≤8 lanes per diagram.
Semantic palette: reuse the six k8s classDefs/hex values, roles remapped (leader=loop driver, standby=idle worker, lease=gate/queue/lock, resource=artifact/context acted on, external=provider/3rd-party, process=logic).

## Assessment system

### Labs (12, in `labs/`)
Per-lab contract: `labs/labNN-slug/` with `README.md` (level, stack, time, offline/live commands), `pyproject.toml` + committed `uv.lock`, `starter/`, `solution/`, `tests/` (pytest; `LAB_TARGET=starter|solution` via conftest).
Reader: `uv sync && uv run pytest` — red tests are the task list.
Offline-first (hard requirement, CI-enforced with zero secrets): three mechanisms —
(1) **ScriptedModel** injection (deterministic in-process fake, `labs/common/` package `worksheet_common`);
(2) **mockllm** stdlib HTTP server serving OpenAI-shaped + Anthropic-shaped endpoints for SDK/framework labs via `base_url`;
(3) **recorded transcripts + config linting** for coding-agent labs (no credible fake for a full harness; live runs optional behind `@pytest.mark.live`, deselected by default).

Roster (lab → owning chapter; a lab ships in the same phase as its owning chapter):
01 first model call + structured output (L1, anthropic SDK, mockllm → Ch 2) ·
02 define/dispatch tools (L1, plain, ScriptedModel → Ch 4) ·
**03 build the tool loop (L1, exemplar A → Ch 1)** ·
04 context truncation & compaction (L2 → Ch 3) ·
05 debug a broken agent, planted bugs (L2 → Ch 4) ·
06 multi-agent handoffs (L2, OpenAI Agents SDK, mockllm → Ch 9) ·
07 stateful graph agent + checkpointing (L2, LangGraph, fake chat model → Ch 5) ·
**08 write an eval (L2, exemplar B → Ch 10**: graders must score good agent ≥0.8 and planted-bug variant ≤0.5**)** ·
09 operate a coding agent: CLAUDE.md/permissions/sessions (L2, transcript analysis + config linting → Ch 8) ·
10 tracing & failure taxonomy on production transcripts (L3 → Ch 12) ·
11 guardrails & tool-permission design (L3, adversarial scripts → Ch 11) ·
12 capstone: eval-gated agent release (L3, composes 03+08 → Ch 14).

### Tiered Q&A
Identical to template: Tier 1 Explain / 2 Reason / 3 Design & Debug (Ch 1–12: 3–4/3–4/2–3), Part E Tier 2/3/4; `**Q N.M**` → `**Answer.**` → `*Strong answers also mention:*`. Appendix C is the rubric.

### Exams (`exams/l1|l2|l3/`)
`exam.md` (in PDF) + `key.md` (repo-only, point-anchored: "award 3 pts if …") + `practical/` (uv project, pytest-scored, offline; L1 lighter, L3 adds a Tier-4 judgment memo scored on the rubric's L3 row).
L2 exemplar: 3h, 100 pts — A written 60 pts (2×T1@5, 3×T2@10, 2×T3@10), B code-reading 10 pts (3 planted bugs), C practical 30 pts (10 pytest checks × 3; diagnose+fix a failing eval, extend the eval to lock the fix).
Pass: ≥70 total AND ≥18/30 on C.
Exams are written LAST (Phase 5) so they sample the finished book.

## Repo layout

```
agentic-engineering/
├── README.md  STYLE.md  CONTRIBUTING.md  LICENSE  Makefile  requirements.txt  .gitignore
├── TRACES.md                         # trace index (FLOWS.md analog) + level column
├── chapters/ ch01..ch14.md, appendices.md
├── labs/ README.md, common/ (worksheet_common: scripted_model.py, mockllm.py, transcripts.py), labNN-slug/…
├── exams/ README.md, l1/ l2/ l3/ (exam.md, key.md, practical/)
├── build/ build.py, check_diagrams.py (verbatim), check_book.py (new), mermaid-config.json, style.css, cover.html
├── notes/ research-notes.md, worksheet-plan.md (this plan, archived)
├── .github/ dependabot.yml, workflows/build-pdf.yml, workflows/labs.yml
└── dist/ (gitignored)
```

Not a uv workspace: each lab is a standalone uv project with its own lockfile (framework pin sets conflict; isolation keeps one broken lab from blocking others). Build pipeline stays on plain `requirements.txt`.

## Build pipeline deltas (build.py, small — verified against template by plan-reviewer)

1. Constants at top: new `PARTS`; `SPINE_LABEL = "Trace"`.
   "Flow" appears in exactly 3 functional places in the template (`build.py:108` replacement string, `:110` regex — note it runs on rendered HTML `<h3>Flow (\d+):`, not markdown — and `:129` TOC heading); interpolate the constant into all three.
   The `flow-{num}` anchors and `class="flow"` CSS selector can keep their internal names.
2. TOC index heading must compute its count dynamically (`f"The {len(entries)} traces"`) — the template hardcodes "The 30 flows" at `build.py:129`.
3. Appendix regexes: widen `Appendix [A-E]` (`build.py:112`) and `appendix-[a-e]` (`:114`) to `[A-F]` — the plan has six appendices; the failure is silent (Appendix F would render with no TOC entry).
4. Level badges: `\[L([123])\]` → colored pill span (~8 lines + 3 CSS rules).
5. Lab callouts: regex `^> \*\*Lab (\d+) — (.+?)\.\*\*` → `<aside class="lab">`; collect a Labs index next to the trace index on the TOC page.
6. Assessment part: `PARTS` gains `("Assessment", ["../exams/l1/exam.md", …l2, …l3])`; `key.md` never listed.
   Verified: `os.path.join(CH, "../exams/…")` resolves fine.
   Constraint: every PARTS file MUST start with `# Title` on line 1, no frontmatter (`build.py:100` crashes otherwise) — this is a rule for exam.md files.
7. Candidate edition: `STRIP_ANSWERS=1` applies `strip_answers()` → `dist/…-candidate.pdf`.
   Closed marker registry with PER-MARKER strip boundaries (uniform marker-to-next-heading would delete later question prompts, since `**Q N.M**` lines are paragraphs, not headings):
   `**Answer.**` and `*Strong answers also mention:*` strip to the next `**Q` or heading;
   `**What's wrong?**` answers, `**Fix.**`, `**Critique.**`, `**What reviewers look for.**` strip to the next heading.
8. Rename the output filenames: `dist/kubernetes-internals-worksheet.pdf` is hardcoded at `build.py:152` AND in the workflow's artifact/release steps (`build-pdf.yml:43,52,54`).
9. `cover.html` needs a full rewrite in Phase 0 (title, subtitle, trace count, baseline line are all k8s-specific); final cover art in Phase 6. `style.css` needs no functional changes.
Note: the markdown pipeline enables `smarty`, so any code comparing raw markdown titles to rendered HTML titles must account for typographic transforms (quotes, dashes).
Makefile targets: `pdf`, `pdf-candidate`, `check`, `check-labs`, `clean`.

## Quality gates & CI

- `check_diagrams.py`: reused verbatim (rename cache dir).
- `check_book.py` (new, stdlib-fast): chapter shape + question counts/IDs; cross-refs resolve (Trace/Figure/Chapter/Lab) + every lab dir referenced exactly once; candidate-strip integrity (stripped text contains zero answer markers, every question keeps its prompt — this also guards the per-marker strip boundaries); exam consistency (exam↔key ID parity, points sum to declared total, C points = test count × per-test, pass bar ≤ total); appendix/TOC entry parity (every `## Appendix X` gets a TOC entry — guards the regex-widening delta); level-tag placement; word budgets (warn; `--strict` on release).
- `build-pdf.yml`: check_book → deps → check_diagrams → build both editions → upload; on `v*` tags attach both to release. Dependabot: actions + pip + per-lab dirs, grouped weekly.
- `labs.yml`: install uv first (`astral-sh/setup-uv` action — the template has no labs workflow to inherit this from); matrix over `labs/lab*` + `exams/*/practical`; `uv sync --frozen && LAB_TARGET=solution uv run pytest -m "not live"`. **No secrets ever** (enforces the no-key guarantee). Path-filtered to labs/exams. Optional workflow_dispatch live job for maintainers.

## STYLE.md deltas (appended to adapted template contract)

Trace format + participant vocab + palette remap; level scheme + tag syntax + tier→level map; lab callout format; lab authoring contract (offline default, solution passes identical tests, pinned lockfile, model access via injection/base_url only); exam format + `exam.md` must start with `# Title` on line 1 (no frontmatter — build.py requirement) + key.md never rendered rule; multi-framework code rules (no-framework first, ≤40-line snippets, mandatory `### In other stacks` box, version claims must match research-notes.md); answer-marker registry incl. `**Fix.**` with per-marker strip boundaries (new marker ⇒ update strip_answers + check_book in same commit); declared out-of-scope list.

## Fact ledger (`notes/research-notes.md`)

Baseline declared as "August 2026", every entry sourced + dated; verify facts via web/docs at writing time (never from planning docs).
Sections: model families/capabilities; provider API feature status (GA/beta + date); MCP spec facts; harness facts (Claude Code hooks/skills/subagents/settings); framework facts (Rosetta raw material); pricing snapshot (feeds only Appendix A table); terminology rulings ("agent", "harness", "context engineering", "workflow vs agent").
Rules: name a model/version only when correctness demands it; never present beta as default; unverifiable ⇒ phrase as pattern not product claim; stale entry (>1 build cycle) blocks reuse.

## Phased execution (each boundary = both PDFs green, gates pass, lab CI green, readable end-to-end)

- **Phase 0 — Skeleton & pipeline proof.** `git init` + create GitHub repo + push (CI/release path needs a remote); copy the template's LICENSE; copy/adapt `build/` from k8s-worksheet (all 9 build deltas above, incl. cover.html rewrite); STYLE.md, CONTRIBUTING.md, README.md, TRACES.md (catalog above), Makefile, CI, dependabot; check_book.py; one stub chapter + stub `exam.md` for ALL THREE levels (PARTS lists all three statically and build.py crashes on a missing file) exercising every renderer feature (badge, callout, trace index, appendix TOC, strip).
- **Phase 1 — Style proof.** Ch 1 written for real (Traces 1–2, anchor diagrams, questions) + lab03 built in full (starter/solution/tests) + callout wired. Validates the whole contract on real content. Populate research-notes.md before further writing.

Lab-phase rule: a lab ships in the same phase as its owning chapter, so the "every lab referenced from exactly one chapter" gate stays green at every boundary.
- **Phase 2 — Part B + Ch 7 (the heart: tools/MCP + harness) + labs 02, 05 (Ch 4), 07 (Ch 5); Appendix C rubric drafted.**
- **Phase 3 — Part A remainder (Ch 2–3) + Part C remainder (Ch 8) + labs 01 (Ch 2), 04 (Ch 3), 09 (Ch 8); mockllm hardened; ledger populated with pinned SDK facts.**
- **Phase 4 — Part D + Part E + labs 06 (Ch 9), 08 (Ch 10), 10–12 + appendices complete.**
- **Phase 5 — Exams** (L2 exemplar first, then L1/L3; practicals derive from lab harnesses). Reviewable: a volunteer can sit the L2 exam offline end-to-end.
- **Phase 6 — Polish & v1.0.** Word budgets `--strict`, cross-ref sweep, cover art, book-card, tag `v1.0` → release both PDFs.

## Verification

- Every phase: `make check` (check_book + check_diagrams) and `make pdf && make pdf-candidate` succeed locally; open the PDF and inspect the new pages.
- Labs: `make check-labs` (all solutions green offline, no keys in env).
- Candidate edition: grep the stripped HTML for each registry marker → zero hits.
- CI: both workflows green on push; `v0.x` pre-release tag exercises the release path early (Phase 1).
- Exam: dry-run the L2 exam yourself (or a volunteer) against the key before v1.0.

## Key reference files (template)

- `/Users/sanketsudake/personal/k8s-worksheet/STYLE.md` — contract to adapt
- `/Users/sanketsudake/personal/k8s-worksheet/build/build.py`, `check_diagrams.py`, `style.css`, `cover.html`, `mermaid-config.json` — pipeline to copy
- `/Users/sanketsudake/personal/k8s-worksheet/chapters/ch01.md` (anchor chapter), `ch06.md` (code exercises), `ch12.md` (judgment format), `appendices.md` (rubric/tables)
- `/Users/sanketsudake/personal/k8s-worksheet/FLOWS.md` — TRACES.md format
- `/Users/sanketsudake/personal/k8s-worksheet/.github/workflows/build-pdf.yml` — CI base
