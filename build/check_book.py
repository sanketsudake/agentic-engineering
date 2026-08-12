#!/usr/bin/env python3
"""Content linter for the Agentic Engineering Worksheet.

Textual checks only — no rendering, stdlib only, fast enough for every CI run.
Word budgets warn by default; --strict turns them into failures (release gate).

Usage: python3 build/check_book.py [--strict]
"""
import glob, os, re, sys

BUILD = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(BUILD)
sys.path.insert(0, BUILD)
from strip import strip_answers, ALL_MARKERS, WHATS_WRONG_RE

STRICT = "--strict" in sys.argv
problems, warnings = [], []

PART_E = {"ch13.md", "ch14.md"}
MAX_TRACE, MAX_CHAPTER = 35, 14
BUDGETS = {  # words, fenced blocks excluded (see STYLE.md)
    "ch01.md": 2000, "ch02.md": 3600, "ch03.md": 3200, "ch04.md": 4200,
    "ch05.md": 2400, "ch06.md": 3000, "ch07.md": 3800, "ch08.md": 3000,
    "ch09.md": 2800, "ch10.md": 3200, "ch11.md": 2800, "ch12.md": 3400,
    "ch13.md": 3000, "ch14.md": 2600, "appendices.md": 4200,
}
TIER_RANGES = {  # (min, max) questions per tier
    "core": {"Tier 1": (3, 4), "Tier 2": (3, 4), "Tier 3": (2, 3)},
    "part_e": {"Tier 2": (3, 4), "Tier 3": (2, 3), "Tier 4": (2, 3)},
}

LEVEL_TAG_RE = re.compile(r"\[L[123]\]")
LEVEL_OK_RE = re.compile(r"(^Level emphasis:|^> .*\*\*Lab \d+|^#{1,3} .*\(\d+ points?\)|^#{1,3} Section)")
Q_RE = re.compile(r"^\*\*Q (\d+)\.(\d+) — .+[?.]\*\*")
TRACE_RE = re.compile(r"^### Trace (\d+): (What happens when .+)$")
FIG_DEF_RE = re.compile(r"^\*Figure (\d+)\.(\d+) — ")
LAB_CALLOUT_RE = re.compile(r"^> \*\*Lab (\d+) — (.+?)\.\*\* `(labs/[^`]+)/?`")
EXAM_Q_RE = re.compile(r"^\*\*E(\d)\.([A-Z])(\d+) \((\d+) pts\) — .+\*\*")
EXAM_SECTION_RE = re.compile(r"^## Section ([A-Z]) — .+ \((\d+) points\)")
CHECKS_LINE_RE = re.compile(r"Scored by pytest: (\d+) checks × (\d+) points")


def fenced_stripped(text):
    out, fence = [], False
    for line in text.split("\n"):
        if line.startswith("```"):
            fence = not fence
            continue
        if not fence:
            out.append(line)
    return "\n".join(out)


def check_chapter(path):
    fn = os.path.basename(path)
    text = open(path).read()
    body = fenced_stripped(text)
    lines = body.split("\n")

    if not text.startswith("# "):
        problems.append(f"{fn}: must start with '# Chapter N — Title' on line 1")
    if fn != "appendices.md":
        for sec in ("## Why this chapter", "## Questions", "## Common mistakes & red flags"):
            if sec not in body:
                problems.append(f"{fn}: missing required section '{sec}'")
        if fn not in PART_E and "### In other stacks" not in body:
            problems.append(f"{fn}: missing mandatory '### In other stacks' box")

    # question numbering + tier counts
    ch_num = int(fn[2:4]) if re.match(r"ch\d\d\.md", fn) else None
    if ch_num:
        tiers = TIER_RANGES["part_e" if fn in PART_E else "core"]
        tier, counts, last_m = None, {}, 0
        for line in lines:
            th = re.match(r"^### Tier (\d) — ", line)
            if th:
                tier = f"Tier {th.group(1)}"
                continue
            q = Q_RE.match(line)
            if q:
                n, m = int(q.group(1)), int(q.group(2))
                if n != ch_num:
                    problems.append(f"{fn}: question Q {n}.{m} has wrong chapter number")
                if m != last_m + 1:
                    problems.append(f"{fn}: question Q {n}.{m} breaks continuity (expected .{last_m + 1})")
                last_m = m
                if tier:
                    counts[tier] = counts.get(tier, 0) + 1
        for tname, (lo, hi) in tiers.items():
            got = counts.get(tname, 0)
            if not lo <= got <= hi:
                problems.append(f"{fn}: {tname} has {got} questions, contract says {lo}–{hi}")
        for tname in counts:
            if tname not in tiers:
                problems.append(f"{fn}: unexpected question tier '{tname}'")

    # level tags only in permitted positions
    for line in lines:
        if LEVEL_TAG_RE.search(line) and not LEVEL_OK_RE.search(line):
            problems.append(f"{fn}: level tag outside permitted positions: {line.strip()[:70]}")

    # word budget
    words = len(body.split())
    budget = BUDGETS.get(fn)
    if budget and words > budget * 1.1:
        msg = f"{fn}: {words} words, budget ~{budget} (+10% allowance)"
        (problems if STRICT else warnings).append(msg)

    # figures defined here (chapter prefix must match)
    figs = set()
    for line in text.split("\n"):
        fd = FIG_DEF_RE.match(line)
        if fd:
            figs.add((int(fd.group(1)), int(fd.group(2))))
            if ch_num and int(fd.group(1)) != ch_num:
                problems.append(f"{fn}: Figure {fd.group(1)}.{fd.group(2)} has wrong chapter prefix")
    return body, figs


