"""
Wrap assets/portrait.txt (a hand-picked ASCII-art portrait) into an SVG with a
continuous scan-line sweep moving left -> right, plus a one-time type-in.

Edit portrait.txt, then:  python assets/portrait.py   ->  writes assets/self.svg
Base text sits at full opacity so the portrait stays readable even where the host
does not run animations (GitHub bakes SVGs at t=0).
"""
import os, html

HERE = os.path.dirname(__file__)
SRC = os.path.join(HERE, "portrait.txt")
OUT = os.path.join(HERE, "portrait-scan.svg")

CHAR_W, CHAR_H = 7.1, 12.4
DIM, BRIGHT, ACCENT, BG = "#8b9096", "#eef0f2", "#ff6b6b", "#0d1117"
FONT = "ui-monospace, 'SF Mono', 'JetBrains Mono', Consolas, monospace"
TYPE_SECONDS = 2.2
SCAN_SECONDS = 3.6

lines = [l.rstrip("\n") for l in open(SRC, encoding="utf-8").read().split("\n")]
while lines and not lines[-1].strip():
    lines.pop()

cols = max((len(l) for l in lines), default=1)
rows = len(lines)
W, H = cols * CHAR_W, rows * CHAR_H
per = TYPE_SECONDS / max(rows, 1)
band = W * 0.22

tspans = "".join(
    f'<text x="0" y="{(i + 0.85) * CHAR_H:.1f}" style="animation-delay:{i * per:.3f}s">'
    f'{html.escape(ln) or " "}</text>'
    for i, ln in enumerate(lines)
)

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W:.0f} {H:.0f}" width="{W:.0f}" height="{H:.0f}" font-family="{FONT}" font-size="{CHAR_H*0.92:.1f}" xml:space="preserve">
<defs>
<linearGradient id="sw" x1="0" y1="0" x2="1" y2="0">
<stop offset="0" stop-color="{ACCENT}" stop-opacity="0"/>
<stop offset="0.5" stop-color="{ACCENT}" stop-opacity="0.9"/>
<stop offset="1" stop-color="{ACCENT}" stop-opacity="0"/>
</linearGradient>
<clipPath id="clip"><rect x="{-band:.0f}" y="0" width="{band:.0f}" height="{H:.0f}">
<animate attributeName="x" from="{-band:.0f}" to="{W:.0f}" dur="{SCAN_SECONDS}s" repeatCount="indefinite"/>
</rect></clipPath>
</defs>
<style>
text{{fill:{DIM};white-space:pre;animation:tp .3s ease forwards}}
@keyframes tp{{0%{{opacity:0}}100%{{opacity:1}}}}
.hi text{{fill:{BRIGHT};animation:none;opacity:1}}
</style>
<rect width="100%" height="100%" fill="{BG}"/>
<g>{tspans}</g>
<g class="hi" clip-path="url(#clip)">{tspans}</g>
<rect x="{-band:.0f}" y="0" width="{band:.0f}" height="{H:.0f}" fill="url(#sw)" opacity="0.3">
<animate attributeName="x" from="{-band:.0f}" to="{W:.0f}" dur="{SCAN_SECONDS}s" repeatCount="indefinite"/>
</rect>
</svg>'''

open(OUT, "w", encoding="utf-8").write(svg)
print("wrote", OUT, round(os.path.getsize(OUT) / 1024, 1), "KB  ", cols, "x", rows)
