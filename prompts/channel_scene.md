Create a scene for a Daxilde channel video in the “Kahlo's Notebook” style (engraving on parchment). Work in the repository's current directory.

Read these before starting:
1. `channels/daxilde/AGENTS.md` — channel style, palette, people, motion, subtitles, audio, and delivery. These channel rules override all others.
2. `AGENTS.md` — technical format only (9:16, 1080×1920, 24 fps, H.264, AAC).
3. `templates/scene_template.html` — scene contract: `window.renderAt(t)`, `window.DURATION_SEC`, `window.WORDS`, `drawSubtitles(t)`.
4. `work/script.json` (`accent`, `metaphors`, `narration_az`), `work/words.json` (word timings are already corrected; do not change them), and `work/narration_trim.wav` duration (use ffprobe).

Tasks:
A. Write `work/storyboard.md` as a table: “timecode | phrase | metaphor/scene | camera | drawing motion”. Give each meaningful phrase its own metaphor from `metaphors`, timed from `words.json`.
B. Create `work/scene/index.html` from `templates/scene_template.html`:
   - `window.DURATION_SEC` = narration duration + 1.2 seconds;
   - `window.WORDS` = contents of `work/words.json`;
   - REQUIRED: before rendering, set `SUB.active = '#c98b5a'` (caramel brown) and `SUB.word = '#f7f2e6'`; keep the rest per specification (Arial 700, 52 px, panel near y≈1540, at most 3 words);
   - draw an engraving: dark parchment, hatching and cross-hatching, ivory on black, ONE colored accent from `accent` in `script.json`; draw lines with pen strokes from left to right;
   - if people appear, use faceless silhouettes with necks, shoulders, hands, legs, and hatched clothing; arms have two segments;
   - add a thin double-page border near the frame edge, vignette, and grain.
C. Render with `python scripts/render.py` to `work/video.mp4`. Check with ffprobe: 1080×1920, 24/1, yuv420p, AAC present.
D. Review with `python tools/make_review_sheets.py work/video.mp4 work/review 4` and inspect the sheets with the Read tool. Fix visible defects (blank frames, mismatch with narration, faces, badly placed subtitle panel) and render again.

Constraints: no music. SFX are not implemented in the pipeline yet; say so in the report and do not claim the sound was designed. Do not use other people's footage or videos. Do not change `scripts/*.py`, `AGENTS.md`, `channels/`, or `.claude/`. Do not send anything to Telegram or commit.

Finish with a brief report: path to `work/video.mp4`, duration, ffprobe checks, what is visible on the sheets, and what was not done (including SFX).