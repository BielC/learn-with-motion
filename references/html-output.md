# Standalone HTML lessons

Read this when the user requests an HTML page ad hoc. The normal explainer deliverable is a narrated video only. Using HTML/SVG internally to render that video does not require a user-facing page or this page's controls and interaction tests.

## Output contract

Create a complete UTF-8 HTML document with `<!doctype html>`, a descriptive title, `lang`, viewport metadata, and embedded CSS and JavaScript. Prefer one self-contained file that works offline when opened from `file://`. Embed the fixture and source excerpts rather than fetching adjacent JSON or relying on module imports, a development server, the inline widget runtime, or CDN availability. Keep source links clickable. If the actual lesson requires external assets, disclose those dependencies and include local copies when appropriate.

Use a readable page width, system fonts, responsive layout, visible keyboard focus, and light/dark contrast. The optional [assets/lesson.css](../assets/lesson.css) is a starting point; inline it into the delivered file. [assets/retry-trace.html](../assets/retry-trace.html) is a working standalone toy example, not source material for unrelated topics.

The default visual direction is **minimal editorial: warm paper, ink, generous spacing**. Default to a warm light canvas, dark ink, serif display typography with readable supporting text, fine rules, and restrained accents that carry meaning. Organize the explanation with typography, spacing, and clear diagrams. Avoid decorative AI branding, repeated rounded panels, and neon accents. Treat the provided CSS and toy example as implementation references rather than a fixed layout. Preserve an established visual direction unless the user requests a change; layout tests do not establish whether they like a design.

Include the bounded learning target, useful diagrams, any example being followed, explanations beside relevant state, and exact source/version context. Separate diagrams are welcome; a single persistent picture is optional. A requested webpage can be the complete explanation, with self-paced examples, linked diagrams, controls and source/code inspection. Choose navigation or scrolling when it supports a coherent learning progression; a webpage need not contain a film or serve as its companion.

When the requested page is a film player, the current diagram supplies context. Keep stage, captions, seek and playback controls visible together, preferably within one viewport. Keep the title compact and fit both width and height; clipping controls or shrinking a dense page is not a solution. Optional experiments, code, transcript and sources can open through deliberate controls rather than accumulating below the film. A detail dialog or alternate view should pause the film, preserve its position, support Close/Escape and restore visible focus. These player conventions do not require all explanatory webpages to use a player or prohibit purposeful scrolling. Preserve guided versus complete-explainer behavior from the main skill.

## Animation implementation

- **Default:** semantic HTML for controls/prose, SVG or DOM elements for the mechanism, CSS for layout and stable styling, and plain JavaScript for explicit lesson state and input changes. The Web Animations API suits small transitions; GSAP suits coordinated films and seeking. A UI framework is optional.
- Keep the mechanism's state separate from animation time: compute the next state from the fixture, render it deterministically, then animate the connection. Previous, next, replay, rapid clicks, and reduced motion must produce the same correct state. Cancel obsolete animations when changing state.
- **GSAP:** consider it for many synchronized movements, labeled timelines, or scrubbing where a custom timeline would become harder to maintain. Include a pinned local dependency when offline use is required. It does not replace the lesson state model or source verification.
- Use a UI framework only when an existing application or substantial UI warrants it. Reserve Canvas/WebGL for dense simulations or genuinely spatial content. Choose the smallest stack that makes the mechanism clear and maintainable.

## Video-style presentation

When HTML is requested, it can contain a video-style animated explainer as well as a manual trace. For an animated page, make the stage the main experience: choreographed scenes, clear diagrams, meaningful movement, timed captions, and visual focus on the current connection. Review the storyboard's relevance before narration. Avoid producing an article with a few animated decorations in place of the requested explainer. An ordinary video request still requires an actual rendered video.

Start paused with a useful opening frame. After Play, let the explanation run through coherent scenes without requiring Next for every operation. Provide play/pause, an accessible seek slider with elapsed/total time, replay, and playback speed. Mark useful chapter boundaries when the lesson has several mechanisms. Optional step controls can visit those boundaries. In complete-explainer mode, the learner can watch through without answering questions; pause for an optional prediction only when explicitly chosen. In guided mode, pause at the agreed teaching boundary before its unrevealed outcome.

Use a single master timeline for scene motion and captions. Derive visible state from the selected time so seeking directly to a frame, replaying, reversing a seek, and changing speed remain correct. With GSAP, labeled scenes and timeline controls can own playback; avoid side effects in callbacks that only occur during forward playback. A native implementation should likewise reconstruct the scene from time instead of chaining `setTimeout` calls. Keep conceptual states available when paused. Do not use scroll position as the playback clock.

For an audio-driven standalone film, reuse [the supplied player and viewport shell](player-runtime.md) instead of recreating its clock, controls and page layout. The topic-specific renderer remains responsible for source fidelity and meaningful transformations.

Voice narration can be added when requested or useful and available; do not assume browser speech synthesis is reliable, offline, or synchronized. Captions should explain the mechanism without audio. If narration is included, keep it synchronized when pausing, seeking, and changing speed. Follow [film-direction.md](film-direction.md): video is the default, HTML is ad hoc, and dual delivery requires a request for both. For requested dual delivery, share the scene/script source, render an actual downloadable video, and verify it separately. Embed essential narration in the standalone HTML; a download link to a companion MP4 may remain a sibling asset. Explain that moving the HTML alone will not carry that download target with it.

For a manual trace, previous/next/replay can be sufficient. Honor `prefers-reduced-motion` in either presentation by offering the same conceptual states and captions without sweeping movement. The reduced-motion version must remain usable, including chapter or state navigation.

## Verify and open

Open the actual delivered file in a browser and exercise important branches, next/previous/replay, keyboard use, narrow layout, and reduced motion. For a film player, also check pause/resume, arbitrary forward/backward seeks, speed changes, captions, end/replay, and that stage and controls fit together at desktop and narrow sizes, including a short window. Check that optional detail views return to the same paused position and visible focus. For a self-paced webpage, inspect its reading/navigation flow and confirm that scrolling or switching views preserves the example's connections. Verify offline operation, no runtime errors and no network requests for essential content. Distinguish browser checks from executing the source system and from evidence of learning.

On macOS, open the saved HTML using an argument-safe process call such as:

```python
subprocess.run(["open", "-a", "Google Chrome", str(html_path)], check=True)
```

For work or private material, use the browser profile required by the local workspace instructions. Do not bake account names or profile directories into a shared skill.

Respect a different browser explicitly requested by the user. Do not change default-browser settings. Return the absolute file link and a short statement of what was opened and checked. If Chrome cannot launch, retain the artifact and report that limitation.
