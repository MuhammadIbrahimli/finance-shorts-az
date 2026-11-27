# finance-shorts-az

A cloud-based pipeline for creating short-form financial videos (9:16, 1080×1920, 24 fps) in Azerbaijani for the **Gizli Xərc** channel. A cloud routine runs once a day following the instructions in [prompt.md](prompt.md). The output consists of a video and accompanying text delivered via Telegram. **No automatic publishing.**

## How It Works

```
find_trend ─► transcript ─► script and delivery content (written by Claude) ─► tts ─► trim ─► align_words
           ─► storyboard and scene (created by Claude) ─► render ─► QA subagents ─► notify
```

| File | Purpose |
|---|---|
| `prompt.md` | Step-by-step instructions for a single routine execution |
| `AGENTS.md` (+ `CLAUDE.md`) | Permanent channel guidelines: format, style, subtitles, quality assurance, and delivery |
| `scripts/find_trend.py` | Finds the most-viewed financial Short, no longer than 90 seconds, published within the last 14 days, and not listed in `used.json` |
| `scripts/transcript.py` | Retrieves the video transcript: first from a vidIQ file (saved by Claude), otherwise from YouTube captions |
| `scripts/tts.py` | Generates script narration using Gemini TTS |
| `scripts/trim.py` | Shortens pauses longer than 0.4 seconds to 0.2 seconds |
| `scripts/align_words.py` | Generates word-level timestamps using speech recognition (faster-whisper) and alignment with the original script |
| `scripts/render.py` | Captures the `window.renderAt(t)` scene frame by frame using Chromium and assembles a 24 fps MP4 video |
| `scripts/notify.py` | Sends the video and accompanying delivery content via Telegram; sends an error report if the pipeline fails |
| `templates/scene_template.html` | Scene framework with embedded karaoke-style subtitles based on the specifications |
| `.claude/agents/` | Three quality assurance subagents: `video-quality-reviewer`, `art-director`, `subtitle-auditor` |
| `.claude/skills/vizavi-motion/` | Motion graphics video creation skill (applied wherever it does not conflict with AGENTS.md) |
| `references/2d-video/` | Guidelines and a sample contact sheet from a 2D project, used as a visual style reference |
| `tools/make_review_sheets.py` | Generates contact sheets and frame differences for quality review |

## Routine Setup (Manual, One-Time Configuration)

1. Create a cloud routine using the `MuhammadIbrahimli/finance-shorts-az` repository, the `main` branch, and a daily schedule. Use the contents of `prompt.md` as the routine prompt.

2. Setup script (Ubuntu):

   ```bash
   apt-get update && apt-get install -y ffmpeg
   pip install -r requirements.txt
   playwright install chromium --with-deps
   ```

3. Configure the routine's environment variables. These are secrets stored in the routine settings and must not be committed to the repository.

| Variable | Purpose |
|---|---|
| `YOUTUBE_API_KEY` | YouTube Data API v3 |
| `GEMINI_API_KEY` | Gemini API (TTS) |
| `TG_TOKEN` | Telegram bot token |
| `TG_CHAT_ID` | ID of the chat where the bot delivers the results |
| `GEMINI_TTS_MODEL`, `GEMINI_TTS_VOICE` | Optional (defaults: `gemini-2.5-flash-preview-tts`, `Kore`) |
| `WHISPER_MODEL` | Optional (default: `medium`) |

4. Write access to the `main` branch is required only to commit changes to `used.json`.

5. vidIQ (optional): connect the vidIQ connector to the routine.

## Local Testing

API keys for local debugging are stored in a file outside the repository. The file path is specified using the `FINANCE_SHORTS_ENV` environment variable.

A template without secret values is available in [.env.example](.env.example). The `.env`, `*.env`, and `work/` files and directories are excluded through `.gitignore`.

```bash
pip install -r requirements.txt && playwright install chromium

python scripts/find_trend.py --dry-run     # Only displays the selected video; does not modify used.json

python scripts/notify.py --check           # Validates the token and chat; does not send messages
```

## Known Limitations

- **YouTube captions:** Retrieved using the `youtube-transcript-api` library without an API key. This is an unofficial method, and YouTube frequently blocks cloud IP addresses. Using a connected vidIQ connector is more reliable.

- **Telegram chat:** The bot cannot send messages to a chat until the user presses "Start" in their conversation with the bot.

- **`used.json`:** Marks a video as used immediately after selection, even if subsequent pipeline stages fail.

- **Gemini voice generation:** Azerbaijani language support is not officially confirmed in the documentation. Review the first generated result.

- **No music:** This is a channel requirement. The `vizavi-motion` skill suggests music by default, but this behavior is overridden in this project.

- **Telegram file size limit:** 50 MB. A 30–60-second video rendered at CRF 22 typically stays within this limit.

- **Rule conflict:** AGENTS.md prohibits trimming the user's voice recordings. However, at the channel owner's request, the pipeline shortens pauses in AI-generated narration. This is the only permitted audio trimming operation; the spoken text and speech speed remain unchanged.

- **Excluded from migration:** The `Daxilde/` directory (a separate channel), the `script-rewrite` skill (specific to the Daxilde channel), 3D projects, and the original project videos and media assets. The `STORYBOARD.md` and `config.json` files referenced in the guidelines did not exist in the original directory.
