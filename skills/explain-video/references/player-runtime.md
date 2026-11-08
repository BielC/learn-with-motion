# Internal render clock

Read when using [film-player.js](../assets/film-player.js) in an HTML/SVG authoring document. It provides a shared audio clock and deterministic export clock without a package dependency. It supplies no scenes or video encoder. Omit user-facing controls from an internal rendering document when unnecessary.

Keep source data and a pure renderer separate from the clock:

```javascript
const CUES = [{id: 'first', start: 0, voiceEnd: 4.2, end: 5}];
window.lessonInspection = createMotionPlayer({
  audio: document.getElementById('voice-track'),
  cues: CUES,
  duration: 5,
  render(t, frame) {
    // Reconstruct all scene state from time and the source fixture.
    // frame: {cue, index, progress, reducedMotion, exporting}
  },
  controls: {caption: null}, // When the renderer owns phrase subtitles.
});
```

Derive `voiceEnd` from measured speech, not estimated speaking speed. Within a paragraph, use measured local landmarks for consequential reveals. Add the cue's timeline offset explicitly. Missing, ambiguous or out-of-range landmarks must fail before rendering rather than silently use scene start. The Qwen helper's optional bookmarks are described in [narration.md](narration.md).

Call `lessonInspection.exportFrame(frameNumber / fps)` for each captured frame. This pauses playback, cancels its animation loop and adds `body.export`, giving the export clock exclusive control. Pending media events cannot overwrite exported frames. Use `frame.exporting` to select the fixed film composition. Mux the same measured audio track after capture; do not use real-time screen recording as a deterministic export.

`exitExport()` restores paused interactive authoring mode. `frame(t)` seeks that mode, and `destroy()` removes listeners. Do not add another audio or animation loop around this helper. Keep changed-input authoring experiments outside a fixed narrated sequence unless the narration also adapts. Inspect decisive decoded frames after export as described in [film-direction.md](film-direction.md).
