# SaaS/UI Motion — Product Interface Animation

An optional module within vizavi_motion, not a separately installable skill. Apply it to product/interface demonstrations or relevant parts of a tutorial demo. SaaS/UI motion is shorthand for staging an interface; it does not mean that the SaaS business model imposes a strict art style.

## Origin and scope

Adapted from user-provided archives higgsfield-motion-saas.skill and higgsfield-motion.skill, received on 2026-10-15; both files were received and read for this revision. This is not a claim of official Higgsfield authorship. Source pointers: higgsfield-motion/references/production-lessons.md, lines 318–325 and 351–375; higgsfield-motion-saas/references/client-taste.md, line 63; higgsfield-motion-saas/references/transitions.md, lines 45–68 and 95–100; higgsfield-motion-saas/references/techniques.md.

techniques.md names MahdiEdits lessons “Top 3 Most Used SaaS Video Transitions”, “Overlapping Keyframes”, and “Overlapping Keyframes in 3D”, but their public URLs are unconfirmed. Measurement/viewing status in the archives belongs to their author and was not independently verified here. Adapt principles, not other people's implementations, branded palettes, project preferences, mandatory duration, BPM, engine, or tool installation. The spatial-mode and tutorial-demo rules below were supplemented by the current user request.

## Action and result

For each segment, choose a clear task: select an item, change a setting, drag a card, rearrange a panel, start a process, or show a result. Show one plausible application with consistent data and states, not an unrelated decorative card with a new heading in every scene. Keep a consistent hierarchy of cards/panels/buttons, corner radii, shadows, and line weights. Highlight only a few main controls in one action (the source suggests 1–3 as a guide, not a universal quota). Do not present demo data as actual attributes or metrics of an existing service.

The cursor leads the action: hover → target response → click/grab → change → readable result. It should not fly randomly over a passive screen. The arrow tip/hotspot determines the hit, not the sprite center. Show a brief readable hover before the click and a visible causal state change afterwards. Keep the cursor sharp and fully visible during the click; do not cover the button label, result, or readable numbers.

Button and object states must be causally connected: hover, pressed/dragging, processing, success/selected, or another meaningful set. Do not show success before processing is complete. A chart, percentage, and other indicators of one operation should share progress. Do not present an editorially shortened wait as the product's real speed; label the compression/demo when needed.

For drag, fix the grab point and cursor-object offset: the card lifts and follows an arc, the destination highlights, and on drop the card gently scales down into the slot. Follow/lag may convey weight and inertia, but not loss of control: the main object stays controllable; delay/catch-up should be justified; neighbors react after the event. Drop, snap, and residual damping end in a stable, clear layout. Do not apply the same spring to every layer.

Choose duration and amplitude for the pace, frame size, and reading window. The original client-taste.md includes a cursor move preset of 0.6–0.9 s on a small arc, a slight compress on click and recovery afterwards, with entrance/exit beyond the frame. This is an example, not a universal requirement; entering/exiting the frame is compatible with full visibility at click time. Do not mechanically apply numeric presets to every scene.

Use a few functional micro-reactions: target highlight, state change, nearby card response, panel reveal. They support the main point rather than compete with it. Motivate a move to detail through action; leave time to read text. Connect selected expressive cuts, reveals, and movement endings to actual musical/SFX accents according to the [motion and sound module](motion-and-sound.md), not every beat.

When an object passes between scenes, align screen position, size, and state; leave no duplicate or ghost remnant. The result should emerge from the element that triggered it; cards spread along soft arcs. During a morph, change real shape/layout dimensions; do not stretch all UI, text, and radii together. Preserve interface identity as it moves from flat to spatial representation.

The camera supports the action: follow the cursor, push toward a click, pull back to show the result, or travel around separated layers. A close-up makes detail readable; a wide shot explains the application context. Choose a motivated camera gesture rather than doing all of these in every segment.

## One interface in 2D, 2.5D, and 3D

| Mode | What should actually change |
|---|---|
| 2D + SaaS/UI | Flat panels, cards, buttons, and content. Do not imply volume through arbitrary thickness; cursor action and state change remain the semantic focus. |
| 2.5D + SaaS/UI | The same flat panels are separated in depth. Camera movement reveals relative placement, perspective, occlusion, and parallax. Panels do not gain real sides or extrusion. |
| 3D + SaaS/UI | Recognizable objects gain real geometric thickness, edges, and sides. Lighting, normals, shadows, and spatial orbit/fly-through establish volume, not just scale or drop shadow. |

For the selected tutorial demo, carry the same object IDs, composition anchors, colors, content, and operation result across the final three segments. The viewer should see one interface's spatial representation change. This is specific to that demo, not a ban on changing the interface in another brief.

## Coordinates and reproducibility

Explicitly separate world-space UI and screen-space overlays. If the cursor interacts with a world object, compute its screen position from the current projection of its anchor, accounting for camera, viewport, aspect ratio, and window scale. If the cursor is fully screen-space, evaluate its target in that same screen system. Do not mix CSS pixels, video-frame coordinates, and world units without conversion.

The tutorial demo's screen-space segment label keeps its position and style as the camera moves. Labels near world-space objects may follow their projection; check margins, occlusion, depth, and camera exit. A 3D panel must not accidentally cover a cursor staged as an overlay or intersect required text.

For reproducible video, animate cursor, grabbing, states, and delays on one controlled timeline. Live user input is not needed for playback. Compute state from time or a reproducible bake/replay, including reverse seeking; do not depend on previous mouse events or the number of frames already played. Full functional QA for rapid repeated clicks, resizing, and reduced motion is needed when building a live app; do not turn an ordinary video demo into an interactive-product build.

## Review

At speed and around transitions, check action clarity, grab accuracy, drop completion, synchronized progress/states, consistent interface identity where required, distinction among the three spatial modes, projection during camera movement/seeking, and overlay readability. Then review the final decoded export with sound. A visible cursor, translateZ, or extrusion parameter in the code does not prove the visual result.