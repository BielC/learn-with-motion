# Directing an explanatory film

Read this for video-style lessons, narrated videos, or substantial changes to an animation's visual treatment. The target is a visual argument the learner can follow, not the surface appearance of another creator's work. Use the default warm-paper/ink direction unless the learner chooses another style.

## Choose the output for the explanation

- **Video is the default deliverable.** Compose a narrated explanation with deliberate visual pacing and deliver an actual MP4 or another requested video format.
- **Interactive webpage is ad hoc.** Build it when the user requests a page, asks for interactive exploration, or explicitly chooses HTML for the current task. It can be the complete explanation and does not require a film. Include playback controls when it contains a continuous animation.
- **Both requires a request for both.** Reuse scene code, cue script and renderer where applicable, and verify each requested format separately.

HTML/SVG with a time-driven renderer works well for software flows and data. It may be an internal rendering document without a user-facing page, experiments, or a polished player. Manim can fit equations, geometry and mathematical transformations. Neither supplies the explanation.

## Reuse the production work

Start from the learner's last approved artifact when it is available. Preserve its visual tokens, player, audio clock, cue schema, deterministic export, and working controls unless the new topic needs a different capability. Change the source-grounded example and visual argument; avoid re-solving playback, narration integration, and layout on every lesson. Reuse causal patterns where they fit: aligned before/after lanes, persistent entities merging into a record, a deciding comparison, and an interval expanding into output units. Choose a new representation when the mechanism demands it rather than forcing every topic into the same diagram.

When using the existing HTML renderer, [player-runtime.md](player-runtime.md) documents the dependency-free clock/export asset; reuse it internally or in an explicitly requested page. User-facing playback controls and viewport layouts are optional for a video-only render target. [visual-patterns.md](visual-patterns.md) gives concrete ways to preserve identity through a reshape, incremental append and deferred evaluation. Read the matching pattern when these mechanisms occur.

Review the storyboard's relevance before generating narration, following the main skill: each section should advance the central question, with incidental or repetitive detail cut, merged, or moved aside. Use silent previews while revising the edited script and storyboard, then generate narration with the selected local voice. This is an authoring self-review, not a user approval gate. Reuse cached speech for visual-only edits and render the full video after representative frames are ready. For frequently revised long scripts, cue-sized caches limit regeneration to changed speech. If a paid provider was explicitly chosen, retain available request-level credit metadata without polling balances. Separate narration credits, AI authoring usage, and local rendering when reporting cost; local speech removes TTS API charges, not authoring or compute costs.

## Find the picture before writing the script

The usual failure is a film whose captions do the reasoning while the picture supplies no inspectable connection. First identify the actual subject and explain what it does, why someone needs it, and where it fits. Use a concrete situation or visible contrast when it helps ground that explanation. Then introduce the architecture or design question, using suitable diagrams to connect component responsibilities, flow, and tradeoffs. Separate diagrams can be clearer than one persistent picture; keep their names and conceptual connections understandable without forcing continuous zooms or morphs. Choose deeper operations only where they help answer that question. A clear held diagram can carry the argument; continuous motion is not the goal. Decide three things before writing narration:

1. **The starting context, design question and useful level of detail.** What does the core idea mean in ordinary language, what problem makes it useful, and which details explain the solution? Introduce needed background before relying on it, including when a later section changes topics. When outputs or counts matter, establish what one unit means before relying on it. Do not introduce dimensions or calculations solely because they appear in the source.
2. **Representations whose relationships or changes carry the claim.** A component map with meaningful connections, two memory lifecycles, aligned before/after flows, or an inspectable operation. Reuse a small set of diagram conventions where they fit, so each view does not require learning a new visual language. Include representative messages, records or other example content when it makes a flow meaningful; numerical toy data is optional. For a UI change, a simplified view of the actual interface may make the consequence clearer than an abstract box. Choose a separate diagram when it improves clarity. Keep terminology consistent and explain how each view contributes to the story.
3. **The connection the viewer should be able to explain.** Show how a component's role, retained state, or design choice produces the relevant behavior. Use a concrete input or numerical comparison when it clarifies that connection; neither is mandatory for every scene. For a change, keep the point of divergence and its consequence visible.

For a Mem0 repository link, introduce Mem0 itself. For example: “Mem0 is software developers integrate into AI applications to store and retrieve information from past interactions. It provides an open-source library and a managed service. In its basic chat example, the application sends conversation messages to Mem0 to create stored memories. For a later reply, the application searches those memories and includes relevant results in the input to the language model. The language model then generates the answer.” Verify this framing against the linked version, and distinguish the library from the managed service where relevant. Build the architecture explanation on that concrete role. A general story about AI remembering preferences would leave the requested project unidentified. Support the framing with source pointers in authoring notes, outside the watching surface.

Then storyboard each beat as: the claim, the visual evidence to inspect or the change to follow, and the source line that supports it. At section boundaries, make clear what the previous section established and why the next question follows. A spoken bridge or shared example can provide this connection across separate diagrams; a title alone may leave the reasoning disconnected. A held frame is useful when it gives the learner time to trace a relationship, read an equation or compare states. Twenty to thirty seconds of stillness can be appropriate; there is no duration ceiling that establishes a quality failure. Add motion when it exposes a missing operation or connection, rather than to meet an activity quota. A short representative slice is a good test of a new direction before building a full film.

In those same notes, identify a plausible wrong reading of the important diagrams and how the picture prevents it. For example, a lost reply must not look like a failed server operation. Distinguish literal relationships from schematic spacing, invented values or metaphors when that difference affects the explanation. This is a small addition to the existing storyboard review, not a new planning document or a requirement to invent a misconception for every shot.

