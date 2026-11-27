# AI Agent Instructions for 2D Video

These rules apply to all tasks and projects inside 2d-video. Before generating a video, read PROMPT_2D_VIDEO_HIGH_QUALITY_RU.md and follow its requirements without asking the user to paste the prompt again. These persistent instructions apply to all new videos; use only narration, scripts, and references supplied for the current task.

## Projects and source files

- Save only one complete final MP4 in the output folder C:\Users\muham\youtube-video\tiktok (or the location specified by the user). Do not put previews, contact sheets, silent renders, render chunks, audio, reports, version copies, or project folders there. After successfully reviewing the final file, remove files and folders created for this video from the output folder, leaving the final MP4. Do not touch unrelated files.
- projects/when-signal-fails is a separate “72 Hours Without Signal” video project, not a general template. Do not replace or reuse its materials for another video.
- Create a separate working project under projects/ for every new video, with its own configuration, timeline, and scenes; do not overwrite an existing project. Keep original narration and files needed for later edits/rebuilds inside the working project only. Use temporary previews, contact sheets, silent renders, and render chunks for internal review; delete those temporary files after review. Deliver only the complete final MP4 unless the user separately asks for other materials.
- The repository root may contain leftovers from an earlier video, including transcript-base.json, transcript-base-rerun.json, sample20.mp3, and debug.log. Treat them as belonging to previous work; do not use them for a new video unless verified to match the narration attached to the current task.
- Use only narration and materials supplied for the current video or explicitly identified by the user. Do not pull material from Telegram, other chats, or unrelated projects.
- Preserve the original narration unchanged. If unspecified, use the narration's language, 16:9, and 1080p.

## Meaning, style, and quality

- First listen to the entire narration, transcribe it accurately, and align phrases to real timecodes. Do not distribute text evenly across the runtime.
- Before building scenes, prepare the complete table: timecode | phrase | visible content | shot/angle | movement. Every scene must illustrate the words at the corresponding time. Use a fitting setting for each location; do not repeat backgrounds, templates, or props without a story reason.
- Create cinematic, beautiful, professionally finished frames in expressive 2D/2.5D, with convincing depth and 3D/low-poly where the scene calls for it. Pay attention to composition, lighting, palette, materials, perspective, clean silhouettes, and coherent models.
- Action must feel alive and physically plausible: weight, support, contact, inertia, and natural completion. Camera movement does not replace character/object action. Avoid floating, clipping, intersections, stray protrusions, scale jumps, broken parts, flicker, and ragged edges. Do not hide defects with darkening, filters, or quick cuts.
- Characters should read as full people: featureless head, neck, body, clothing, arms, legs, and shoes; poses, gestures, and interaction with props must be clear. Do not replace a person with an envelope, icon silhouette, object, or abstract geometry. Main characters remain the focus; props must not hide heads or bodies.
- For paper collage, draw characters, environments, and objects with project tools (Canvas/code) when the user asks for hand-drawn visuals. Do not substitute generated images for frames. Keep recurring characters' models/clothing consistent; give each new location its own recognizable details and lighting.
- Do not add random decoration, unspoken facts, or irrelevant labels. Text, numbers, maps, and graphics appear only when meaningful and spoken.

## Required review before the final render

- For each new or substantially revised video, use a separate independent subagent named video_quality_reviewer with settings from .codex/agents/video_quality_reviewer.toml to review meaning, visual quality, movement, synchronization, and sound. Run reviews inside the working project; do not show intermediate review materials to the user unless asked. If the environment cannot select a named profile, run an independent subagent and give it that file's instructions. If subagents are unavailable due to environment limits, perform the same review yourself and state clearly that independent review was not performed.
- The reviewer must explicitly check for full human characters and readable actions in every meaningful shot; abstract props or character-free compositions do not count. Check subtitles against actual speech and word boundaries in previews; flag and fix low-confidence speech recognition before approval.
- After fixes, resubmit changed scenes for review. Do not describe unchecked segments as reviewed. Reviews are internal quality control; the user need not see the full table, contact sheets, and previews.
- Build scenes in batches and make a contact sheet. Inspect every sheet for phrase matching, shot variety, composition, clean visuals, and unjustified repetition. Check intermediate animation moments, not only still frames.
- Fix all mismatches, static/cardboard scenes, and visual defects; recheck the contact sheet and affected shots.
- Independently check the scene table, contact sheets, start, middle, key event, and ending; review the original narration and added sounds. Do not ask for approval of these materials before the full render if the user explicitly requested a finished video. After assembly, check duration, audio, frame rate, and visual artifacts; fix and recheck any defect.
- After review succeeds, leave only the complete final MP4 in the output folder. In your response, give its name and a link. Do not list or attach working files, reports, previews, or other materials unless the user asks.

