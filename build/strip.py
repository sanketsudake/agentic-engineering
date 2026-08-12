"""Answer stripping for the candidate edition.

Shared by build.py (applies it) and check_book.py (verifies it), and kept
stdlib-only so the checker can run before any pip install.

Closed marker registry. Each marker strips from its line to a per-marker
boundary. "**Q N.M**" lines are paragraphs, not headings, so answer markers
must stop at the next question — a next-heading rule would eat later prompts.
Adding a marker requires updating check_book.py in the same commit.
"""
import re

HEADING_RE = re.compile(r"^#{1,3} ")
QUESTION_RE = re.compile(r"^\*\*(Q \d+\.\d+|E\d\.[A-Z]\d+)")
ANSWER_MARKERS = (r"^\*\*Answer\.\*\*", r"^\*Strong answers also mention:\*")
SECTION_MARKERS = (r"^\*\*Fix\.\*\*", r"^\*\*Critique\.\*\*",
                   r"^\*\*What reviewers look for\.\*\*")
WHATS_WRONG_RE = re.compile(r"^\*\*What's wrong\?\*\*")
ALL_MARKERS = ANSWER_MARKERS + SECTION_MARKERS


def strip_answers(md_text: str) -> str:
    out, i, lines = [], 0, md_text.split("\n")

    def until(start, stop_at_question):
        j = start
        while j < len(lines):
            l = lines[j]
            if HEADING_RE.match(l) or (stop_at_question and QUESTION_RE.match(l)):
                break
            if stop_at_question and any(re.match(p, l) for p in SECTION_MARKERS):
                break
            j += 1
        return j

    while i < len(lines):
        line = lines[i]
        if any(re.match(p, line) for p in ANSWER_MARKERS):
            i = until(i + 1, stop_at_question=True)
        elif any(re.match(p, line) for p in SECTION_MARKERS):
            i = until(i + 1, stop_at_question=False)
        elif WHATS_WRONG_RE.match(line):
            out.append(line)   # keep the prompt, drop the explanation under it
            i = until(i + 1, stop_at_question=False)
        else:
            out.append(line)
            i += 1
    return "\n".join(out)
