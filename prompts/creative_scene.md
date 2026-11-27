Create a scene for a short finance video in paper-collage style for the Disli Hardz channel. Work in the repository's current directory.

Read first:
1. `AGENTS.md` — channel rules (9:16, 1080×1920, 24 fps, paper collage, karaoke subtitles, no music).
2. `.claude/skills/vizavi-motion/SKILL.md` — section 0 (channel overrides), then other sections as needed.
3. `references/2d-video/sheets/sheet_02.png` — style reference; inspect the image.
4. `templates/scene_template.html` — scene contract: `window.renderAt(t)`, `window.DURATION_SEC`, `window.WORDS`, `drawSubtitles(t)`.
5. `work/script.json`, `work/words.json`, and `work/narration_trim.wav` (use ffprobe for duration).

Tasks:
A. Write `work/storyboard.md` as a table: “timecode | phrase | visible content | shot | motion”, based on segments in `work/words.json`. Give each phrase its own illustration at the right time.
B. Create `work/scene/index.html` from `templates/scene_template.html`:
   - `window.DURATION_SEC` = duration of `work/narration_trim.wav` + 1.2 seconds;
   - `window.WORDS` = contents of `work/words.json` (embed the array in the file);
   - `window.renderAt(t)` draws a paper collage: paper texture, irregular edges, soft shadows, muted palette, and 3+ parallax planes;
   - if people appear, make them full paper figures without facial features (head, neck, body, detailed clothing, hands, legs, shoes);
   - keep `drawSubtitles(t)` over every frame, unchanged.
C. Render with `python scripts/render.py` to `work/video.mp4`. Check with ffprobe: 1080×1920, 24/1 fps, yuv420p, AAC audio.
D. Review quality with `python tools/make_review_sheets.py work/video.mp4 work/review 4` and inspect `work/review/sheet_*.png`. Fix problems (cropping, blank frames, mismatch with phrase, artifacts, faces), then render and review again.

Constraints: no music or sound effects; do not use other people's videos, footage, or audio; do not change `scripts/*.py`, `AGENTS.md`, or `.claude/`; do not send anything to Telegram or commit.

Finish with a brief report: path to `work/video.mp4`, duration, ffprobe checks, what is visible in the contact sheets, and remaining problems. Do not claim to have checked motion or real-time audio.