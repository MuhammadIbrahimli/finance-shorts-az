---
name: vizavi-motion
description: "Create and refine original motion videos, product animations, and kinetic typography, from concept and dynamic storyboard to reviewed export."
metadata:
  version: "1.6.1"
  display_name: "vizavi_motion"
---

# vizavi_motion

The three mechanics below are the foundation of this skill. Additional modules help carry them out; they do not replace them or impose a required template. The user's explicit brief, format, duration, audio, and permitted resources take priority over defaults. A simple idea is enough: make production decisions independently instead of asking the user to fill out a technical questionnaire. Do not invent real product attributes, prices, or confirmed preferences.

By default, prefer direct HTML/CSS/JavaScript, SVG/Canvas, and a custom controlled timeline when they are sufficient for the desired quality. Appropriate libraries and engines are allowed when genuinely needed; do not choose a framework or install dependencies in advance without a reason.

## 0. Channel overrides (finance-shorts-az) — take precedence over the sections below

This skill is used only for videos in this repository. When the defaults below conflict with channel rules, follow the channel rules in AGENTS.md and CLAUDE.md:

- **Format:** 9:16, **1080×1920**, **24 fps**, H.264 (libx264 -preset slow -crf 22), yuv420p, AAC. The 1920×1080 and 60 fps defaults do not apply here.
- **Audio:** narration only (Gemini TTS). **No music or SFX.** Section 1's music and sound-design advice does not apply.
- **Style:** paper collage (AGENTS.md, references in references/2d-video/sheets/): paper texture, irregular edges, soft shadows, muted palette, 3+ parallax planes. Flat vector fills without texture are not acceptable.
- **People:** when the story is about people, show complete characters (featureless head, body, arms, legs, clothing). Abstract diagrams may appear as inserts, not as the entire frame.
- **Subtitles:** follow AGENTS.md karaoke specification; panel centered near y≈1540; text matches the script; timings from work/words.json.
- **Scene contract:** window.renderAt(t) is a pure function of time; use window.DURATION_SEC and templates/scene_template.html.
- **Review:** all three agents in .claude/agents/ are required: video-quality-reviewer, art-director, subtitle-auditor. The first pass is not final.
- **Delivery:** provide the Azerbaijani block (Başlıq, Örtük üçün prompt, Təsvir with 5 hashtags), as described in AGENTS.md.

## 1. Default quality

Create lively, rich, detailed animation. Keep the camera moving smoothly during active narration: controlled acceleration and deceleration, coherent trajectories, motivated tilts, diagonals, slight rotations, and orbits. Show perspective depth and relative motion between foreground, midground, and background. A single linear zoom across a flat composition is not a substitute. A technical pause or a final readable frame does not need meaningless motion.

Typography participates in the action: use expressive type and shape, and animate letters, words, and spatial form rather than merely revealing a caption. Objects should convey weight, inertia, material, lighting, contact, and secondary reactions. Vary emphasis and shot size without long idle holds or chaotic flicker; preserve visual richness through hierarchy rather than removing the environment.

Use motion blur based on relative motion and controlled depth of field in spatial or close shots. When useful, add radial blur for cards or deep scenes; it does not replace depth of field or motion blur. Preserve readability and recognizability. By default, create suitable music and sound design synchronized with rhythm, action, and style, without requiring a particular generation tool. If the brief requires silence, omit audio. Do not call a silent result narrated. Details: references/motion-and-sound.md.

Periodically connect transitions, cuts, and meaningful actions to expressive accents in the actual music/SFX. Treat these as deliberate sync points, not a requirement to change the shot on every beat.

## 2. Direct before implementation

Before full production, develop one original concept/thread and a complete dynamic storyboard. For **each scene**, propose 3–5 meaningfully different short creative options and choose the strongest one for the overall piece. Concise options, the selected direction, and a practical storyboard are enough; internal reasoning is not required.

For each shot, define the semantic emphasis, composition and layers, action/object change, text and its motion, camera, lighting/focus, entry from the previous scene, exit into the next scene, sound, and rhythm. Scenes should advance the story causally. A circle, letter O, or portal is only one possible technique; do not repeat it automatically. You may combine 2–3 techniques when they form one coherent action. Before expensive production, test the main technical or artistic risk with a short prototype. Details: references/storyboard.md.

## 3. Required iteration after the first build

By default, treat the first build as an unfinished internal draft, not a final deliverable. Watch the entire video, every scene, and transitions; when audio is present, listen to the music, SFX, and complete mix. Check meaning, dull pauses, pacing, camera, readability, shape, artifacts, cuts, and sync. Fix the underlying causes, then review the changes and the complete video again. Do not claim the skill's effectiveness is proven by the presence of these instructions or one successful frame.

By default, deliver a finished **MP4: 1920×1080, 60 fps, H.264, yuv420p, AAC audio**, unless the user requested silence. Also save editable HTML/JS and other sources; provide 4K on request. Explicit brief parameters override defaults. An HTML preview is not a substitute for the finished video.

Also inspect the **final decoded export**, including its beginning, ending, scene boundaries, and technical properties. Code, a contact sheet, and a frame count do not substitute for perceiving motion and sound. If a required tool is unavailable, state exactly which property was not checked and provide the available artifact with an accurate status; do not claim it passed that check. Finish once material defects are fixed and brief criteria are met; optional stylistic alternatives do not require endless revisions. Details: references/review-and-export.md.

### Additional modules — use only when relevant

- Video or multiple references: analysis and combination — references/video-references.md.
- Image series, characters, alpha: identity consistency — references/image-continuity.md.
- Existing 3D models, materials, joints: 3D assets — references/models-3d.md.
- Product interface animation, cursor, and states: SaaS/UI motion — references/saas-ui-motion.md.
- Consistent styles and verified sources: registry — references/styles-and-sources.md. The six selected parts of the tutorial demo apply only to that demo; for other videos, follow their own brief.
