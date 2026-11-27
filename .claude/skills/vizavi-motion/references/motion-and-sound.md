# Motion, Optics, Typography, and Sound

Apply these techniques according to the chosen storyboard. The goal is the quality described by core mechanic 1, not simultaneous use of every technique.

## Camera and depth

Separate trajectory, speed, orientation, target, FOV, and focus. Design one long, coherent trajectory with speed waves; do not concatenate identical ease-in-out moves that stop at zero on every accent. At transitions, check position, direction, screen-space speed, and acceleration. During readable parts of an active scene, a large move should settle into a calm arc/drift. Character tracking can coexist with visible environmental parallax. A motivated editorial cut does not need continuous world coordinates between different locations.

Separate foreground, middle, and background by scale, relative motion, overlap, and perspective. Protect silhouettes and text from accidental occlusion. Attach a label near a moving 3D object to the projection of its anchor, preserving frame margins without jitter or lag.

## Optics and materials

- Motion blur reflects relative screen movement over exposure. A tracked sharp character may have a blurred background. Subframe sampling or a suitable renderer are tools, not proof of the effect. Blur should ease during deceleration.
- Depth of field highlights a chosen depth. During a push-in, focus should follow the meaningful detail without accidental defocus. Near/far layers may soften while text and character remain recognizable. Do not create artificial illegibility in flat UI just to check a box.
- Radial/zoom blur is a separate stylistic accent, useful for depth or fast cards. Do not call it depth of field or temporal motion blur. Do not apply maximum blur throughout the video.
- Shape is communicated through geometry, lighting, normals, thickness, contact shadows, and occlusion. Highlights, grain, and particles do not fix incorrect construction. Texture and shadows should follow the object and light.

## Typography and rhythm

Choose an expressive available font or a consistent pair; check specific glyphs, Cyrillic, weight, line breaks, and whether the font file may be used. If external fonts are disallowed, use permitted system fonts or custom geometry. First design a readable final layout, then animate letters/words: assembly, width changes, masks, spatial relationships, interaction with objects. The effect should serve a semantic purpose.

Combine anticipation, action, contact, reaction, and decay with varied masses and curves. One main accent can have coherent secondary layers. If everything competes for attention, adjust phase, scale, depth, and contrast. Do not fix pacing by deleting required content or speeding it until unreadable. Avoid repeated flashes as a substitute for energy.

## Music and sound design

Unless the user chooses silent mode, music and SFX are part of production from the start. Choose a creation method according to permitted resources and the task: musical character and result matter, not a particular service or synthesizer. Music should have a suitable motif/groove, development, contrast, and ending; a collection of whooshes and hits is not a composition. Tie SFX to motion, contact, material, and transitions instead of adding them randomly.

Drive sound and picture from the same events. After a speed ramp, recalculate the actual accent time; do not unintentionally change the entire music tempo/pitch. Listen to the complete mix and necessary layers; check balance, clipping, clicks, sync, and tail. Technical metrics do not prove musical quality. If audio was not created or heard, state those statuses separately.

### Editing to expressive accents

Plan around musical accents while designing sound and animation: a highlighted note, impact, phrase/harmony change, pause, or returning rhythm may support a cut, scene reveal, angle change, contact, or movement ending. This is an occasional deliberate technique, not a requirement to cut on every beat. A piano note is only an example, not a required instrument or genre.

After selecting/creating the **actual audio track**, mark the timecodes of audible accents and corresponding visual events. For selected points, record the perceived peak/accent onset, target visual action, and nearest suitable frame: frame / fps. Account for real audio start/offset and editorial shifts. BPM, a calculated beat grid, or the start of an SFX file is not enough: a musical peak, attack, and visual climax may occur at different times. Compare by listening and watching at frame-level accuracy, not from one waveform.

If a sync point does not work, gently adjust shot duration, trajectory, reveal/landing timing, or arrangement within the brief. Do not create unnatural speed or damage pacing/speech clarity to fit a grid. Meaningful events, readable text, voice, and explicit no-music requirements outrank mechanical beat matching; in silent mode, do not apply music sync.

Coordinate SFX with musical gestures: a sound may support the accent, complement it, or leave it space. Do not layer the same whoosh on every transition or duplicate every musical impact with an effect. After replacing/trimming a track or applying a speed ramp, update the accent map. Review chosen sync points and final mix with video; do not claim perfect synchronization without that review.