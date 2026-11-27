# Daily Run: Azerbaijani Finance Short (Disli Hardz)

You are working in a cloud routine inside a clone of `finance-shorts-az`. One run produces one video. Before starting, read `AGENTS.md` (included through `CLAUDE.md`). Those persistent channel rules cover format, style, subtitles, review, and deliverables. They take precedence over `.claude/skills/vizavi-motion` where they conflict; for example, this channel has no music.

Do not publish the video elsewhere. Deliver only to Telegram: the video and its publication text. Do not reuse another creator's video, footage, audio, or full script. Use facts and ideas rewritten in your own words.

Read keys and tokens only from environment variables. Do not print them, write them to files, or commit them.

## 0. Environment

```bash
pip install -r requirements.txt
playwright install chromium --with-deps
ffmpeg -version >/dev/null && ffprobe -version >/dev/null || echo "NO FFMPEG"
```

If ffmpeg is unavailable, send an error report (see “Errors”) and stop.

Required variables: `YOUTUBE_API_KEY`, `GEMINI_API_KEY`, `TG_TOKEN`, and `TG_CHAT_ID`. Optional: `GEMINI_TTS_MODEL`, `GEMINI_TTS_VOICE`, `WHISPER_MODEL` (default `medium`), and `RENDER_FPS` (default 24).

Store all temporary files in `work/`. This directory is not committed.

## Workflow

Perform the steps in order. If a step fails, send an error report and stop:

```bash
python scripts/notify.py --error --step "<step number and name>" --message "<reason in 1–3 sentences>"
```

### 1. Find a trend

```bash
python scripts/find_trend.py
```

The script selects the most-viewed eligible finance Short (up to 90 seconds, posted within 14 days, and not already listed in `used.json`). It writes `work/trend.json` and adds the selected ID to `used.json`.

### 2. Get a transcript

If the vidIQ connector and its `video_transcript` tool are available, call it for the URL in `work/trend.json` and save text without timestamps to `work/vidiq_transcript.txt`. Then run:

```bash
python scripts/transcript.py
```

The script uses the vidIQ transcript if present; otherwise it tries YouTube captions. A missing transcript or one shorter than 300 characters is an error. Do not invent transcript text.

### 3. Write the script, translation, and deliverables

Read `work/transcript.txt` and `work/trend.json`. Write `work/script.json` with exactly these fields:

```json
{
  "source_url": "from trend.json",
  "title_az": "Başlıq: up to 90 characters",
  "cover_prompt_az": "Örtük üçün prompt: a 9:16 cover prompt in the video's style, with text below the middle and decorative typography; see AGENTS.md",
  "description_az": "Təsvir: 2–4 sentences about the video, followed by exactly five hashtags",
  "narration_az": "90–130 words of narration, about 30–50 seconds",
  "key_facts": ["source facts and figures retained"]
}
```

Rules:

- Preserve the source's meaning, facts, and numbers. Do not change figures, percentages, or dates.
- Write new phrasing; do not copy sentences. The idea structure may remain similar.
- If a claim cannot be verified, qualify it as “according to the source” or omit it.
- Do not give personalized investment advice or tell viewers to buy a specific asset.
- Write Azerbaijani with correct characters: ə, ı, ö, ü, ş, ç, ğ.
- `description_az` must contain exactly five hashtags; otherwise sending will stop.

### 4. Create narration audio

```bash
python scripts/tts.py          # work/narration.wav (Gemini TTS)
python scripts/trim.py         # work/narration_trim.wav (pauses >0.4 s become 0.2 s)
python scripts/align_words.py  # work/words.json (script word timings)
```

Check `work/narration_trim.wav` duration with ffprobe. If it is outside 20–60 seconds, rewrite `narration_az` and repeat audio synthesis, trimming, and alignment.

### 5. Storyboard

Write `work/storyboard.md` as a table: `timecode | phrase | what is visible | shot/camera | movement`. Cover the entire narration using the timings in `work/words.json`. Give every phrase its own environment. Characters must be full, faceless figures and actions must read clearly. Do not add music.

### 6. Build the scene

Create `work/scene/index.html` from `templates/scene_template.html`:

- Set `window.DURATION_SEC` to narration duration plus 1.2 seconds.
- Set `window.WORDS` to the contents of `work/words.json`.
- Implement `window.renderAt(t)` in the paper-collage style described in `AGENTS.md`.
- Keep `drawSubtitles(t)` over the rendered frame (karaoke captions, panel around y≈1540).

Style references: `references/2d-video/sheets/sheet_02.png` and `references/2d-video/AGENTS.md`.

### 7. Render

```bash
python scripts/render.py       # work/video.mp4, 1080x1920, 24 fps
```

If rendering fails, fix the scene and retry this step only, no more than twice.

### 8. Quality review (required)

```bash
python tools/make_review_sheets.py work/video.mp4 work/review
```

Then run the three independent agents from `.claude/agents/`, giving them paths to `work/` and `work/review/`:

- `video-quality-reviewer`: meaning, anatomy, movement, matching frames to words, technical properties
- `art-director`: paper collage style, color, detail, composition
- `subtitle-auditor`: karaoke timing, word boundaries, text, and panel

Fix every MAJOR/FAIL issue, rebuild affected scenes, and repeat the review. If the agents are unavailable, check the video yourself and say that independent review was not performed.

Inspect the final file:

```bash
ffprobe -v error -show_entries stream=codec_name,width,height,r_frame_rate,pix_fmt -show_entries format=duration -of default=nw=1 work/video.mp4
```

Expected: H.264, 1080×1920, 24/1 fps, yuv420p, AAC audio, and duration equal to the narration plus tail.

### 9. Send to Telegram

```bash
python scripts/notify.py
```

Only the video and the publication text (Başlıq, Örtük üçün prompt, Təsvir) are sent.

### 10. Save the used-video record

`find_trend.py` has already updated `used.json`. Commit and push only that file to `main`:

```bash
git config user.name "finance-shorts-bot"
git config user.email "finance-shorts-bot@users.noreply.github.com"
git add used.json
git commit -m "Mark video as used: <video_id from work/trend.json>"
git push origin HEAD:main
```

Do not commit `work/`, create a branch, or open a pull request.

## Errors

```bash
python scripts/notify.py --error --step "<step>" --message "<what happened>"
```

Do not present a placeholder as a finished video. State clearly if anything failed.

## Run summary

Briefly report the source link, transcript source (`vidiq` or `youtube_captions`), duration, review results (which agents ran and what they found), whether Telegram delivery succeeded, and what was not checked.