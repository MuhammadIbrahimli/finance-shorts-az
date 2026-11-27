# Agent Instructions — Azerbaijani Finance Shorts (Disli Hardz)

These persistent rules apply to every video in this repository. A specific brief can override them for that video only. This repo serves the Disli Hardz finance channel; if a brief names another channel, stop because this repo is not configured for it.

## Files and output

- Each run uses `work/`, which is not committed. Keep the script, voiceover, transcript, word timings, storyboard, and review frames there.
- The final video is `work/video.mp4`. After review, keep only the MP4 and files required to reproduce it; remove drafts, contact sheets, and temporary frames.
- The scene template is `templates/scene_template.html`; shared paths and configuration are in `scripts/common.py`.
- Review agents live in `.claude/agents/`. The 2D reference material is in `references/2d-video/`.
- Remove superseded scene drafts after accepting a replacement.

## Video format

- Vertical 9:16, 1080×1920, 24 fps, H.264/yuv420p video, AAC audio.
- Final encode uses libx264 with `-preset slow -crf 22` via `scripts/render.py`.
- Duration equals the voiceover plus a 1–1.5 second tail.

## Audio

The only audio is the narration (Gemini TTS, default voice `Kore`). Do not add music or extra sound effects unless the current brief explicitly requires them.

The `vizavi-motion` skill may normally suggest music and sound design; this channel overrides that default: no music.

Per the pipeline owner's requirement, pauses longer than 0.4 seconds are shortened to 0.2 seconds by `scripts/trim.py`. Do not change the words or narration speed.

## Visual style: paper collage

- Use `references/2d-video/sheets/sheet_02.png` and `references/2d-video/AGENTS.md` as references. 3D projects are not the style reference.
- Everything should look like layered cut paper: visible paper grain, slightly irregular edges, soft contact shadows, and a muted evening palette (blue-gray, sand, sage, terracotta, gold). Avoid a childish cartoon look, bright gradients, thick outlines, and neon colors.
- Give each meaningful phrase its own environment with concrete objects, furniture, windows, shelves, lighting, and shadows. Do not reuse a background without a story reason.
- Build depth with at least three parallax planes, subtle camera movement, light pools, and a vignette.
- Add detail without random clutter. Text and numbers appear only when the narration mentions them.
- Use moderate paper grain: roughly 34/255 on elements and 11/255 on the overall background.

## Lessons from previous revisions

- **Subtitles:** burned-in word-by-word karaoke. Use Arial Bold (700), 52 px at 1080×1920, at most three words per group, group width no more than 820 px, background `rgba(18,22,28,.5)`, radius 13 px, padding about 17 px. Text is `#f7f2e6`; the active word is `#ffdc45`; no text shadow. Center the panel around y≈1540. Do not place it below about y=1600, where it can cover interface controls.
- **Subtitle text must exactly match** `work/script.json` → `narration_az`. Timing comes from speech recognition (faster-whisper); align the script words to recognized speech using `scripts/align_words.py`. Record and report any mismatch between the voice and script.
- **Walking:** step phase follows distance traveled; legs move in the direction of travel. Vary speed (about 120–170 px/s), phase, and start times between people. Arms swing opposite to the legs. Keep walking speed constant (about 230 px/s); do not accelerate mid-scene. Use a short smooth deceleration when stopping. Keep characters at least one body-width apart.
- **Objects rest on surfaces:** laptops, jars, and dishes sit on tables; the bottom of an object meets the tabletop. Do not make objects float.
- Keep hands out of furniture and surfaces. A thinking gesture places the hand near the cheek. Question/exclamation marks appear near a character's head, not on windows or paintings.
- A character in a conversation remains present until the scene ends.
- Each location needs meaningful detail; empty backgrounds are defects.
- Use brand names from the script (for example, “Hyper Agency”).

## Characters

Characters are full human figures without facial features: head, neck, shoulders, detailed clothing, hands, legs, and shoes. Keep clothes and hairstyles consistent between scenes.

Use plausible anatomy: arms attach to shoulders and have upper arm, forearm, and hand; reach is limited; elbows point naturally down or outward. Do not draw twisted, protruding, stretched, or cut-off limbs, floating bodies, or limbs crossing furniture. People seated at a table or counter must be behind it.

Make actions readable: an object being handed over must visibly travel from one hand to the other; a thrown object follows an arc; walking shows alternating legs. Objects must not cover a character's head.

## Workflow

1. **Narration:** synthesize Gemini TTS from `narration_az`; trim long pauses with `trim.py`; transcribe with faster-whisper `medium`, explicitly using language `az`; align script words and write `work/words.json`.
2. **Storyboard:** use real word timings to map each phrase to an environment, action, and camera. Save a `timecode | phrase | what is visible | shot | movement` table in `work/storyboard.md`.
3. **Build the scene:** use HTML/Canvas and make each frame a function of time (`window.renderAt(t)`). Cache static layers and render with headless Chromium plus ffmpeg.
4. **Quality review before delivery:** run the independent agents in `.claude/agents/`:
   - `video-quality-reviewer` — meaning, anatomy, movement, physics, and matching frames to narration
   - `art-director` — paper-collage style, color, detail, and composition
   - `subtitle-auditor` — karaoke timing, word boundaries, text, and readability
   Give them the `work/` path and review sheets from `tools/make_review_sheets.py`. Fix every FAIL/MAJOR issue and rerun review for affected scenes. If the agents are unavailable, perform the same checks yourself and say independent review was not performed.
5. **Inspect the final MP4:** verify codec, 1080×1920, 24 fps, frame count equals duration × 24, duration equals narration plus tail, AAC audio is present, scene boundaries, start/end, and neighboring-frame differences for unintended jumps.
6. **Clean up:** leave only `video.mp4` and reproducibility files in `work/`; remove temporary material.
7. **Report honestly:** state which visual and numeric checks were performed and which were not. The agent cannot perceive motion and sound in real time from a contact sheet.

## Deliverables (Azerbaijani)

Write the publication text in `work/script.json`, in Azerbaijani:

1. **Başlıq:** short, relevant, engaging, without misleading clickbait.
2. **Örtük üçün prompt:** a 9:16 cover-image prompt in the same visual style, palette, lighting, atmosphere, and metaphors as the video. Specify the exact cover text, its placement around 55–75% of frame height, and decorative typography (paper-cut, dimensional, illuminated, or calligraphic). Do not request a generic system font.
3. **Təsvir:** 2–4 sentences describing the video and exactly five hashtags.

Do not add unrelated material to this deliverables block.

## Telegram delivery

After the video is accepted and checked, send only the video and deliverables text through `scripts/notify.py`. Do not send source information or technical reports to Telegram; include those in the run report.

Use `TG_TOKEN` and `TG_CHAT_ID` only from environment variables. Never print or store them in repository files, logs, or responses. If delivery is unavailable because variables are missing or the file exceeds 50 MB, report that; do not invent a workaround.

## Routine environment

The cloud routine runs Linux/Ubuntu. It requires ffmpeg, Python 3, Chromium (`playwright install chromium --with-deps`), and packages from `requirements.txt`. For Windows debugging, use Playwright with the configured Chromium executable.