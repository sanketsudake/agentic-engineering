#!/usr/bin/env python3
"""Build the Agentic Engineering Worksheet PDF.

Usage:  python3 build/build.py                 # full edition
        STRIP_ANSWERS=1 python3 build/build.py # candidate edition (answers removed)
Output: dist/agentic-engineering-worksheet.pdf
        dist/agentic-engineering-worksheet-candidate.pdf

Requires: python packages in requirements.txt, mermaid-cli (mmdc) on PATH,
and a Chromium/Chrome for mermaid rendering (set CHROME_PATH to point at a
specific binary; otherwise mermaid-cli uses its own bundled browser).
"""
import hashlib, json, os, re, shutil, subprocess, sys
import markdown

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # repo root
CH = os.path.join(ROOT, "chapters")
DIST = os.path.join(ROOT, "dist")
DIA = os.path.join(DIST, "diagrams")
os.makedirs(DIA, exist_ok=True)

# The spine unit. "Trace N: What happens when <event>" headings are detected,
# indexed on the TOC page, and given stable anchors.
SPINE_LABEL = "Trace"
BOOK_SLUG = "agentic-engineering-worksheet"
STRIP = os.environ.get("STRIP_ANSWERS") == "1"

PARTS = [
    ("Part A — Foundations", ["ch01.md"]),
    ("Appendices", ["appendices.md"]),
    ("Assessment", ["../exams/l1/exam.md", "../exams/l2/exam.md", "../exams/l3/exam.md"]),
]

# ---- puppeteer config for mermaid-cli ----
PPTR = os.path.join(DIST, "puppeteer.json")
pptr_cfg = {"args": ["--no-sandbox"]}
chrome = os.environ.get("CHROME_PATH") or (
    "/opt/pw-browsers/chromium" if os.path.exists("/opt/pw-browsers/chromium") else shutil.which("chromium") or shutil.which("google-chrome"))
if chrome:
    pptr_cfg["executablePath"] = chrome
with open(PPTR, "w") as f:
    json.dump(pptr_cfg, f)

MMD_RE = re.compile(r"```mermaid\n(.*?)```\s*\n\s*(\*Figure[^\n]*\*)", re.S)

# Layout config, shared with build/check_diagrams.py so the size the gate
# measures is the size that actually gets built. Mermaid's default 150px actor
# box and 50px margin put a hard floor under sequence-diagram width -- roughly
# 1450px at 7 participants -- which shrinks labels below readable size on A4.
MERMAID_CFG = os.path.join(BUILD_DIR := os.path.dirname(os.path.abspath(__file__)),
                           "mermaid-config.json")
CFG_STAMP = hashlib.md5(open(MERMAID_CFG, "rb").read()).hexdigest()[:6]

def render_mermaid(code: str) -> str:
    # Cache key includes the config: change the layout and every diagram must
    # re-render, otherwise stale PNGs from the old layout survive.
    h = hashlib.md5((code + CFG_STAMP).encode()).hexdigest()[:12]
    png = os.path.join(DIA, f"{h}.png")
    if not os.path.exists(png):
        src = os.path.join(DIA, f"{h}.mmd")
        with open(src, "w") as f:
            f.write(code)
        r = subprocess.run(
            ["mmdc", "-i", src, "-o", png, "-b", "white", "-s", "3", "-w", "1000",
             "-p", PPTR, "-c", MERMAID_CFG, "--quiet"],
            capture_output=True, text=True)
        if r.returncode != 0 or not os.path.exists(png):
            print(f"MERMAID FAIL {h}: {r.stderr[-600:]}", file=sys.stderr)
            return None
    return png

fail = []

def replace_mermaid(md_text: str) -> str:
    def sub(m):
        code, caption = m.group(1), m.group(2)
        png = render_mermaid(code)
        cap_html = caption.strip("*")
        if png is None:
            fail.append(cap_html)
            return f"\n<p><em>[diagram failed]</em> {cap_html}</p>\n"
        return (f'\n<figure class="diagram"><img src="file://{png}"/>'
                f"<figcaption>{cap_html}</figcaption></figure>\n")
    return MMD_RE.sub(sub, md_text)

# ---- candidate edition: strip model answers (see build/strip.py) ----
sys.path.insert(0, BUILD_DIR)
from strip import strip_answers

def md2html(text: str) -> str:
    return markdown.markdown(text, extensions=["tables", "fenced_code", "sane_lists", "smarty"])

