# Production craft adapted from Brag

Read when planning a new narrated explanation or improving its production pipeline. These are adaptations for learning, not instructions to run Brag or turn the lesson into a launch ad. Preserve the selected visual style and voice.

Source reviewed: [latent-spaces/brag at 669ab928](https://github.com/latent-spaces/brag/tree/669ab9286aa28b6c3ee30e75f181ee74319d012a), including full/slim workflows, inspection, planning, composition, delivery and audio references. A framework change is optional; these techniques work with the existing HTML/SVG renderer.

## Make the plan describe evidence and action

Brag's strongest principle is showing a product in use instead of its marketing. For a technical lesson, make the architecture, interaction, or consequential behavior inspectable. A concrete input is useful when it connects the parts; numerical worked examples are optional. Start with the design question or discrepancy that makes the explanation worth following. The opening can be quiet; it needs a reason to keep watching, not advertising urgency.

Keep a compact authoring brief in the lesson's existing notes. It should identify the learner's target capability, source, architecture or process diagrams, the details worth explaining and those being omitted, visual/voice choices to preserve, and the consequence the final frame should make clear. Include a persistent example when useful. Apply the main skill's storyboard relevance review before synthesizing narration: cut or merge sections that do not advance the central question. Separate diagrams are valid; no single picture must persist throughout. Avoid duplicating this into several mandatory planning documents.

For each consequential beat, record only what the implementation needs:

| Beat | What must be visible | Action and result | Narration relationship | Evidence and timing |
| --- | --- | --- | --- | --- |
| Exclude padding | Same rows, mask and denominator | A zero mask prevents one row entering the sum or count | Point to the excluded row, then explain why the denominator is three | Source pointer in authoring notes; measured voice landmark, settled hold |

Be specific about sequence: which item enters, what it meets, what changes, and what remains visible afterward. “Animate attention” leaves the explanatory work undecided. For a UI change, show the relevant action and resulting state; for a paper, show the operation or comparison that supports the claim. A simulated interaction must be identifiable as a teaching reconstruction, not evidence of a live run.

The brief specifies meaning and constraints; the renderer chooses suitable mechanics. Reuse the approved player, scene patterns, source components or vector assets when useful. Match the source's behavior while keeping the learner's approved visual style. Animate editable elements rather than relying on pans over flat screenshots when the elements' relationships matter.

## Budget attention from settled visibility

Brag estimates about 0.3 seconds per word and 0.8 seconds for a short label. Treat these as initial readability checks, not learning targets or ceilings. A mathematical operation, unfamiliar symbol, comparison or causal trace can need substantially longer. Count reading time only after the complete text is visible and before it exits; entrance animation does not count as a hold.

When several items arrive, retain the set long enough to inspect their relationship. If narration, labels and movement compete, reduce or sequence the demands. Do not shorten the explanation to an ad's 15–25 second total or add motion to fill an acceptable 20–30 second hold.

Use clean transitions between dense layouts: preserve shared entities, remove outgoing material before introducing unrelated material, or pass through the paper background. A long crossfade can superimpose two individually readable diagrams into an unreadable one. Review the middle of the transition, not just its endpoints.

Center subtitle lines on the film's horizontal midpoint in the reserved caption area. A generic paragraph `max-width` can shift the box even with `text-align:center`; override it for captions in interactive and export modes. With CSS grid, use `place-content:end center` (or equivalent separate axes); `place-content:end` also right-aligns the content and can undo horizontal centering. Keep wrapping centered, safe margins clear of controls, and the diagram unobscured. Verify actual text-line geometry at narrow sizes and in an exported frame.

## Spend production effort where it changes the explanation

Iterate on the causal storyboard and representative stills before a full render. For a new treatment, render a short slice that includes one real transformation, its narration and its settled result. Prefer changing the existing lesson over rebuilding its shell.

Reuse speech on visual edits. Cache speech by text and synthesis settings, and treat caption/alignment revisions separately from speech regeneration where the tooling permits. Generate coherent paragraphs, then align the known script afterward; convenient timestamps should not dictate disconnected sentence delivery. These paragraph/alignment refinements come from this lesson's production experience, rather than from Brag's Kokoro implementation.

Keep essential assets local or embedded for the chosen delivery format. Wait for fonts, images and media readiness before capture. Use deterministic, seekable scene state and the same measured narration track for HTML and video. Reuse identical held frames in the exporter when possible without altering their duration. Keep drafts, audio caches and final deliverables distinguishable; do not copy an entire source asset library to use two files.

Report local synthesis, rendering and AI authoring usage separately when asked about cost. A local voice eliminates TTS API charges; it does not establish free authoring or a measured improvement in learning.

## Optional sound without stealing attention

Speech alone is a complete audio treatment for these lessons. If music or SFX improve a particular explanation, choose a coherent, restrained palette. Tie sounds to visible actions and use sparse accents at consequential moments; repeated typing ticks or bright impacts can distract from technical narration. Choose exact cues after the motion exists.

Mix speech, music and effects as separate authoring stems, then deliver a synchronized track. Duck music under speech, avoid harsh peaks and clipping, and check the actual mix; numerical volume settings alone do not establish intelligibility. At slow playback speeds, speech and visual timing must remain together.

Brag provides precomputed beat/strong-cue metadata and an analysis script for custom music. Such metadata can help an optional musical edit, but conceptual timing and readable holds take priority. RMS/energy modulation is different from beat detection. Avoid pulsing subtitles or explanatory values. Do not add music, beat analysis or audio-reactive backgrounds by habit to the user's current style.

If reusing assets, read their specific source/license: Brag's music is CC BY 4.0; its Kenney effects and separately sourced keyboard pack are described as CC0. Preserve required attribution in accompanying details/materials. No bundled code or media is needed to apply this reference.

## Check coverage, meaning and final delivery

Inspect the opening, every scene's settled state, intermediate transformation states and the ending. Include desktop, narrow and short windows. Check actual text and contrast coverage: a validator that inspected zero visible text elements has not verified readability. Structural checks do not establish factual correctness; audit asserted shapes, numbers, capabilities and comparisons against the source separately. Inventing a framing question is different from inventing a result.

For the default video delivery, decode the video and compare representative frames with independent renders at the same timestamps. Confirm real narration, audio continuity and duration; an existing WAV is not proof that the MP4 contains it. Check HTML playback and offline dependencies only when a user-facing page is requested. Keep source hashes, detailed scope and production metadata in source materials or optional page Details, off the film.

A separately chosen settled poster can help delivery; do not replace frame zero and disturb an explanatory opening to influence thumbnails. Sharing copy, public publishing and launch-video CTAs are outside this learning workflow unless requested.

## Upstream map

- [Inspection](https://github.com/latent-spaces/brag/blob/669ab9286aa28b6c3ee30e75f181ee74319d012a/skills/brag/references/step-1-inspect.md): working flow, real material, identity extraction.
- [Planning](https://github.com/latent-spaces/brag/blob/669ab9286aa28b6c3ee30e75f181ee74319d012a/skills/brag/references/step-2-plan.md): specific moments, explicit sequential actions, settled reading time.
- [Composition](https://github.com/latent-spaces/brag/blob/669ab9286aa28b6c3ee30e75f181ee74319d012a/skills/brag/references/step-3-compose.md): brief/implementation boundary, voice integration, factual-claim audit.
- [Delivery](https://github.com/latent-spaces/brag/blob/669ab9286aa28b6c3ee30e75f181ee74319d012a/skills/brag/references/step-4-deliver.md): draft/final iterations, actual validation coverage, settled poster.
- [Audio](https://github.com/latent-spaces/brag/blob/669ab9286aa28b6c3ee30e75f181ee74319d012a/skills/brag/references/audio.md): gesture-matched effects, cue analysis, asset licenses and local packaging.
- [Slim workflow](https://github.com/latent-spaces/brag/blob/669ab9286aa28b6c3ee30e75f181ee74319d012a/skills/brag-slim/SKILL.md): reuse source elements, pure time-driven frames, transition review with existing tools. It has no narration workflow; its model-specific dispatch is not a learning requirement.
