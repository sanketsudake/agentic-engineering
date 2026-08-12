# Contributing

## Repo layout

```
STYLE.md            the writing contract — read it before touching a chapter
TRACES.md           index of the 35 traces (the book's spine and checklist)
chapters/           one markdown file per chapter + appendices.md
labs/               hands-on labs; labs/common holds the shared offline harness
exams/              per-level exams: exam.md (in PDF), key.md (repo-only), practical/
build/              build.py (PDF pipeline), check_book.py, check_diagrams.py
notes/              research-notes.md (normative fact ledger), worksheet-plan.md
dist/               build output (gitignored)
```

## Making changes

1. Read [STYLE.md](STYLE.md) first. It is a contract, not guidance.
2. Edit the chapter, lab, or exam.
3. Keep every version-sensitive fact in sync with `notes/research-notes.md`.
4. Run the gates and rebuild:

```bash
make check        # check_book.py (content linter) + check_diagrams.py (size gate)
make pdf          # full edition
make pdf-candidate  # answers-stripped edition
make check-labs   # every lab's solution passes its tests, offline
```

## Three things that fail silently

- **Caption coupling.** Prose between a ```` ```mermaid ```` fence and its `*Figure N.M — …*`
  line breaks the match: the build exits 0 and raw mermaid lands in the PDF.
  `check_diagrams.py` counts fences, captions, and matches, and fails loudly on mismatch.
- **Diagram size.** A diagram can render fine on GitHub and print unreadably small on A4.
  `python3 build/check_diagrams.py chapters/*.md` measures printed label size; 7 pt is the gate.
- **Lab callouts.** A malformed `> **Lab N — title.**` opener renders as a plain
  blockquote instead of a lab box, and the lab drops out of the Labs index.
  `check_book.py` catches it.

## Building the PDF

Prereqs:

```bash
pip install -r requirements.txt
npm install -g @mermaid-js/mermaid-cli
```

WeasyPrint needs system libraries on Linux (`libpango-1.0-0 libpangoft2-1.0-0`)
plus the DejaVu and Liberation fonts.
Set `CHROME_PATH` if mermaid-cli cannot find a Chromium.
Diagrams cache in `dist/diagrams/` by content hash; `make clean` resets everything.

## Labs

Each lab is a standalone uv project:

```bash
cd labs/lab03-tool-loop
uv sync
uv run pytest                      # red tests are your task list
LAB_TARGET=solution uv run pytest  # the reference solution passing
```

Every lab completes offline with zero API keys.
Live-model tests are optional and marked `live`.

## CI

- `build-pdf.yml` — content linter → diagram gate → both PDF editions on every push and PR;
  attaches both PDFs to the release on `v*` tags.
- `labs.yml` — runs every lab and exam practical against its solution, offline, no secrets.
