import os, html, collections, numpy as np
from PIL import Image, ImageEnhance, ImageOps, ImageFilter

SRC = r"C:/Users/hp/Desktop/Projects/github_setup/onyxmytrojin/assets/_src.jpeg"
OUT = r"C:/Users/hp/Desktop/Projects/github_setup/onyxmytrojin/assets/portrait.svg"

COLS = 92
CHAR_W, CHAR_H = 7.2, 12.6
RAMP = " .·:-=+*oO#%@"
FG, BG = "#c9d1d9", "#0d1117"
FONT = "ui-monospace, 'SF Mono', 'JetBrains Mono', 'Cascadia Code', Consolas, monospace"
TYPE_SECONDS = 2.6
CROP = (110, 108, 302, 356)          # head + shoulders on the 400x400 source

base = Image.open(SRC).convert("L").crop(CROP)
SS = 3
g = base.resize((COLS * SS, round(COLS * SS * (base.height / base.width) * (CHAR_W / CHAR_H))), Image.LANCZOS)
g = ImageOps.autocontrast(g, cutoff=1)
gv = np.asarray(g, np.float32) / 255.0
H0, W0 = gv.shape

# --- knock out the bright background with a border flood-fill ---
T = np.percentile(gv, 55)
bright = gv > T
bg = np.zeros_like(bright)
dq = collections.deque()
for x in range(W0):
    for y in (0, H0 - 1):
        if bright[y, x]:
            bg[y, x] = True; dq.append((y, x))
for y in range(H0):
    for x in (0, W0 - 1):
        if bright[y, x] and not bg[y, x]:
            bg[y, x] = True; dq.append((y, x))
while dq:
    y, x = dq.popleft()
    for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        ny, nx = y + dy, x + dx
        if 0 <= ny < H0 and 0 <= nx < W0 and bright[ny, nx] and not bg[ny, nx]:
            bg[ny, nx] = True; dq.append((ny, nx))

subj = ~bg
subj = np.asarray(Image.fromarray((subj * 255).astype(np.uint8))
                  .filter(ImageFilter.MaxFilter(3))
                  .filter(ImageFilter.MinFilter(5))
                  .filter(ImageFilter.MaxFilter(3))) > 127

# tone the subject: lift shadows so the backlit face has detail, keep it dark-ish
face = np.clip((gv - gv[subj].min()) / (np.ptp(gv[subj]) + 1e-6), 0, 1)
face = face ** 0.72
val = np.where(subj, 0.18 + 0.82 * face, 0.0)

# downsample to the character grid (block mean)
rows = round(H0 / SS)
val = np.asarray(Image.fromarray((val * 255).astype(np.uint8)).resize((COLS, rows), Image.BOX)) / 255.0
mask = np.asarray(Image.fromarray((subj * 255).astype(np.uint8)).resize((COLS, rows), Image.BOX)) / 255.0

idx = np.clip((val * (len(RAMP) - 1)).round().astype(int), 0, len(RAMP) - 1)
lines = []
for r in range(rows):
    row = "".join(RAMP[idx[r, c]] if mask[r, c] > 0.35 else " " for c in range(COLS))
    lines.append(row.rstrip())

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
print("wrote", OUT, round(os.path.getsize(OUT) / 1024, 1), "KB   grid", COLS, "x", rows,
      "  subj%", round(100 * subj.mean(), 1))
