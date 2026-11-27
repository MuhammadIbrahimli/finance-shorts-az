# Daxilde — Agent Instructions (Psychology, Neuroscience, Health, and Body Care)

Daxilde is an Azerbaijani-language channel about dark psychology, neuroscience, behavioral psychology (“why we do what we do”), health, and body care. Apply these persistent rules to every video request in this folder without asking again. A new explicit brief overrides them only for that video.

The related Disli Hardz channel (finance, paper collage) is in the parent folder. Its technical rules for format, subtitles, sound, and review are inherited here; this channel differs in visual style (“Kahlo's Notebook” engraving), colors, and sound.

## Project layout
- Channel workspace: C:\Users\muham\claude-video\Daxilde. Project files (code, narration, script, timed words) belong in projects/<name>/.
- Final videos go only in videos/ (for example, videos/<name>.mp4). Keep only finished videos there: no frames, clips, drafts, audio, subtitles, contact sheets, or project files.
- Store temporary PNGs, sheets, intermediate MP4/WAV files, and speech-recognition virtual environments in scratchpad/temp; remove them after review. Remove superseded project versions after accepting a replacement.
- Tool templates are in tools/templates/: render.js renders frames through puppeteer-core and Chrome; sfx_base.py synthesizes sound effects and mixes them with speech; align_script.py/mkwords.py convert script words to timings. Review finished MP4 files with tools/make_review_sheets.py.

## Format (required, inherited from Disli Hardz)
- 9:16, 1080×1920, H.264, yuv420p, AAC, 24 fps. Encode the final video with libx264 -preset slow -crf 22 (about 35–80 MB for 95 seconds; CRF 17 is unnecessary).
- The user's narration is the audio source. Do not trim it, alter its speed, or replace it; video duration is narration plus a short tail. Narration and subtitles are in Azerbaijani unless the user says otherwise. Subtitle text must exactly match the user's script; faster-whisper medium (ffmpeg to float32 16 kHz) supplies word timings only.

## Visual style: “Kahlo's Notebook” — an animated scientific engraving
Approved by the user on 2026-11-09. This is not Disli Hardz paper collage and not a flat “dark noir” look with colored figures (the previous version was rejected for looking too much like Disli Hardz).
- Concept: the video feels like pages from an old anatomy atlas or neuroscientist's notebook (Ramon y Cajal): dark ink, hatching, fine lines on aged dark parchment. Draw the image in with a pen before the viewer's eyes and illuminate it. Use the language of science and “forbidden notes,” not children's illustration.
- Materials: linework, cross-hatching, engraved cuts, ivory contours; hatching density controls volume and light. No flat character fills or cut-paper look. Background: parchment with stains, fibers, and grain; add a thin double-page border around the frame.
- Palette: nearly black parchment (#12100d, #1c1712), ivory ink (#e9dfc8), plus one colored accent per scene: amber #ffb867 (light, memory), blood red #c2414b (anxiety/threat), or turquoise blue #5fd8ff (neuron impulses, brain signals). Everything else is monochrome. For health/body-care topics, use softer peach #f2b08a or mint #7fe0c3 on skin/layers. No rainbow palettes.
- People: anatomical figures in engraving style (écorché: show muscles/vessels/skeleton only where they explain the point), head-profile cross-sections, or faceless silhouettes with neck, shoulders, hands, legs, and hatched clothing. Keep clothing and hairstyle consistent across scenes. Anatomy must be plausible; arms use two segments (IK); no twisted limbs, floating, or clipping through objects.
- Motion: draw lines in; let hatching build up; let neurons grow with impulses traveling along them; turn or reveal pages. The camera drifts slowly across 3+ parallax planes with dust/impulse particles. Reveal each scene with left-to-right pen strokes.
- Labels/on-screen text: fine handwritten margin notes and organ labels only when spoken. Large accent typography only for a spoken word. No random text.
- Metaphors: neuron and synapse, brain cross-section, highlighted brain region, anatomical cutaway, puppet and strings, mask, mirror, maze, clock/gears, scales, door/lock, trap — always rendered as engravings.
- Lighting: the scene accent is the only glow source. Use vignette, light grain, and aged-paper stains. Each meaningful phrase gets its own metaphor/setting; do not repeat backgrounds without a reason. Blank or monochrome frames are defects.
- Quality references (composition, detail, cleanliness): 2D projects under youtube-video/2d-video/projects (3D projects are not references). The style differs, but the quality bar is the same. Devise the video design/concept before coding, within these rules.

## Subtitles (required, burned in; inherited from Disli Hardz)
- Word-by-word karaoke, Arial 700, 52 px at 1080×1920, no more than 3 words per group, group width ≤ 820 px.
- Panel: rgba(18,22,28,0.5), radius 13, padding about 17 px. Words are #f7f2e6; the active spoken word is caramel brown #c98b5a (user decision; not blue or yellow — Disli Hardz uses yellow). No shadows. If brown lacks contrast on a dark frame, lighten only up to #d9a06a, staying within brown.
- Position: panel center at y≈1540 of 1920 (not above 1500 or below 1600, due to TikTok UI).
- Use word timings; compare boundaries with speech (re-transcription/energy). Log and report discrepancies between speech and script.

## Audio (required)
- Speech plus quiet SFX and ambience only. SFX peak ≤ 0.20 (speech peak ≈1.0); ambience quieter still. Duck SFX under speech by about 45%. Do not add transition sounds.
- Choose distinct sounds appropriate to the action; do not reuse the same sound. Suggestions: ambience: low drone/hum (sub-bass), quiet electrical buzz, faint wind, occasional clock tick or distant drip; tense scenes: soft pulse/heartbeat; calm scenes: breathing/soft air.
- Neuroscience: short electrical ticks/sparks for neuron impulses, soft synthetic pings, a quiet click when a brain region lights up.
- Psychology/manipulation: puppet-string creak, dull knock, metal lock, fabric rustle, wordless airy whisper, glass-crack chime.
- Health/body care: water/drop, soft exhale, fabric rustle, light sparkle on clean skin.
- Text accents: short quiet pops/blips at varying pitches. No music or loud stingers.

## Transitions
Do not overuse transition animation. Mostly cut on speech. Use a stylized transition (pen-drawing a page, accent flash, or reveal from darkness) only for major topic changes (intro to topic, topic to conclusion, ending/call to action). No circles/balls and no frequent wipes.

## From script to video
1. Read the script; identify the idea, 3–5 key images, and accent color.
2. Transcribe and align script words; create STORYBOARD.md (timecode → phrase → metaphor/scene → camera).
3. Build HTML/Canvas (each frame is a function of time; cache static layers), render with 4 processes, add SFX through sfx_base.py, and use ffmpeg.
4. If the user supplies replacement narration for the same video, do not rewrite the video. Re-align words, create anchors with align_script.py, warp scene timing, and rewrite only changed portions.

## Delivery text accompanying a finished video (required, in Azerbaijani)
In the final response after delivering a video (technical report may be in Russian), always include in Azerbaijani:
1. Başlıq — short, engaging, on-topic title without misleading clickbait.
2. Örtük üçün prompt — a prompt for a 9:16 cover in the same style as the video (palette, lighting, atmosphere, metaphors), with a short topical phrase. Cover text must sit below the middle of the frame (about 55–75% of its height, neither near the top nor in the UI area at the bottom) and use expressive custom typography matching the video (decorative, dimensional/glowing/cut-paper/handwritten calligraphy, with outline, shadow, or glow and strong readability), not a standard system font. State the exact text, placement below the middle, and typography/effect in the prompt.
3. Təsvir — 2–4 sentences describing the video plus exactly 5 hashtags.
Do not add anything else to this block.

## Telegram delivery (required after acceptance, for all channels)
Standing user authorization (2026-11-09): once the video is accepted and reviewed, the assistant sends to the user's Telegram: (1) final MP4 using python tools/send_telegram.py --video <path>, and (2) Azerbaijani text with Başlıq, Örtük üçün prompt, and Təsvir (+5 hashtags), as one UTF-8 file via --text. Configuration is telegram.env at the claude-video root (bot token and chat ID; only the script reads it).
- Never display, print, copy into responses/logs/project files, or otherwise expose the token. Do not read telegram.env unless needed; check with python tools/send_telegram.py --check.
- If telegram.env is unconfigured (exit code 2) or the file exceeds 50 MB, do not invent a workaround. Tell the user what needs to be done; still provide the video and text in chat as usual.
- Send only the accepted final video and delivery text, and only to the chat configured in telegram.env. If the user explicitly asks not to send, do not send.

## Review (required before delivery)
Run independent agents from .claude/agents/ (give them project paths and review sheets from tools/make_review_sheets.py): video-quality-reviewer, art-director, and subtitle-auditor. Fix FAIL/MAJOR findings and repeat review for affected portions. Check the final MP4: codec, 1080×1920, 24 fps, frame count, duration equals narration, audio present, and no unintended jumps (large differences between neighboring frames outside subtitle/transition changes). Leave only the final MP4 in videos/. Report honestly what was reviewed visually/by numbers and what was not (the agent cannot perceive motion or audio in real time).

## User revision lessons (inherited; apply from the start)
- Walking: step phase follows distance traveled; legs move in the travel direction; vary speed/start/phase between people; maintain a steady pace (≈230 px/s); arms swing opposite the legs; keep characters separated.
- Objects rest on surfaces; hands do not pass through furniture; question/exclamation marks sit near the character's head; characters do not disappear without reason.
- Sleeping/lying poses must read clearly (head, shoulders, arm, breathing).
- Every location needs meaningful detail; blank backgrounds are defects.
- Use brand and technical names from the script.

## Profanity (required)
- Remove profanity from scripts completely: rewrite the sentence to preserve its meaning without profanity. Do not replace it with a softened synonym, asterisks, or beeps.
- If a sentence loses meaning without profanity, shorten it to a neutral formulation; preserve relevant numbers and facts.
- Subtitles and narration must match the cleaned text.

## Environment
Windows 11; ffmpeg/ffprobe, Node, and Python on PATH; Chrome at C:\Program Files\Google\Chrome\Application\chrome.exe; install puppeteer-core with npm i puppeteer-core in the project folder; keep the faster-whisper virtual environment in a temporary folder (if av fails, decode audio with ffmpeg and pass the array).
