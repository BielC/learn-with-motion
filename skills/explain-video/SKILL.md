---
name: explain-video
description: Explain a PR, paper, article, framework, or technical concept through a narrated video. Establish the actual subject and necessary background before architecture and relevant mechanisms. Use for animated explainers and video requests; ordinary summaries and code reviews remain their own tasks.
---

# Explain Video

Create a source-grounded explanation the viewer can follow from the big picture into useful detail. Deliver a narrated MP4 by default. Respect an explicitly requested draft or other video format. For a requested interactive webpage, use explain-interactive when available; do not add a companion page to a video request.

## 1. Read the subject and establish context

Read the linked material before planning the explanation. For a named project, establish what it actually is, what it does, who uses it, and where it fits. Use clear professional language and explain unfamiliar terms through their role. A generic story about the broader concept or an acronym expansion does not supply that background.

For a PR, inspect the exact revision, full diff, relevant callers, unchanged dependencies and tests. Explain the existing system, the core idea of the change, and old versus new behavior for the same situation before grouping implementation details by responsibility. For a paper, connect the research question, method, evidence and limits. For a framework, identify its responsibilities and trace a representative operation when helpful.

Choose a useful scope when the topic is broad. Ask only for missing information that affects the explanation. Preserve the distinction between source claims, inference, verified execution and invented examples. Source pointers belong in authoring notes. Keep confidential sources and all generated lessons outside this skill's repository; access to a source does not authorize publishing it or sending it to a cloud voice service.

## 2. Build the explanation before producing it

Establish necessary background, then architecture, then the mechanisms needed to answer the central question. Explain why a design produces its observable consequence without claiming undocumented author intent. Omit incidental helpers, dimensions and arithmetic unless they clarify a consequential connection. Numerical examples are optional. Keep substantial beginner background in an identifiable chapter when skipping it would help an informed viewer.

Read [film-direction.md](references/film-direction.md) to plan and verify the visual argument. In existing authoring notes, record the central question and each section's claim, visible evidence and supporting source. Check that the opening identifies the actual subject, prerequisites precede their use, examples retain their meaning, and each section makes the next question understandable. Cut sections that mainly complete a file inventory or repeat a point. Check important diagrams for plausible wrong readings. This review is part of authoring, not an approval gate.

Use warm paper, dark ink, generous spacing and restrained accents unless another style was chosen. Separate diagrams are welcome. Keep names and example state consistent and explain a change of view. Use motion for an operation or relationship it clarifies. A useful diagram held for twenty to thirty seconds is acceptable. Keep music, decorative motion, source labels and production metadata out of the default watching experience. A complete film must work without answering questions; do not require quizzes or teach-backs.

## 3. Generate narration and measured timing

Read [narration.md](references/narration.md). Preserve the selected voice. The default local recipe is Qwen3-TTS BF16 through MLX-Audio, Ryan, with measured British documentary delivery. Check available models and hardware; if that setup is unavailable, explain the blocker and ask before changing voice or provider.

Generate coherent paragraphs, then align captions afterward. Reuse cached speech for visual and caption revisions. Derive scene timings from measured audio plus deliberate holds. Center phrase subtitles in the reserved caption area, and keep negation, conditions and qualifications attached to the claims they modify. Inspect caption meaning across breaks, not just line length. A silent preview is a draft.

## 4. Render and verify the requested video

Reuse a working renderer and approved visual treatment when suitable. Choose the smallest stack that serves the explanation. HTML/SVG with a pure time-driven renderer is useful for software flows; Manim can suit mathematical transformations. An internal HTML render document does not require a user-facing webpage or player.

Use [player-runtime.md](references/player-runtime.md) only when adopting the included JavaScript clock/export helper. Use [visual-patterns.md](references/visual-patterns.md) when a reshape, incremental append or deferred evaluation needs a concrete representation. Keep one master clock and reconstruct scene state at arbitrary timestamps.

Inspect decisive states and transition frames, then export the film with its narration. Verify audio presence and continuity, dimensions, frame rate and duration; fully decode the result and compare representative decoded frames with the renderer at matched timestamps. A successful render does not establish factual accuracy, good teaching or preferred voice delivery. Fix observed problems and rerun affected checks.

## 5. Deliver

Return the actual video using the host's media display and an absolute file link. Briefly state the scope and material verification limits. Keep source notes available separately. Report authoring usage, voice charges and local rendering separately when cost is requested. Assess teaching quality through the learner's feedback and optional explanation or application, without claiming that the method is optimal or mastery was established.
