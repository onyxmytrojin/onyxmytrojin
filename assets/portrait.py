"""
Wrap assets/portrait.txt (a hand-picked ASCII-art portrait) into an SVG that
gently "breathes" — a slow scale + opacity pulse, centred. No sweep, no typing.

    python assets/portrait.py   ->  writes assets/breathe.svg

Base opacity is 1 so it stays visible even where the host does not run SMIL.
"""
import os, html

HERE = os.path.dirname(__file__)
SRC = os.path.join(HERE, "portrait.txt")
OUT = os.path.join(HERE, "breathe.svg")

CHAR_W, CHAR_H = 7.1, 12.4
FG, BG = "#c9d1d9", "#0d1117"
FONT = "ui-monospace, 'SF Mono', 'JetBrains Mono', Consolas, monospace"

lines = [l.rstrip("\n") for l in open(SRC, encoding="utf-8").read().split("\n")]
while lines and not lines[-1].strip():
    lines.pop()
while lines and not lines[0].strip():
    lines.pop(0)

cols = max((len(l) for l in lines), default=1)
rows = len(lines)
W, H = cols * CHAR_W, rows * CHAR_H
dx, dy = -W * 0.011, -H * 0.011

tspans = "".join(
    f'<text x="0" y="{(i + 0.85) * CHAR_H:.1f}">{html.escape(ln) or " "}</text>'
    for i, ln in enumerate(lines)
)
breath = (
    f'<animateTransform attributeName="transform" type="translate" additive="sum" '
    f'dur="5s" repeatCount="indefinite" calcMode="spline" keyTimes="0;0.5;1" '
    f'keySplines=".45 0 .55 1;.45 0 .55 1" values="0 0;{dx:.1f} {dy:.1f};0 0"/>'
    f'<animateTransform attributeName="transform" type="scale" additive="sum" '
    f'dur="5s" repeatCount="indefinite" calcMode="spline" keyTimes="0;0.5;1" '
    f'keySplines=".45 0 .55 1;.45 0 .55 1" values="1;1.02;1"/>'
    f'<animate attributeName="opacity" dur="5s" repeatCount="indefinite" '
    f'calcMode="spline" keyTimes="0;0.5;1" keySplines=".45 0 .55 1;.45 0 .55 1" '
    f'values="1;0.88;1"/>'
)
svg = (
    f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W:.0f} {H:.0f}" '
    f'width="{W:.0f}" height="{H:.0f}" font-family="{FONT}" '
    f'font-size="{CHAR_H * 0.92:.1f}" xml:space="preserve">'
    f'<rect width="100%" height="100%" fill="{BG}"/>'
    f'<g fill="{FG}">{breath}{tspans}</g></svg>'
)
with open(OUT, "w", encoding="utf-8", newline="\n") as f:
    f.write(svg)
print("wrote", OUT, round(os.path.getsize(OUT) / 1024, 1), "KB  ", cols, "x", rows)
