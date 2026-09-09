# assets

| file | what |
|---|---|
| `hero.gif` | Masthead banner — animated dark grayscale gradient with the name. Seamless 36-frame loop, ~0.75 MB. |
| `hero.py` | Regenerates `hero.gif`. `pip install pillow numpy` then `python assets/hero.py`. Tweak `NAME`, size, palette, motion constants at the top. |
| `shubhan.png` | Profile photo — circular crop of the GitHub avatar. |
| `portrait.py` | Turns a photo into an animated monochrome ASCII-portrait SVG that types itself in. Needs a **good source**: save it as `assets/_src.jpeg` first. |

## ASCII portrait — source photo needs

The current profile photo (backlit, small face, busy river background) does **not**
convert cleanly — the code has no ML background removal. For a recognisable result
the source should be:

- a head-and-shoulders shot, face filling ~60%+ of the frame
- even, front-ish lighting (not backlit)
- plain or softly blurred background

Then: `cp your-headshot.jpg assets/_src.jpeg && python assets/portrait.py`, and swap
`shubhan.png` for `portrait.svg` in `README.md`.

## Adding a project GIF

1. Record the app with **ScreenToGif** (Windows) — 6–12 s, cropped tight, ~700 px wide.
2. Save it here, e.g. `phoneix.gif`, keep it under ~5 MB.
3. Reference it under a project row in `README.md`:
   `<br><img src="assets/phoneix.gif" width="640" alt="">`
