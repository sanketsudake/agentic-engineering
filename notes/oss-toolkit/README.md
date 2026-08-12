# Open-source agent toolkit — author research notes

**Author-side material. No chapter may cite this directory** — the PDF does not contain it,
and the style contract forbids pointing a reader at a document the book does not carry.
Use it the way the fact ledger is used: to decide what to write, never as a reference the reader follows.

## Provenance

- **Source:** *Open Source Toolkit for Building AI Agents 2026 (Global Edition)*, an .xlsx workbook.
- **Compiled by:** Avinash Singh — Let's Code (lets-code.co.in).
- **Compiled:** August 2026. 404 entries across 20 catalogue sheets.
- **Captured here:** 2026-08-12, one markdown file per tab, tables preserved verbatim.

**This is someone else's curation.** The facts inside it (a project's licence, what it does) are
facts, but the selection, the wording, and the editorial ratings are the compiler's work.
Do not copy its descriptions into the book. If the book benefits from it, cite it in
Appendix F and write our own words.

## The compiler's own caveats, which apply to every file here

- Difficulty and Adoption are editorial judgements, not benchmarks.
- Licences and releases drift; verify on the linked repository before relying on either.
- Hardware prices are Indian-market estimates for August 2026 and will drift.
- Nothing in it is sponsored.

## How the tabs map to the book

| Tab | Book home | Note |
|---|---|---|
| 01 Agent Frameworks | Appendix E, Chapter 13 | our Rosetta covers 3 stacks; this shows the wider field |
| 02 Coding and CUA Agents | Chapters 7–8 | harness landscape beyond Claude Code |
| 03 Inference and Serving | Chapter 12 | serving, local runtimes, gateways |
| 04 Open Weight Models | Chapters 2, 12 | the self-hosted half of model selection |
| 05 Vector and Retrieval | Chapter 6 | vector stores and embedding infrastructure |
| 06 RAG and Data Pipeline | Chapter 6 | parsing, chunking, graph RAG |
| 07 Memory and Context | Chapters 3, 5 | memory layers and state persistence |
| 08 Tools MCP and Sandbox | Chapter 4 | MCP SDKs, tool platforms, sandboxes |
| 09 Observability and Evals | Chapters 10, 12 | tracing and eval frameworks |
| 10 Guardrails and Security | Chapter 11 | guardrails, red teaming, regulation |
| 11 Fine-tuning and RL | Appendix D | the one place the book discusses fine-tuning |
| 12 Agent UI and Low-Code | — | out of scope (agent product and UI design) |
| 13 Voice and Multimodal | — | out of scope |
| 14 Deploy and Infra | Chapter 12 | containers, queues, durable execution |
| 15 Stack Recipes | Appendix E | seven end-to-end stacks by budget |
| 16 Learning Roadmap | Appendix C | compare against our level reading paths |
| 17 Project Ideas | labs, capstones | compare against our 12 labs |
| 18 Interview Prep | questions, exams | 40 questions; ours are separate work — do not copy |
| 19 Hardware and Cost | Appendix A | self-hosting cost, which our snapshot omits |
| 20 Resources and Community | Appendix F | papers, leaderboards, communities |

## What the book does not have, and this does

1. **Per-step reliability arithmetic.** "95% per step is 36% over 20 steps."
   The book argues qualitatively that errors compound; it never does the multiplication.
2. **The self-hosted half of the stack.** The book is vendor-neutral and names almost no
   concrete tool. A reader who must choose a vector store or a serving engine gets no map.
3. **Hardware and self-hosting cost.** Our pricing snapshot covers hosted API tiers only.

## What was taken into the book (2026-08-12)

- **Appendix G — The open-source stack, by layer.** A map of 16 layers with what you choose,
  what to judge it on, and 3–4 representative projects. Categories, not a catalogue: the layers
  are stable, the projects are dated and will drift. The appendix attributes the shortlist to
  the toolkit's compiler.
- **Appendix A — Reliability over a loop.** The per-step reliability table (99/95/90/80% over
  5/10/20/50 steps). The arithmetic is ours; the toolkit's "accuracy compounds downward" framing
  prompted it. Chapter 12 now points at it from the turn-count ranking.

Deliberately **not** taken: the interview questions (tab 18 — ours are separate work), the tool
descriptions themselves (that is the compiler's writing), the India-specific hardware prices
(tab 19), and everything in the tabs the book declares out of scope (12 Agent UI, 13 Voice).
