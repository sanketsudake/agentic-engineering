#!/usr/bin/env python3
"""Check every mermaid diagram against the size gate in STYLE.md.

    python3 build/check_diagrams.py chapters/ch04.md
    python3 build/check_diagrams.py chapters/*.md

Two things are verified.

1. Size. The page gives a diagram 174mm of width (A4 minus 18mm margins) and
   150mm of height, so the image is scaled by min(174/W, 150/H). A diagram that
   is too tall shrinks exactly like one that is too wide. Mermaid's label font
   is ~16px and print needs at least 7pt, so the gate is the resulting "pt"
   column -- the size a label actually prints at. Roughly, that means staying
   under ~1100px wide or ~960px tall, whichever binds first.

2. Caption coupling. build.py pairs a diagram with its caption using a regex
   that allows only whitespace between the closing fence and the *Figure ...*
   line. If that pairing breaks, the build still exits 0 and raw mermaid source
   lands in the PDF. Counting fences and captions is not enough to catch it --
   prose inserted between the two keeps the counts equal while the match is
   lost -- so this compares fences, captions, and actual regex matches.

Needs mmdc (npm install -g @mermaid-js/mermaid-cli). Set CHROME_PATH if
mermaid cannot find a browser.
"""
import hashlib
import os
import re
import shutil
import subprocess
import sys
import tempfile

# The gate is the size a label actually prints at, not the raw pixel box.
# W/H limits alone are a proxy: a 1050px-wide diagram that is also short still
# prints at ~7.5pt and reads fine, while a narrow but very tall one does not.
MIN_PT = 7.0
TEXT_MM, HEIGHT_MM = 174.0, 150.0
FONT_PX = 16

# Must stay in step with MMD_RE in build.py.
MMD_RE = re.compile(r"```mermaid\n(.*?)```\s*\n\s*(\*Figure[^\n]*\*)", re.S)
FENCE_RE = re.compile(r"^```mermaid$", re.M)
FIG_RE = re.compile(r"^\*Figure[^\n]*\*$", re.M)
HTML_RE = re.compile(r"<[a-zA-Z/]")
# Sequence diagrams emit negative offsets: viewBox="-56 -10 725.5 708".
VIEWBOX_RE = re.compile(r'viewBox="-?[\d.]+ -?[\d.]+ ([\d.]+) ([\d.]+)"')

CACHE = os.path.join(tempfile.gettempdir(), "k8s-worksheet-diagram-check")
# Same layout config build.py renders with, so this measures what gets built.
MERMAID_CFG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mermaid-config.json")


def _puppeteer_config():
    cfg = os.path.join(CACHE, "puppeteer.json")
    chrome = os.environ.get("CHROME_PATH")
    args = '"args":["--no-sandbox"]'
    body = "{%s,\"executablePath\":\"%s\"}" % (args, chrome) if chrome else "{%s}" % args
    with open(cfg, "w") as f:
        f.write(body)
    return cfg


def measure(code, pptr):
    """Render one diagram and return ((width, height), None) or (None, error)."""
    stamp = hashlib.md5(open(MERMAID_CFG, "rb").read()).hexdigest()[:6]
    digest = hashlib.md5((code + stamp).encode()).hexdigest()[:12]
    svg = os.path.join(CACHE, digest + ".svg")
    if not os.path.exists(svg):
        src = os.path.join(CACHE, digest + ".mmd")
        with open(src, "w") as f:
            f.write(code)
        r = subprocess.run(["mmdc", "-i", src, "-o", svg, "-p", pptr,
                            "-c", MERMAID_CFG, "--quiet"],
                           capture_output=True, text=True)
        if r.returncode != 0 or not os.path.exists(svg):
            return None, (r.stderr or "render failed").strip()[-200:]
    m = VIEWBOX_RE.search(open(svg).read())
    if not m:
        return None, "no viewBox in SVG"
    return (float(m.group(1)), float(m.group(2))), None


def check(path, pptr):
    """Check one markdown file. Returns the number of problems found."""
    text = open(path).read()
    fences, figures = len(FENCE_RE.findall(text)), len(FIG_RE.findall(text))
    pairs = MMD_RE.findall(text)
    problems = 0

    if not (fences == figures == len(pairs)):
        print(f"\n=== {path}")
        print(f"  CAPTION PAIRING BROKEN: {fences} fences, {figures} captions, "
              f"{len(pairs)} matched by build.py")
        print("  -> a diagram will render as raw source in the PDF, with no build error")
        return 1
    if not pairs:
        return 0

    print(f"\n=== {path} ({len(pairs)} diagrams)")
    for i, (code, caption) in enumerate(pairs, 1):
        kind = code.strip().split("\n")[0][:17]
        dims, err = measure(code, pptr)
        if dims is None:
            print(f"  {i:2d}. RENDER FAIL  {kind:<17} {err}")
            problems += 1
            continue
        w, h = dims
        pt = FONT_PX * min(TEXT_MM / w, HEIGHT_MM / h) * 72 / 25.4
        flags = []
        if pt < MIN_PT:
            # say which dimension is the binding one, so the fix is obvious
            flags.append("TOO WIDE" if TEXT_MM / w < HEIGHT_MM / h else "TOO TALL")
        if HTML_RE.search(code):
            flags.append("HTML-IN-LABEL")
        if flags:
            problems += 1
        print(f"  {i:2d}. {','.join(flags) or 'ok':<14} w={w:7.1f} h={h:6.1f} "
              f"{pt:4.1f}pt  {kind:<17} {caption[:38]}")
    return problems


def main(paths):
    if not shutil.which("mmdc"):
        print("mmdc not found: npm install -g @mermaid-js/mermaid-cli", file=sys.stderr)
        return 2
    os.makedirs(CACHE, exist_ok=True)
    pptr = _puppeteer_config()
    total = sum(check(p, pptr) for p in paths)
    print(f"\n==== {'FAIL' if total else 'PASS'}: {total} problem(s); "
          f"gate is {MIN_PT}pt minimum label size in print ====")
    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:] or ["chapters/ch01.md"]))
