# assets

| file | what |
|---|---|
| `hero.gif` | Masthead banner — animated dark grayscale gradient with the name. Seamless 36-frame loop, ~0.75 MB. |
| `hero.py` | Regenerates `hero.gif`. `pip install pillow numpy` then `python assets/hero.py`. Tweak `NAME`, size, palette, motion constants at the top. |
| `shubhan.png` | Profile photo (dark-graded, rounded). |

## Adding a project GIF

1. Record the app with **ScreenToGif** (Windows) — 6–12 s, cropped tight, ~700 px wide.
2. Save it here, e.g. `phoneix.gif`, keep it under ~5 MB.
3. Reference it under a project row in `README.md`:
   `<br><img src="assets/phoneix.gif" width="640" alt="">`
