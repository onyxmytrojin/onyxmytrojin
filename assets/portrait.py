"""
ASCII-portrait -> animated monochrome SVG that types itself in.

The hard part is separating you from the background. This script does NOT do
that well on its own for busy natural backgrounds. Give it a clean cutout:

    pip install rembg pillow numpy
    rembg i your-headshot.jpg assets/_src.png     # -> transparent background

Then:  python assets/portrait.py
It uses the alpha channel as the subject mask. If _src.png has no alpha (or you
pass a .jpg), it falls back to using the whole frame — expect noise unless the
background is already plain.

Swap `shubhan.png` for `portrait.svg` in README.md once it looks right
(assets/_portrait_preview.png is written so you can check first).
"""
import os, html, glob, numpy as np
from PIL import Image, ImageEnhance, ImageOps, ImageFilter, ImageDraw, ImageFont

HERE = os.path.dirname(__file__)
SRC = next((p for p in (os.path.join(HERE, "portrait-src.png"),
                        os.path.join(HERE, "_src.png"), os.path.join(HERE, "_src.jpg"))
            if os.path.exists(p)), os.path.join(HERE, "portrait-src.png"))
OUT = os.path.join(HERE, "portrait.svg")
PREVIEW = os.path.join(HERE, "_portrait_preview.png")

COLS = 92
CHAR_W, CHAR_H = 7.4, 12.8
RAMP = " .·-:=+o*#%@"
FG, BG = "#c9d1d9", "#0d1117"
FONT = "ui-monospace, 'SF Mono', 'JetBrains Mono', Consolas, monospace"
TYPE_SECONDS = 2.4
CROPF = (0.15, 0.53, 0.72, 0.80)      # x0,y0,x1,y1 as fractions of the source

im = Image.open(SRC)
W, Hs = im.size
box = (int(CROPF[0] * W), int(CROPF[1] * Hs), int(CROPF[2] * W), int(CROPF[3] * Hs))
im = im.crop(box)

alpha = im.split()[3] if im.mode in ("RGBA", "LA") else None
g = ImageOps.autocontrast(im.convert("L"), cutoff=1)

SS = 4
tw = COLS * SS
thh = round(tw * (g.height / g.width) * (CHAR_W / CHAR_H))
g = g.resize((tw, thh), Image.LANCZOS)
gv = np.asarray(g, np.float32) / 255.0
H0, W0 = gv.shape

if alpha is not None:
    m = np.asarray(alpha.resize((W0, H0), Image.LANCZOS), np.float32) / 255.0
else:
    m = np.ones_like(gv)

# local contrast for feature detail, then S-curve
lp = np.asarray(g.filter(ImageFilter.GaussianBlur(W0 * 0.17)), np.float32) / 255.0
tone = np.clip(0.62 * gv + 0.62 * (gv - lp) + 0.14, 0, 1)
tone = np.clip((tone - 0.5) * 1.5 + 0.5, 0, 1) ** 0.9
val = tone * np.clip(m * 1.05, 0, 1)

rows = round(H0 / SS)
v = np.asarray(Image.fromarray((val * 255).astype(np.uint8)).resize((COLS, rows), Image.BOX)) / 255.0
mm = np.asarray(Image.fromarray((m * 255).astype(np.uint8)).resize((COLS, rows), Image.BOX)) / 255.0
lines = []
for r in range(rows):
    row = "".join(
        RAMP[min(len(RAMP) - 1, max(0, round(v[r, c] * (len(RAMP) - 1))))] if mm[r, c] > 0.38 else " "
        for c in range(COLS)
    )
    lines.append(row.rstrip())

# ---- preview ----
cw, ch = 8, 15
pim = Image.new("RGB", (max(len(l) for l in lines) * cw or 8, len(lines) * ch), (13, 17, 23))
pd = ImageDraw.Draw(pim)
try:
    pf = ImageFont.truetype(r"C:/Windows/Fonts/consola.ttf", 14)
except Exception:
    pf = ImageFont.load_default()
for i, l in enumerate(lines):
    pd.text((0, i * ch), l, font=pf, fill=(201, 209, 217))
pim.save(PREVIEW)

# ---- animated svg ----
Wsvg, Hsvg = COLS * CHAR_W, rows * CHAR_H
per = TYPE_SECONDS / rows
# base opacity="1" so the portrait still shows if the host does not run SMIL;
# where SMIL works, <set> hides each line and <animate> reveals it in sequence
tspans = "".join(
    f'<text x="0" y="{(i + 0.85) * CHAR_H:.1f}" opacity="1">{html.escape(ln) or " "}'
    f'<set attributeName="opacity" to="0"/>'
    f'<animate attributeName="opacity" to="1" begin="{i * per:.3f}s" dur="0.01s" fill="freeze"/></text>'
    for i, ln in enumerate(lines)
)
cur_y = ";".join(f"{(i + 0.85) * CHAR_H - CHAR_H * 0.8:.1f}" for i in range(rows))
cursor = (
    f'<rect width="{CHAR_W:.1f}" height="{CHAR_H * 0.9:.1f}" fill="{FG}" x="2" opacity="0">'
    f'<set attributeName="opacity" to="1"/>'
    f'<animate attributeName="y" values="{cur_y}" dur="{TYPE_SECONDS:.2f}s" calcMode="discrete" fill="freeze"/>'
    f'<animate attributeName="opacity" values="1;1;0;1;0;1;0" keyTimes="0;0.6;0.67;0.77;0.84;0.93;1" '
    f'dur="{TYPE_SECONDS + 1.1:.2f}s" fill="freeze"/></rect>'
)
svg = (
    f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {Wsvg:.0f} {Hsvg:.0f}" '
    f'width="{Wsvg:.0f}" height="{Hsvg:.0f}" font-family="{FONT}" '
    f'font-size="{CHAR_H * 0.92:.1f}" xml:space="preserve">'
    f'<rect width="100%" height="100%" fill="{BG}"/><g fill="{FG}">{tspans}{cursor}</g></svg>'
)
open(OUT, "w", encoding="utf-8").write(svg)
print("wrote", OUT, round(os.path.getsize(OUT) / 1024, 1), "KB   grid", COLS, "x", rows,
      "   alpha mask:", alpha is not None)