## Stage the mechanism

- Establish the idea's meaning and purpose before its internal structure, then introduce detail as it becomes relevant. Keep background tied to the situation being explained; a long generic preamble or glossary creates another detour. Separate diagrams are appropriate for distinct questions or aspects; switching views does not need a continuous geometric transformation.
- Keep identity through transformations: values travel into the structure they join, an interval splits into its units, a rejected candidate stays where it was stopped.
- Leave traces. When the second version plays, the first outcome stays quietly visible, so the final frame is itself the comparison.
- Focus attention within the current diagram. When switching diagrams, give enough context to connect the new view to the explanation; a persistent map is optional. Avoid separate progress strips, slide counters, status panels or repeated labels.
- Give quantities that look alike (several percentages, two dates) a distinct color or position and name each once.
- Make retained structure look identical in both versions and keep it in place; animate only what the change removes or adds. Scope "same in both" claims to the part where that is actually true.
- Hold a settled, readable frame after each consequential change. Recompose narrow layouts rather than shrinking text into illegibility.

## Keep words subordinate to the picture

Captions are phrase-level subtitles of the narration, one or two lines, not paragraphs. Center their box and each wrapped line on the film’s horizontal midpoint in the reserved subtitle area, including exported video; keep the diagram clear. Narration should explain the visible relationship or operation, including why a component exists or what a design choice changes. A held architecture diagram can support that reasoning without arithmetic or continuous motion.

Keep source links, commit hashes, provider metadata, production notes and detailed scope caveats in optional Details or accompanying source materials. The user's preferred watching surface has no audit footers or source end cards. Keep an assumption local only when it changes how the pictured mechanism should be understood; use a concise teaching label such as ‘2D example’ rather than repeated disclaimer prose. A film can follow one consequential mechanism if it says so; optional details or another chapter can map the rest of the change.

## Narration and one source of time

Keep a cue table with script, start, measured voice duration and scene timing, and derive animation times from it. Prefer pre-generated local audio over browser speech synthesis; label synthetic narration honestly and do not claim to have judged a voice you could not hear. Captions must make the film usable without sound.

For a reveal tied to a spoken phrase, use a named landmark from the narration manifest rather than a sentence's list position. Resolve and validate all referenced landmarks before rendering; missing names, ambiguous phrases and out-of-range times are errors, never a fallback to scene start. Add the cue's timeline start to its local landmark time. These are estimated speech times, so inspect the decisive reveal after export. The Qwen helper supports optional phrase bookmarks without changing the spoken text or requiring a new scene framework; see [narration.md](narration.md).

Use one master clock. In the HTML player, audio time can drive a pure `render(t)`; play/pause, seek and speed then stay synchronized, and seeking backwards works. For export, render each frame at its exact timestamp and mux the same narration; suspend audio-driven rendering while the export clock owns the scene, because queued media events can overwrite frames. A real-time screen recording is not a deterministic export.

Script edits invalidate audio, timing and export: cache audio by text, regenerate, and recheck. Keep changed-input experiments outside the narrated sequence unless the narration also adapts.

Use [narration.md](narration.md) for the current local Qwen paragraph workflow, the optional Kokoro helper, cached timing and the optional ElevenLabs workflow. Keep voice generation on the authoring machine and embed audio so playback works offline. Narration is complete only when real speech is present in the delivered file and the voice control is enabled. Check both the embedded HTML track and the MP4 audio stream; creating WAVs alone does not finish integration.

For a new film or production-pipeline revision, read [production-craft.md](production-craft.md). It adapts Brag’s source-first demonstrations, actionable scene briefs, settled reading time, cheap draft iteration, optional sound design and validation-coverage checks to this learning workflow while preserving the approved style.

## Critique the actual frames

Render and look at the beginning, the intermediate states of each transformation, the decisive moment, and the end, on desktop and narrow layouts. Then ask:

- With captions hidden, can a viewer locate the relevant components, trace their relationship, and see the behavior being explained? If numerical values are shown, do they clarify a necessary connection?
- Before the internal mechanism starts, do narration and pictures establish what the linked subject actually is, why it is needed, and what changes for someone using it? Does a later section rely on an unexplained prerequisite?
- Does the scene explain a component's purpose, interaction, or consequential design choice? Compress or omit detail that does not help the current question; completeness is not the goal.
- Can the viewer locate the evidence for the claim in the picture? For a held diagram, can they trace the reasoning through it? For a transformation, can they follow the same object through the operation? Stillness alone is not a defect, and decorative movement does not repair a missing connection.
- Does each element clarify a relevant role, relationship, operation, or context? Remove elements that contribute none of these.
- Is the meaning of the output established before the result depends on it?
- Does the final frame preserve the architectural relationship or design consequence being taught? For a change, does it show the before/after difference and its cause?
- Do labels collide, overflow their boxes, or become illegible on a narrow screen?

Treat review findings as hypotheses to check against sources and actual frames. A second model's praise is not verification. Do not claim 3Blue1Brown-level production or learning effectiveness; the user's judgment of the design is separate from technical checks.

## Verify the requested deliverable

For the default video, verify dimensions, frame rate, duration and narration, fully decode the file, and compare representative decoded frames with the source renderer at matched timestamps. An internal HTML renderer does not require user-facing page, mobile-player, or experiment testing. When HTML is requested, also check decisive frames, arbitrary seeks, end/replay, speed, keyboard use, reduced motion, optional prediction pauses, and any input experiment from the saved offline page. Keep playback correctness, source fidelity, design judgment and evidence of learning separate in the report.
