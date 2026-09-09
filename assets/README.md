# assets

| file | what |
|---|---|
| `banner.svg` | Masthead — dark gradient + turbulence texture, a drifting glow and a diagonal light sweep (SMIL), name in light tracked type. ~3 KB, hand-editable. Renders reliably on GitHub (an animated GIF here rendered intermittently via GitHub's image player). |
| `hero.py` | Alternative: generates an animated **GIF** banner (procedural spectral-noise flow). `pip install pillow numpy` then `python assets/hero.py`. Kept in case you want the GIF look; not referenced by the README. |
| `self.svg` | Monochrome ASCII portrait that types itself in (SMIL). Generated from `portrait-src.png`. |
| `portrait-src.png` | Background-removed cutout used by `portrait.py` (made with `rembg`). |
| `portrait.py` | `python assets/portrait.py` → regenerates `self.svg` + `_portrait_preview.png`. Adjust `CROPF` / `COLS` at the top. For a new photo: `rembg i new.jpg assets/portrait-src.png` first. |
| `shubhan.png` | Circular crop of the GitHub avatar — the previous profile image, kept as a fallback. |
| `portrait.py` | Turns a photo into an animated monochrome ASCII-portrait SVG that types itself in. Needs a **good source**: save it as `assets/_src.jpeg` first. |

## ASCII portrait — source photo needs

The current profile photo (backlit, small face, busy river background) does **not**
convert cleanly — the code has no ML background removal. For a recognisable result
the source should be:

- a head-and-shoulders shot, face filling ~60%+ of the frame
- even, front-ish lighting (not backlit)
- plain or softly blurred background

Then: `cp your-headshot.jpg assets/_src.jpeg && python assets/portrait.py`, and swap


## Adding a project GIF

1. Record the app with **ScreenToGif** (Windows) — 6–12 s, cropped tight, ~700 px wide.
2. Save it here, e.g. `phoneix.gif`, keep it under ~5 MB.
3. Reference it under a project row in `README.md`:
   `<br><img src="assets/phoneix.gif" width="640" alt="">`
