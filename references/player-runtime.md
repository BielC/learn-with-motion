# Reusable film player

For a film authored in HTML/SVG, [assets/film-player.js](../assets/film-player.js) can supply the audio clock and exclusive deterministic export clock inside an internal rendering document. The default deliverable is the rendered video; this asset does not require a user-facing HTML page or player controls. When HTML is requested ad hoc, inline it into that page to reuse playback, reverse seeking, keyboard handling and reduced-motion context. Adapt scenes and layout instead of rewriting these mechanics. It has no network or package dependencies. A manual step-through lesson does not need it.

Keep source-grounded lesson data and a pure scene renderer separate from the player:

```javascript
// Measured audio timing, not estimated speaking time in a final voiced film.
const CUES = [{id: 'first', start: 0, voiceEnd: 4.2, end: 5,
               cap: 'Phrase-level caption.'}];

window.lessonInspection = createMotionPlayer({
  audio: document.getElementById('voice-track'),
  cues: CUES,
  duration: 5,
  render(t, frame) {
    // Reconstruct ALL scene state from t and your fixture.
    // frame: {cue, index, progress, reducedMotion, exporting}
    // progress spans the voice interval; compose separate operation timings
    // when a cue contains more than one consequential change.
    // Choose a settled conceptual state when frame.reducedMotion is true.
    // Use frame.exporting to choose the film's fixed landscape composition.
  },
  onError(error) { /* Show a useful playback error in the page. */ },
});
```

Default optional control IDs are `play`, `replay`, `seek`, `back`, `forward`, `speed`, `voice`, `clock`, and `caption`. For a requested user-facing page, use semantic buttons, a labeled range input, and a speed select. Include 0.8× and 0.9× alongside 1× and the other offered speeds; these offer finer slow-playback control. Override individual elements with `controls: {play: anotherButton}`. The page owns any styling, chapter navigation, source links, transcript, and changed-input experiments. Keep those experiments outside the narrated sequence. Omit user-facing controls and experiments from an internal video-only rendering target when unnecessary.

The default caption is `cue.cap`. Supply `captionText(t, frame)` for phrase-level timed subtitles, or `controls: {caption: null}` if the scene renderer owns them. In a silent edition, ensure the full explanation remains available rather than keeping only captions intended to supplement voice, and omit the voice toggle when audio is only a silent clock.

`lessonInspection.frame(t)` seeks the playable page. `exportFrame(t)` pauses playback, cancels its animation loop, adds `body.export`, and gives the export clock exclusive control. Capture frames at `frameNumber / fps`, then mux the same audio track. Pending media events cannot overwrite export frames. `exitExport()` restores paused interactive mode; `destroy()` removes listeners. Do not attach a second audio or animation loop around the player.

The renderer owns the visual argument. This asset does not supply causal scenes, correct source interpretation, responsive composition or video encoding. Preserve an SVG title/description when replacing its contents. Check representative intermediate states, actual narrow-screen label sizes, and decoded video frames as described in [film-direction.md](film-direction.md).

## Single-viewport host

When a viewport film player fits the chosen explanation, inline [film-viewport.css](../assets/film-viewport.css) and [film-viewport.js](../assets/film-viewport.js) to reuse viewport fit, compact chapter menus, full-screen control and optional detail dialogs. This is an optional film host, not the required structure for every explanatory webpage. Inline the script after assigning `window.lessonInspection`. Keep the scene's visual tokens (`--paper`, `--ink`, `--rule`, `--serif`, `--sans`) and its own SVG/caption styling. The shell adapts landscape films to available width and height; a portrait renderer supplies its own narrow composition. Export mode retains a 1280×720 artboard.

The required layout hierarchy is:

```html
<html class="motion-document">
<body class="motion-view">
<main class="motion-app">
  <header class="app-header"><h1>Lesson title</h1><!-- compact menus --></header>
  <div class="stage">
    <section class="film"><svg id="scene"></svg><p id="caption" class="caption"></p></section>
  </div>
  <div class="controls"><!-- labeled seek and the player controls above --></div>
  <!-- Optional dialog, embedded audio, player, scene and viewport scripts. -->
</main>
</body>
</html>
```

Optional chapter navigation uses `details.menu#chapter-menu` containing a `summary` and `nav#chapters`. A `button#fullscreen` toggles the app's full-screen mode. The viewport helper does not create chapters or explanatory content.

For optional details, buttons with `data-panel="explore|code|sources|transcript"` select matching `section.resource-panel#resource-NAME` elements inside `dialog#resource-dialog`. Give the dialog an accessible `h2#resource-title`, `button#close-resources`, optional `nav.resource-tabs` with the same data-panel buttons, and a `.resource-body` around the panels. The helper pauses playback, shows one panel, keeps long content scrolling inside that optional view, and restores a visible opener on close. It blocks media keyboard shortcuts while reading details. Do not append those panels below the player as a scrolling article.
