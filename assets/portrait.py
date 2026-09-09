"""
Wrap assets/portrait.txt (a hand-picked ASCII-art portrait) into an animated
monochrome SVG that types itself in line by line.

Edit portrait.txt, then:  python assets/portrait.py   ->  writes assets/self.svg
The SVG stays visible even where the host doesn't run animations (GitHub bakes
SVGs at t=0): base opacity is 1, the CSS animation only adds the type-in.
"""
import os, html

HERE = os.path.dirname(__file__)
SRC = os.path.join(HERE, "portrait.txt")
OUT = os.path.join(HERE, "self.svg")

CHAR_W, CHAR_H = 7.1, 12.4
FG, BG = "#c9d1d9", "#0d1117"
FONT = "ui-monospace, 'SF Mono', 'JetBrains Mono', Consolas, monospace"
TYPE_SECONDS = 2.4

lines = [l.rstrip("\n") for l in open(SRC, encoding="utf-8").read().split("\n")]
while lines and not lines[-1].strip():
    lines.pop()

cols = max((len(l) for l in lines), default=1)
rows = len(lines)
W, H = cols * CHAR_W, rows * CHAR_H
per = TYPE_SECONDS / max(rows, 1)

tspans = "".join(
    f'<text x="0" y="{(i + 0.85) * CHAR_H:.1f}" style="animation-delay:{i * per:.3f}s">'
    f'{html.escape(ln) or " "}</text>'
    for i, ln in enumerate(lines)
)
svg = (
    f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W:.0f} {H:.0f}" '
    f'width="{W:.0f}" height="{H:.0f}" font-family="{FONT}" '
    f'font-size="{CHAR_H * 0.92:.1f}" xml:space="preserve">'
    f'<style>text{{fill:{FG};white-space:pre;animation:tp .3s ease forwards}}'
    f'@keyframes tp{{0%{{opacity:0}}100%{{opacity:1}}}}</style>'
    f'<rect width="100%" height="100%" fill="{BG}"/>{tspans}</svg>'
)
open(OUT, "w", encoding="utf-8").write(svg)
print("wrote", OUT, round(os.path.getsize(OUT) / 1024, 1), "KB  ", cols, "x", rows)
