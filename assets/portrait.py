"""
Turn assets/portrait-src.png (a background-removed headshot) into an ASCII
portrait SVG that gently "breathes" — a slow scale + opacity pulse.

    python assets/portrait.py   ->  writes assets/self.svg

Pipeline (approximates the ASCII-Portrait-README-Guide): alpha mask -> grayscale
-> local-contrast (unsharp) -> darkening curve v^1.6 -> map to a deep ramp.
"""
import os, html
import numpy as np
from PIL import Image, ImageOps, ImageFilter

HERE = os.path.dirname(__file__)
SRC = os.path.join(HERE, "portrait-src.png")
OUT = os.path.join(HERE, "breathe.svg")

COLS = 108
CHAR_W, CHAR_H = 7.1, 12.4
CROPF = (0.02, 0.0, 0.99, 0.90)          # x0,y0,x1,y1 as fractions
GAMMA = 1.55                             # >1 darkens mids -> more depth
LOCAL = 1.15                             # unsharp amount (local contrast)
# light -> dark; leading space clears the background
RAMP = " .'`^\":;~-_+<>i!lI?][}{1)(|/tfjrxnuvczmwXYUJCLQ0OZbdpqkhao*#MW&8%B@$"

FG, BG = "#c9d1d9", "#0d1117"
FONT = "ui-monospace, 'SF Mono', 'JetBrains Mono', Consolas, monospace"


def build_lines():
    im = Image.open(SRC).convert("RGBA")
    W, H = im.size
    im = im.crop((int(CROPF[0] * W), int(CROPF[1] * H), int(CROPF[2] * W), int(CROPF[3] * H)))
    alpha = im.split()[3]

    SS = 4
    tw = COLS * SS
    thh = round(tw * (im.height / im.width) * (CHAR_W / CHAR_H))
    g = ImageOps.autocontrast(im.convert("L"), cutoff=1).resize((tw, thh), Image.LANCZOS)
    m = np.asarray(alpha.resize((tw, thh), Image.LANCZOS), np.float32) / 255.0
    gv = np.asarray(g, np.float32) / 255.0

    # local contrast: pull detail out of a flatly-lit face
    blur = np.asarray(g.filter(ImageFilter.GaussianBlur(tw * 0.06)), np.float32) / 255.0
    t = np.clip(gv + LOCAL * (gv - blur), 0, 1)

    # normalise to the subject's own range, then darken mids
    sub = m > 0.4
    lo, hi = np.percentile(t[sub], [2, 98])
    t = np.clip((t - lo) / (hi - lo + 1e-6), 0, 1) ** GAMMA

    n = len(RAMP) - 1
    rows = round(thh / SS)
    tt = np.asarray(Image.fromarray((t * 255).astype(np.uint8)).resize((COLS, rows), Image.BOX)) / 255.0
    mm = np.asarray(Image.fromarray((m * 255).astype(np.uint8)).resize((COLS, rows), Image.BOX)) / 255.0

    lines = []
    for r in range(rows):
        row = "".join(
            RAMP[min(n, max(0, round(tt[r, c] * n)))] if mm[r, c] > 0.33 else " "
            for c in range(COLS)
        )
        lines.append(row.rstrip())
    while lines and not lines[0].strip():
        lines.pop(0)
    while lines and not lines[-1].strip():
        lines.pop()
    return lines


def main():
    lines = build_lines()
    cols = max((len(l) for l in lines), default=1)
    rows = len(lines)
    W, H = cols * CHAR_W, rows * CHAR_H
    dx, dy = -W * 0.011, -H * 0.011

    tspans = "".join(
        f'<text x="0" y="{(i + 0.85) * CHAR_H:.1f}">{html.escape(ln) or " "}</text>'
        for i, ln in enumerate(lines)
    )
    # breathing: scale + a counter-translate so it pulses about the centre,
    # plus a faint brightness swell. Pure SMIL — GitHub runs it.
    breath = (
        f'<animateTransform attributeName="transform" type="translate" additive="sum" '
        f'dur="4.8s" repeatCount="indefinite" calcMode="spline" keyTimes="0;0.5;1" '
        f'keySplines=".45 0 .55 1;.45 0 .55 1" values="0 0;{dx:.1f} {dy:.1f};0 0"/>'
        f'<animateTransform attributeName="transform" type="scale" additive="sum" '
        f'dur="4.8s" repeatCount="indefinite" calcMode="spline" keyTimes="0;0.5;1" '
        f'keySplines=".45 0 .55 1;.45 0 .55 1" values="1;1.022;1"/>'
        f'<animate attributeName="opacity" dur="4.8s" repeatCount="indefinite" '
        f'calcMode="spline" keyTimes="0;0.5;1" keySplines=".45 0 .55 1;.45 0 .55 1" '
        f'values="1;0.86;1"/>'
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

    # preview png
    from PIL import ImageDraw, ImageFont
    cw, ch = 8, 15
    pim = Image.new("RGB", (cols * cw or 8, rows * ch), (13, 17, 23))
    pd = ImageDraw.Draw(pim)
    try:
        pf = ImageFont.truetype(r"C:/Windows/Fonts/consola.ttf", 14)
    except Exception:
        pf = ImageFont.load_default()
    for i, l in enumerate(lines):
        pd.text((0, i * ch), l, font=pf, fill=(201, 209, 217))
    pim.save(os.path.join(HERE, "_portrait_preview.png"))


if __name__ == "__main__":
    main()
