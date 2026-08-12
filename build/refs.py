"""The cross-reference map: what a Chapter/Trace/Appendix reference points at.

One module builds the map from the chapter files themselves, so the anchors
can never drift from the headings. `linkify.py` inserts the links,
`check_book.py` verifies them, and `build.py` rewrites them for the PDF.

Anchors are GitHub heading slugs, so a reader browsing the repository gets
working links; `build.py` converts them to internal anchors for the PDF.
"""
from __future__ import annotations

import glob
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CH_DIR = os.path.join(ROOT, "chapters")


def github_slug(heading: str) -> str:
    """GitHub's heading-anchor slug: lowercase, drop punctuation, spaces to hyphens."""
    s = heading.strip().lower()
    s = re.sub(r"[^\w\s-]", "", s)      # drop punctuation, keep word chars and hyphens
    return re.sub(r"\s", "-", s)         # every space becomes a hyphen


def build_map() -> dict:
    """Return {"chapters": {n: file}, "traces": {n: (file, anchor)},
    "appendices": {letter: (file, anchor)}, "titles": {n: title}}."""
    chapters, traces, appendices, titles = {}, {}, {}, {}

    for path in sorted(glob.glob(os.path.join(CH_DIR, "ch[0-9][0-9].md"))):
        fn = os.path.basename(path)
        num = int(fn[2:4])
        text = open(path).read()
        chapters[num] = fn
        m = re.match(r"# (.+)", text)
        if m:
            titles[num] = m.group(1).strip()
        for line in text.split("\n"):
            t = re.match(r"^### (Trace (\d+): .+)$", line)
            if t:
                traces[int(t.group(2))] = (fn, github_slug(t.group(1)))

    app_path = os.path.join(CH_DIR, "appendices.md")
    if os.path.exists(app_path):
        for line in open(app_path).read().split("\n"):
            a = re.match(r"^## (Appendix ([A-Z]) .+)$", line)
            if a:
                appendices[a.group(2)] = ("appendices.md", github_slug(a.group(1)))

    return {"chapters": chapters, "traces": traces,
            "appendices": appendices, "titles": titles}


def owner_chapter(trace_num: int, refs: dict) -> int | None:
    """Which chapter carries this trace, as an int (None if unwritten)."""
    entry = refs["traces"].get(trace_num)
    return int(entry[0][2:4]) if entry else None


def iter_prose(text: str):
    """Yield (index, line) for lines outside fenced code blocks and headings."""
    fence = False
    for i, line in enumerate(text.split("\n")):
        if line.startswith("```"):
            fence = not fence
            continue
        if fence or line.startswith("#"):
            continue
        yield i, line