def check_traces(chapter_bodies):
    planned = {}
    for line in open(os.path.join(ROOT, "TRACES.md")).read().split("\n"):
        m = re.match(r"^(\d+)\. \[?(What happens when [^\]·]+?)(?:\]\([^)]*\))?( · L\d.*)?$", line)
        if m:
            planned[int(m.group(1))] = m.group(2).strip()
    if len(planned) != MAX_TRACE:
        problems.append(f"TRACES.md: expected {MAX_TRACE} traces, found {len(planned)}")
    seen = {}
    for fn, body in chapter_bodies.items():
        for line in body.split("\n"):
            t = TRACE_RE.match(line)
            if not t:
                continue
            num, title = int(t.group(1)), t.group(2).strip()
            if num in seen:
                problems.append(f"{fn}: Trace {num} already defined in {seen[num]}")
            seen[num] = fn
            if num not in planned:
                problems.append(f"{fn}: Trace {num} is not in TRACES.md")
            elif planned[num].lower() != title.lower():
                warnings.append(f"{fn}: Trace {num} title differs from TRACES.md")
    return seen


def check_cross_refs(chapter_bodies, defined_traces, all_figs):
    for fn, body in chapter_bodies.items():
        for m in re.finditer(r"\bTrace (\d+)\b", body):
            n = int(m.group(1))
            if not 1 <= n <= MAX_TRACE:
                problems.append(f"{fn}: reference to nonexistent Trace {n}")
            elif defined_traces and n not in defined_traces:
                warnings.append(f"{fn}: reference to Trace {n}, not yet written")
        for m in re.finditer(r"\bFigure (\d+)\.(\d+)\b", body):
            if (int(m.group(1)), int(m.group(2))) not in all_figs:
                problems.append(f"{fn}: reference to nonexistent Figure {m.group(1)}.{m.group(2)}")
        for m in re.finditer(r"\bChapter (\d+)\b", body):
            if not 1 <= int(m.group(1)) <= MAX_CHAPTER:
                problems.append(f"{fn}: reference to nonexistent Chapter {m.group(1)}")


def check_labs(chapter_texts):
    callouts = {}
    for fn, text in chapter_texts.items():
        for line in text.split("\n"):
            if re.match(r"^> \*\*Lab ", line):
                c = LAB_CALLOUT_RE.match(line)
                if not c:
                    problems.append(f"{fn}: malformed lab callout: {line.strip()[:70]}")
                    continue
                num, _, d = int(c.group(1)), c.group(2), c.group(3).rstrip("/")
                if num in callouts:
                    problems.append(f"{fn}: Lab {num} referenced more than once (also in {callouts[num][0]})")
                callouts[num] = (fn, d)
                if not os.path.isdir(os.path.join(ROOT, d)):
                    problems.append(f"{fn}: lab callout points at missing dir {d}")
    for d in sorted(glob.glob(os.path.join(ROOT, "labs", "lab[0-9]*"))):
        num = int(re.match(r"lab(\d+)", os.path.basename(d)).group(1))
        if num not in callouts:
            problems.append(f"labs/{os.path.basename(d)}: not referenced from any chapter callout")


def check_strip(all_texts):
    for fn, text in all_texts.items():
        stripped = strip_answers(text)
        for pat in ALL_MARKERS:
            if re.search(pat.replace("^", r"(?m)^"), stripped):
                problems.append(f"{fn}: candidate strip left marker {pat} behind")
        want_q = [l for l in text.split("\n") if Q_RE.match(l) or EXAM_Q_RE.match(l)]
        have_q = [l for l in stripped.split("\n") if Q_RE.match(l) or EXAM_Q_RE.match(l)]
        if want_q != have_q:
            problems.append(f"{fn}: candidate strip lost question prompts ({len(want_q)} -> {len(have_q)})")
        for l in stripped.split("\n"):
            if WHATS_WRONG_RE.match(l):
                break


