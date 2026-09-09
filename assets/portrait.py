import os, html, numpy as np
from PIL import Image, ImageEnhance, ImageOps, ImageFilter

SRC = r"C:/Users/hp/Desktop/Projects/github_setup/onyxmytrojin/assets/_src.jpg"
OUT = r"C:/Users/hp/Desktop/Projects/github_setup/onyxmytrojin/assets/portrait.svg"
PREVIEW = r"C:/Users/hp/Desktop/Projects/github_setup/onyxmytrojin/assets/_portrait_preview.png"

COLS = 84
CHAR_W, CHAR_H = 7.4, 12.8
RAMP = " .·-:=+o*#%@"          # dark -> light
FG, BG = "#c9d1d9", "#0d1117"
FONT = "ui-monospace, 'SF Mono', 'JetBrains Mono', Consolas, monospace"
TYPE_SECONDS = 2.4
CROP = (108, 138, 372, 452)     # x0,y0,x1,y1 on a 460x460 source

base = Image.open(SRC).convert("L")
if base.size != (460, 460):
    base = base.resize((460, 460), Image.LANCZOS)
g = base.crop(CROP)

SS = 4
g = g.resize((COLS * SS, round(COLS * SS * (g.height / g.width) * (CHAR_W / CHAR_H))), Image.LANCZOS)
gv = np.asarray(g, np.float32) / 255.0
H0, W0 = gv.shape

# local-contrast / high-pass: cancel the broad lighting gradient (bright sky vs
# shadowed face) and keep the detail that actually describes the face
lp = np.asarray(g.filter(ImageFilter.GaussianBlur(W0 * 0.16)), np.float32) / 255.0
detail = (gv - lp) * 2.3 + 0.5
mix = np.clip(0.35 * gv + 0.75 * detail, 0, 1)

# S-curve for punch
mix = np.clip((mix - 0.5) * 1.35 + 0.5, 0, 1)
mix = mix ** 1.05

# oval vignette so the leftover background corners fade out
yy, xx = np.mgrid[0:H0, 0:W0].astype(np.float32)
r = np.sqrt((((xx / (W0 - 1)) - 0.5) / 0.60) ** 2 + (((yy / (H0 - 1)) - 0.46) / 0.62) ** 2)
mix = np.clip(mix * (1.0 - 0.85 * np.clip(r - 0.75, 0, 1)) - 0.30 * np.clip(r - 1.0, 0, 1), 0, 1)

rows = round(H0 / SS)
small = np.asarray(Image.fromarray((mix * 255).astype(np.uint8)).resize((COLS, rows), Image.BOX)) / 255.0
idx = np.clip((small ** 0.95 * (len(RAMP) - 1)).round().astype(int), 0, len(RAMP) - 1)
lines = ["".join(RAMP[i] for i in row).rstrip() for row in idx]

# ---- preview png ----
from PIL import ImageDraw, ImageFont
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
W, Hh = COLS * CHAR_W, rows * CHAR_H
per = TYPE_SECONDS / rows
tspans = []
for i, ln in enumerate(lines):
    tspans.append(
        f'<text x="0" y="{(i+0.85)*CHAR_H:.1f}" opacity="0">{html.escape(ln) or " "}'
        f'<animate attributeName="opacity" from="0" to="1" begin="{i*per:.3f}s" dur="0.01s" fill="freeze"/></text>')
cur_y = ";".join(f"{(i+0.85)*CHAR_H - CHAR_H*0.8:.1f}" for i in range(rows))
cursor = (f'<rect width="{CHAR_W:.1f}" height="{CHAR_H*0.9:.1f}" fill="{FG}" x="2">'
          f'<animate attributeName="y" values="{cur_y}" dur="{TYPE_SECONDS:.2f}s" calcMode="discrete" fill="freeze"/>'
          f'<animate attributeName="opacity" values="1;1;0;1;0;1;0" keyTimes="0;0.6;0.67;0.77;0.84;0.93;1" '
          f'dur="{TYPE_SECONDS+1.1:.2f}s" fill="freeze"/></rect>')
svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W:.0f} {Hh:.0f}" width="{W:.0f}" height="{Hh:.0f}" '
       f'font-family="{FONT}" font-size="{CHAR_H*0.92:.1f}" xml:space="preserve">'
       f'<rect width="100%" height="100%" fill="{BG}"/><g fill="{FG}">'
       + "".join(tspans) + cursor + '</g></svg>')
open(OUT, "w", encoding="utf-8").write(svg)
print("wrote", OUT, round(os.path.getsize(OUT) / 1024, 1), "KB   grid", COLS, "x", rows)
