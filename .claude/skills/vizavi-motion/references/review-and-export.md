# Iteration, Review, and Export

This is a working review of core mechanic 3, not a quality certificate based on the existence of code.

## After the first build

The first result is an unfinished internal draft. Watch the complete video at normal speed, then inspect each scene and transition. If audio is present, listen to the complete mix and relevant individual layers. Record material findings as: **interval → observation → cause → specific fix → recheck**. Do not imitate revisions just to increase the iteration count; if no defects are found, state exactly what was reviewed.

Check:
- whether the idea and causal through-line are clear, the character is recognizable, and the piece develops instead of idling;
- whether camera, shot size, perspective, and layers guide attention; whether motion and transitions feel smooth;
- whether typography acts meaningfully and required words remain readable;
- whether shape, lighting, shadows, materials, identity, and contact are preserved, with no artifacts, accidental crops, or layer conflicts;
- whether blur and focus fit the motion/depth without hiding what matters;
- whether music and SFX support style, rhythm, and events, with no sync problems, clicks, or cutoffs;
- whether the format, duration, frame rate, silent/offline mode, and other explicit requirements are met.

Fix material causes, review changed sections with adjacent phases, then watch the complete video again. After simplifying, compare against the brief: “cleaner” is not acceptable if required characters, text, environment, or action disappeared. Finish when mandatory requirements are met and checked, material defects are fixed, and remaining ideas are optional stylistic alternatives.

## Implementation and finished MP4 by default

When HTML/CSS/JavaScript, SVG/Canvas, and a custom controlled timeline can meet the quality bar, prefer that direct approach. Do not require Remotion, Hyperframes, or another framework in advance, and do not install dependencies by template. This is a preference, not a ban: Three.js, Remotion, Lottie, audio libraries, and other suitable tools are allowed when genuinely needed. Choose based on result quality, required capabilities, available environment, and complexity; do not claim vanilla is always better.

Web Audio API is a built-in browser API, not a synonym for an audio.js library. No particular music generator or synthesizer is required: use an appropriate permitted method; use audio libraries only when needed. Do not restructure an existing project or a user-selected stack just to follow this preference.

Default deliverable is a finished MP4: **1920×1080, constant 60 fps, H.264, compatible yuv420p**, with **AAC audio** unless the user requested silent. Also preserve editable HTML/JS and other source files. Make 4K on request; explicit size, fps, duration, codec, or silent requirements in the brief override defaults. Do not label a file 4K/60 fps or a finished MP4 if the actual file differs.

Reliable export without a mandatory framework:
1. Fix the controllable timeline and frame grid. Render **all** frames reproducibly at times i / fps, including complex motion and transitions; verify sequence completeness and order. With another engine, provide equivalent reproducibility instead of recording realtime playback with dropped frames.
2. Create and mix music, SFX, and speech when present into an actual exportable audio track. Align starts, offsets, accents, and endings to the shared timeline. A Web Audio realtime preview does not guarantee audio in the MP4: produce a usable audio file/buffer with an available offline render, recording, or equivalent reliable method, then inspect its contents.
3. Combine the frames and complete audio mix with FFmpeg or an equally reliable pipeline. Preserve requested frame rate and timing. When muxing, explicitly include the intended video and audio streams; do not lose speech, music, or SFX or replace the full mix with a single effect. Do not add audio to a silent export.
4. Align opening and ending tails to the brief before muxing. Do not cut off the final scene, speech, or music ending just to force equal stream durations, or extend the video with a random audio tail. Do not apply -shortest blindly if the shorter stream will cut off the intended ending.
5. Check the **finished decoded MP4**: actual codec/pixel format, resolution, constant frame rate and timestamps, frame count and exact duration, AAC/required audio, AV sync, opening, ending, and scene boundaries. Watch and listen to the final mix with the video; the source preview does not prove audio exported successfully.

If the environment truly cannot render, encode/use FFmpeg or an equivalent, or deliver the file, state the specific blocker, completed work, and actual format. Preserve and provide source files and available playback/export instructions; do not present HTML as a finished video. This is an exception for a confirmed limitation, not a normal shortcut around the required MP4. Do not install an unavailable framework automatically to bypass a limitation.

## Review the deliverable

After encoding, open and decode the final export; review its motion and sound, not just HTML or source PNG/WAV files. Check opening/ending, neighboring frames on both sides of each scene boundary, readable holds, and fastest motion. Contact sheets help evaluate composition, dense frame sequences help assess a cut, full playback helps assess rhythm and smoothness, and listening helps assess sound. These types of evidence are not interchangeable.

If music sync is used, compare selected transitions/actions with perceived accents in the **actual track** and decoded export frames, including audio offset after mux. Watch and listen at speed, then review the complete mix with video: check for offset, repetitive SFX, and loss of meaning/readability/speech to hit the beat. Numeric marker alignment does not prove ideal sync; if playback/listening is unavailable, leave this item unchecked.

At a constant 20 seconds and 60 fps, expect 1200 frames on the grid 0..1199/60; renderAt(20) is not an additional video frame. Twenty seconds is only an example, not a required length. The default 60 fps changes when the brief explicitly says otherwise. Distinguish audio-stream presence from audio quality: a silent stream cannot PASS as an audio result, while AAC presence alone does not confirm audible music/speech or balance.

For a controlled timeline, repeat a frame after cold seek, reverse seek, and navigation from elsewhere. Analytical state, baking, or deterministic replay is needed for simulations and cumulative effects; a random seed alone is not enough. Compare source and final file hashes when version preservation matters. Do not call previous shortcomings “without the skill” if the skill was applied.

## Honest statuses

Distinguish: **implemented**, **run and checked**, **visible in frames**, **checked in motion**, **listened to**. Parameters or general impression do not give PASS to an unchecked item. If a tool is unavailable, name the specific unchecked property and why; provide the available artifact with an accurate status, not as if it passed artistic review. Do not invent playback, execution, or skill effectiveness.

If required quality cannot actually be achieved in the available environment, state the exact blocker and completed parts. Do not hide it after claiming completion. If an external action has an uncertain result, determine its outcome before repeating it. Do not ask for new authorization for ordinary reversible work already authorized.

Do not use repeated strobing as a substitute for energy. Check risky brightness changes in the exported video; reduced motion and absence of errors do not prove formal flash safety. Do not claim standards compliance without the relevant analysis.