def check_exams():
    for level_dir in sorted(glob.glob(os.path.join(ROOT, "exams", "l[0-9]"))):
        lvl = os.path.basename(level_dir)
        exam_p, key_p = os.path.join(level_dir, "exam.md"), os.path.join(level_dir, "key.md")
        if not os.path.exists(exam_p):
            problems.append(f"exams/{lvl}: missing exam.md")
            continue
        exam = open(exam_p).read()
        if not exam.startswith("# "):
            problems.append(f"exams/{lvl}/exam.md: must start with '# Title' on line 1")
        total_m = re.search(r"\*\*Total:\*\* (\d+) points", exam)
        if not total_m:
            problems.append(f"exams/{lvl}/exam.md: missing '**Total:** N points' declaration")
        if "**Pass:**" not in exam:
            problems.append(f"exams/{lvl}/exam.md: missing '**Pass:**' bar")
        if "key.md" in exam:
            pass  # repo-path references to the key are fine in exam.md headers
        section, sec_declared, sec_sum, grand = None, {}, {}, 0
        for line in exam.split("\n"):
            s = EXAM_SECTION_RE.match(line)
            if s:
                section = s.group(1)
                sec_declared[section] = int(s.group(2))
                sec_sum.setdefault(section, 0)
                continue
            q = EXAM_Q_RE.match(line)
            if q:
                if section is None:
                    problems.append(f"exams/{lvl}/exam.md: question {line[:20]} outside any section")
                    continue
                if q.group(2) != section:
                    problems.append(f"exams/{lvl}/exam.md: E{q.group(1)}.{q.group(2)}{q.group(3)} in Section {section}")
                sec_sum[section] += int(q.group(4))
            c = CHECKS_LINE_RE.search(line)
            if c and section:
                sec_sum[section] += int(c.group(1)) * int(c.group(2))
        for sec, declared in sec_declared.items():
            if sec_sum.get(sec, 0) != declared:
                problems.append(f"exams/{lvl}/exam.md: Section {sec} sums to {sec_sum.get(sec, 0)}, declares {declared}")
            grand += declared
        if total_m and grand != int(total_m.group(1)):
            problems.append(f"exams/{lvl}/exam.md: sections sum to {grand}, total declares {total_m.group(1)}")
        # key parity
        if os.path.exists(key_p):
            key = open(key_p).read()
            exam_ids = set(re.findall(r"\*\*E(\d\.[A-Z]\d+)", exam))
            key_ids = set(re.findall(r"\*\*E(\d\.[A-Z]\d+)", key))
            for missing in sorted(exam_ids - key_ids):
                problems.append(f"exams/{lvl}/key.md: no entry for E{missing}")
            for extra in sorted(key_ids - exam_ids):
                problems.append(f"exams/{lvl}/key.md: entry E{extra} not in exam.md")
        else:
            problems.append(f"exams/{lvl}: missing key.md")
        # practical points vs test count, when a practical exists
        tests = glob.glob(os.path.join(level_dir, "practical", "tests", "test_*.py"))
        if tests:
            n_tests = sum(len(re.findall(r"^def test_", open(t).read(), re.M)) for t in tests)
            m = CHECKS_LINE_RE.search(exam)
            if m and int(m.group(1)) != n_tests:
                problems.append(f"exams/{lvl}: exam declares {m.group(1)} checks, practical has {n_tests} tests")
        # key must never be rendered
        exam_rel_refs = re.findall(r"key\.md", exam)
        if len(exam_rel_refs) > 1:
            warnings.append(f"exams/{lvl}/exam.md: multiple key.md mentions — keep it to the header pointer")


def check_appendix_toc():
    p = os.path.join(ROOT, "chapters", "appendices.md")
    if not os.path.exists(p):
        return
    heads = re.findall(r"^## (Appendix ([A-Z]))", open(p).read(), re.M)
    for full, letter in heads:
        if letter not in "ABCDEF":
            problems.append(f"appendices.md: '{full}' is outside the A–F range build.py indexes")


def main():
    chapter_paths = sorted(glob.glob(os.path.join(ROOT, "chapters", "*.md")))
    chapter_texts, chapter_bodies, all_figs = {}, {}, set()
    for p in chapter_paths:
        fn = os.path.basename(p)
        chapter_texts[fn] = open(p).read()
        body, figs = check_chapter(p)
        chapter_bodies[fn] = body
        all_figs |= figs
    defined = check_traces(chapter_bodies)
    check_cross_refs(chapter_bodies, defined, all_figs)
    check_labs(chapter_texts)
    exam_texts = {f"exams/{os.path.basename(os.path.dirname(p))}/exam.md": open(p).read()
                  for p in glob.glob(os.path.join(ROOT, "exams", "l[0-9]", "exam.md"))}
    check_strip({**chapter_texts, **exam_texts})
    check_exams()
    check_appendix_toc()

    for w in warnings:
        print(f"WARN  {w}")
    for e in problems:
        print(f"FAIL  {e}")
    print(f"==== {'FAIL' if problems else 'PASS'}: {len(problems)} problem(s), {len(warnings)} warning(s) ====")
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
