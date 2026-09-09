import os, numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 250
FRAMES = 36
DURATION_MS = 70
SEED = 11
OUT = r"C:/Users/hp/Desktop/Projects/github_setup/onyxmytrojin/assets/hero.gif"
PALETTE_COLORS = 110

BG = 0.050
BASE = 0.085
CONTRAST = 0.155
HIGHLIGHT = 0.13

NAME = "SHUBHAN MEHROTRA"
FONT_PATH = r"C:/Windows/Fonts/segoeuil.ttf"
FONT_SIZE = 68
TRACKING = 9
NAME_GREY = 231


def tileable(h, w, beta, seed):
    r = np.random.default_rng(seed)
    fy = np.fft.fftfreq(h)[:, None]
    fx = np.fft.fftfreq(w)[None, :]
    f = np.sqrt(fy ** 2 + fx ** 2)
    f[0, 0] = 1e-6
    img = np.fft.ifft2((1.0 / f ** beta) * np.exp(1j * r.uniform(0, 2 * np.pi, (h, w)))).real
    img -= img.mean(); img /= img.std()
    return img


base = tileable(H, W, 2.7, SEED)
warpx = tileable(H, W, 3.0, SEED + 1)
warpy = tileable(H, W, 3.0, SEED + 2)
fine = tileable(H, W, 2.3, SEED + 3)
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)


def sample(field, sx, sy):
    x0 = np.floor(sx).astype(int); y0 = np.floor(sy).astype(int)
    fx = sx - x0; fy = sy - y0
    x0 %= W; y0 %= H; x1 = (x0 + 1) % W; y1 = (y0 + 1) % H
    a = field[y0, x0]; b = field[y0, x1]; c = field[y1, x0]; d = field[y1, x1]
    return (a * (1 - fx) + b * fx) * (1 - fy) + (c * (1 - fx) + d * fx) * fy


vy = np.linspace(-1, 1, H)[:, None]
vig = np.clip(1.0 - (np.abs(vy) ** 2.4) * 1.18, 0.0, 1.0)

# static dither: white grain + a Bayer pattern, identical every frame ->
# breaks GIF banding without any inter-frame shimmer
_bayer = np.array([[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]]) / 16.0 - 0.5
bayer = np.tile(_bayer, (H // 4 + 1, W // 4 + 1))[:H, :W]
grain = (np.random.default_rng(99).normal(0, 0.010, (H, W)) + bayer * 0.028)


def smoothstep(e0, e1, v):
    t = np.clip((v - e0) / (e1 - e0), 0, 1)
    return t * t * (3 - 2 * t)


font = ImageFont.truetype(FONT_PATH, FONT_SIZE)
_d = ImageDraw.Draw(Image.new("L", (1, 1)))
widths = [_d.textlength(ch, font=font) for ch in NAME]
total = sum(widths) + TRACKING * (len(NAME) - 1)
nx0 = (W - total) / 2
ascent, descent = font.getmetrics()
ny = (H - (ascent + descent)) / 2 - 3

rgb_frames = []
for i in range(FRAMES):
    p = i / FRAMES
    ang = 2 * np.pi * p
    # every term is periodic in `ang` -> the loop is seamless
    ox = 22 * np.cos(ang) + 7 * np.cos(2 * ang + 0.7)
    oy = 13 * np.sin(ang)
    wx = sample(warpx, xx + 34 * np.cos(ang), yy + 20 * np.sin(ang))
    wy = sample(warpy, xx + 30 * np.sin(ang + 1.1), yy + 20 * np.cos(ang))
    amp = 92.0
    f1 = sample(base, xx + ox + amp * wx, yy + oy + amp * wy)
    f2 = sample(fine, xx * 1.8 + 40 * np.cos(ang) + 45 * wx, yy * 1.8 + 20 * np.sin(ang) + 22 * wy)
    field = 0.8 * f1 + 0.2 * f2
    field = 0.5 + 0.5 * np.tanh(field * 0.9)

    grey = BASE + CONTRAST * (field - 0.5)
    grey = grey + HIGHLIGHT * smoothstep(0.80, 0.995, field)
    grey = BG + (grey - BG) * vig
    grey = np.clip(grey + grain, 0.0, 1.0)

    im = Image.fromarray((grey * 255).astype(np.uint8), "L").convert("RGB")
    d = ImageDraw.Draw(im)
    x = nx0
    for ch, wch in zip(NAME, widths):
        d.text((x, ny), ch, font=font, fill=(NAME_GREY, NAME_GREY, NAME_GREY))
        x += wch + TRACKING
    rgb_frames.append(im)

pal_src = rgb_frames[FRAMES // 3].quantize(colors=PALETTE_COLORS, method=Image.MEDIANCUT)
frames = [f.quantize(palette=pal_src, dither=Image.NONE) for f in rgb_frames]
frames[0].save(OUT, save_all=True, append_images=frames[1:],
               duration=DURATION_MS, loop=0, optimize=True)
print("wrote", OUT, round(os.path.getsize(OUT) / 1e6, 2), "MB", W, "x", H, FRAMES, "frames")