def slug(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")

# ---- process chapters ----
toc_entries = []    # (level, title, anchor)
trace_entries = []  # (num, title, anchor)
lab_entries = []    # (num, title, anchor)
body_parts = []

for part_title, files in PARTS:
    part_anchor = "part-" + slug(part_title.split("—")[0])
    if not part_title.startswith("Appendices"):
        toc_entries.append((0, part_title, part_anchor))
        body_parts.append(f'<div class="part-page" id="{part_anchor}"><h1 class="part-title">{part_title}</h1></div>')
    for fn in files:
        text = open(os.path.join(CH, fn)).read()
        if STRIP:
            text = strip_answers(text)
        text = replace_mermaid(text)
        m = re.match(r"# (.+)", text)
        title = m.group(1).strip()
        anchor = slug(title.split("—")[0].strip())
        text = text[m.end():]
        def trace_sub(mm):
            num, rest = mm.group(1), mm.group(2)
            ta = f"{SPINE_LABEL.lower()}-{num}"
            trace_entries.append((int(num), rest.strip(), ta))
            return f'<h3 class="flow" id="{ta}">{SPINE_LABEL} {num}: {rest.strip()}</h3>'
        html = md2html(text)
        html = re.sub(rf"<h3>{SPINE_LABEL} (\d+): (.*?)</h3>", trace_sub, html)
        # level badges: [L1] [L2] [L3] anywhere in rendered prose
        html = re.sub(r"\[L([123])\]", r'<span class="level l\1">L\1</span>', html)
        # lab callouts: blockquote whose first strong text is "Lab N — title."
        def lab_sub(mm):
            num, lab_title, rest = mm.group(1), mm.group(2), mm.group(3)
            la = f"lab-{num}"
            lab_entries.append((int(num), lab_title.strip(), la))
            return (f'<aside class="lab" id="{la}"><p><strong>Lab {num} — '
                    f"{lab_title.strip()}.</strong>{rest}</p></aside>")
        html = re.sub(
            r"<blockquote>\s*<p><strong>Lab (\d+) (?:—|&mdash;) (.*?)\.</strong>(.*?)</p>\s*</blockquote>",
            lab_sub, html, flags=re.S)
        if fn == "appendices.md":
            html = re.sub(r"<h2>(Appendix [A-F][^<]*)</h2>",
                          lambda mm: f'<h2 class="chapter-title appendix" id="{slug(mm.group(1)[:10])}">{mm.group(1)}</h2>', html)
            for mm in re.finditer(r'id="(appendix-[a-f])">([^<]+)<', html):
                toc_entries.append((0, mm.group(2), mm.group(1)))
            body_parts.append(f'<section class="chapter">{html}</section>')
        else:
            toc_entries.append((1, title, anchor))
            body_parts.append(
                f'<section class="chapter"><h2 class="chapter-title" id="{anchor}" '
                f'data-title="{title.split("—")[1].strip() if "—" in title else title}">{title}</h2>{html}</section>')

# ---- TOC + trace index + labs index ----
toc_html = ['<div class="toc-page"><h2 class="toc-h">Contents</h2><ul class="toc">']
for level, title, anchor in toc_entries:
    cls = "toc-part" if level == 0 else "toc-ch"
    toc_html.append(f'<li class="{cls}"><a href="#{anchor}"><span class="t">{title}</span><span class="pg"></span></a></li>')
toc_html.append("</ul>")
toc_html.append(f'<h2 class="toc-h">The {len(trace_entries)} {SPINE_LABEL.lower()}s</h2><ul class="toc flows">')
for num, title, anchor in sorted(trace_entries):
    toc_html.append(f'<li class="toc-flow"><a href="#{anchor}"><span class="t"><b>{num}.</b> {title}</span><span class="pg"></span></a></li>')
toc_html.append("</ul>")
if lab_entries:
    toc_html.append(f'<h2 class="toc-h">The {len(lab_entries)} labs</h2><ul class="toc flows">')
    for num, title, anchor in sorted(lab_entries):
        toc_html.append(f'<li class="toc-flow"><a href="#{anchor}"><span class="t"><b>{num}.</b> {title}</span><span class="pg"></span></a></li>')
    toc_html.append("</ul>")
toc_html.append("</div>")

BUILD = os.path.dirname(os.path.abspath(__file__))
css = open(os.path.join(BUILD, "style.css")).read()
cover = open(os.path.join(BUILD, "cover.html")).read()

doc = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>{css}</style></head><body>
{cover}
{''.join(toc_html)}
{''.join(body_parts)}
</body></html>"""

edition = "-candidate" if STRIP else ""
with open(os.path.join(DIST, f"worksheet{edition}.html"), "w") as f:
    f.write(doc)

if fail:
    print("FAILED DIAGRAMS:", fail, file=sys.stderr)
    sys.exit(1)

from weasyprint import HTML
out = os.path.join(DIST, f"{BOOK_SLUG}{edition}.pdf")
HTML(os.path.join(DIST, f"worksheet{edition}.html")).write_pdf(out)
print(f"PDF written: {out}")
