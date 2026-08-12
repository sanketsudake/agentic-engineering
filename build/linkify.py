#!/usr/bin/env python3
"""Turn plain cross-references into links, mechanically.

Authors write "Chapter 3", "Trace 9", "Appendix C" as plain text.
This script inserts the correct link and anchor, so nobody hand-writes a slug.
It only links references that LEAVE the current file: a chapter's own traces
stay plain, because the reader is already there.

Figures and questions are never linked — their anchors do not exist on GitHub.
Exam files are never linked either: an exam must not point at its own answers.

Usage: python3 build/linkify.py [--check]
       --check exits 1 if any file would change (CI use).
"""
from __future__ import annotations

import glob
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from refs import CH_DIR, build_map

# A reference already inside a link, or inside a code span, is left alone.
LINKED = r"(?<!\[)"


def linkify_text(text: str, own_chapter: int | None, refs: dict) -> str:
    out, fence = [], False
    for line in text.split("\n"):
        if line.startswith("```"):
            fence = not fence
            out.append(line)
            continue
        if fence or line.startswith("#"):
            out.append(line)
            continue
        out.append(linkify_line(line, own_chapter, refs))
    return "\n".join(out)


def _protect(line: str):
    """Blank out code spans and existing links so we never nest a link."""
    spans = []

    def hide(m):
        spans.append(m.group(0))
        return f"\x00{len(spans) - 1}\x00"

    line = re.sub(r"`[^`]*`", hide, line)
    line = re.sub(r"\[[^\]]*\]\([^)]*\)", hide, line)
    return line, spans


def _restore(line: str, spans: list) -> str:
    return re.sub(r"\x00(\d+)\x00", lambda m: spans[int(m.group(1))], line)


def linkify_line(line: str, own_chapter: int | None, refs: dict) -> str:
    line, spans = _protect(line)

    def chapter_sub(m):
        n = int(m.group(1))
        if n == own_chapter or n not in refs["chapters"]:
            return m.group(0)
        return f"[Chapter {n}]({refs['chapters'][n]})"

    def trace_sub(m):
        n = int(m.group(1))
        entry = refs["traces"].get(n)
        if not entry:
            return m.group(0)
        fn, anchor = entry
        if own_chapter is not None and int(fn[2:4]) == own_chapter:
            return m.group(0)          # same chapter: the reader is already here
        return f"[Trace {n}]({fn}#{anchor})"

    def appendix_sub(m):
        letter = m.group(1)
        entry = refs["appendices"].get(letter)
        if not entry or own_chapter is None:
            return m.group(0)          # inside appendices.md itself: leave plain
        fn, anchor = entry
        return f"[Appendix {letter}]({fn}#{anchor})"

    line = re.sub(LINKED + r"\bChapter (\d+)\b", chapter_sub, line)
    line = re.sub(LINKED + r"\bTrace (\d+)\b", trace_sub, line)
    line = re.sub(LINKED + r"\bAppendix ([A-F])\b", appendix_sub, line)
    return _restore(line, spans)


def main() -> int:
    check = "--check" in sys.argv
    refs = build_map()
    changed = []

    paths = sorted(glob.glob(os.path.join(CH_DIR, "*.md")))
    for path in paths:
        fn = os.path.basename(path)
        own = int(fn[2:4]) if re.match(r"ch\d\d\.md", fn) else None
        text = open(path).read()
        new = linkify_text(text, own, refs)
        if new != text:
            changed.append(fn)
            if not check:
                open(path, "w").write(new)

    if check:
        if changed:
            print("FAIL  un-linked cross-references in:", ", ".join(changed))
            print("      run: python3 build/linkify.py")
            return 1
        print("==== PASS: every cross-reference is linked ====")
        return 0

    print(f"linkified {len(changed)} file(s): {', '.join(changed) or 'none'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
