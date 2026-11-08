---
name: explain-interactive
description: Explain a PR, paper, article, framework, or technical concept through a self-contained interactive HTML page with inspectable diagrams, states, and optional experiments. Use when the user requests interactive exploration or an HTML explanation. A narrated video request belongs to explain-video.
---

# Explain Interactive

Build an explanation the learner can explore at their own pace. Deliver one self-contained HTML file by default. If a narrated video was requested, use explain-video when available. Produce both formats only when requested.

## 1. Read the source and explain the actual subject

Read the linked material and establish what it is, what it does, who uses it, and where it fits. Introduce necessary background before architecture and mechanisms, using clear professional language. Explain unfamiliar terms through their role. Keep examples tied to the subject; generic analogies and slogans do not replace an introduction to the actual project.

For a PR, inspect the exact revision, full diff and relevant surrounding code. Explain the existing system, the core idea of the change, and old versus new behavior for the same situation. Group code by responsibility. For a paper, connect its question, method, evidence and limits. For a framework, explain boundaries and responsibilities before tracing a representative operation. Mark inference, toy data and unverified behavior accurately. Keep source/version links available within the page, apart from the primary visual.

Choose a useful scope rather than requiring a prerequisite questionnaire. Keep source snapshots and generated lessons outside the skill repository. Private source access does not authorize publication or sending material to another service.

## 2. Choose an interaction that explains something

Identify the central question and which relationship the learner should be able to inspect. A before/after comparison, step-through trace, selectable case or changed-input experiment can help. Use only controls that expose meaningful differences. Numerical examples are optional. A diagram with clear relationships can be static.

In existing authoring notes, connect each section's claim to visible evidence and its source. Establish prerequisites before use, preserve names and example state across views, and make clear why the next question follows. Separate diagrams are welcome; reuse visual conventions where appropriate. Cut sections that only repeat a point or inventory implementation files. Check important diagrams for misleading interpretations before building the page.

Use warm paper, dark ink, generous spacing, clear typography and restrained accents unless another style was selected. Match navigation to the explanation: a purposeful reading sequence can scroll; a timed film player should keep its stage and controls together. Do not force every explanation into either layout. Make substantial beginner background skippable while keeping relevant context near its use.

## 3. Build the offline page

Read [html-output.md](references/html-output.md) for the document, interaction and verification contract. Prefer semantic HTML, SVG, CSS and plain JavaScript; add a framework only when it solves a real need. Keep source data, state transitions and rendering separate. Preserve the same correct state after replay, reverse navigation, rapid clicks or reduced-motion changes.

Inline essential assets so the file works from `file://` without a development server or network. Provide readable labels, keyboard-operable controls and visible focus. Explain the current state beside its diagram so a paused or interrupted learner can resume without a separate progress dashboard. Use meaningful clause boundaries for any captions, keeping negation and qualifications with their claims.

For a timed experience, read [player-runtime.md](references/player-runtime.md) before adopting the included clock and optional viewport shell. Supply pause, seek, replay and speed, including 0.8× and 0.9×. Manual traces can use previous/next and replay. Narration is optional: when requested, use the selected voice and available narration tooling, embed the audio, and verify synchronization. Ask before substituting an unavailable voice or provider. A page must remain understandable without audio.

## 4. Support optional guided use

A complete page must be usable without answering questions. Offer predictions or worked reveals only when useful, and honor requests for no quizzes. Do not infer understanding from clicks or keyword matching.

When the user explicitly asks to work through the topic together, read [guided-learning.md](references/guided-learning.md). This conversational mode waits for the learner's reasoning at agreed boundaries. It does not block delivery of an otherwise requested complete page.

## 5. Verify and deliver

Open the saved file and exercise its meaningful cases, previous/next/replay, arbitrary seeks if present, keyboard use, narrow and short windows, and reduced motion. Check state correctness, clipping, runtime errors and offline loading. For changed-input experiments, derive results from the changed state rather than replaying a fixed answer. Test optional audio and detail dialogs when present.

Return the absolute file link and open it in Google Chrome unless the user selected another browser; respect workspace profile instructions. State what was checked and any remaining limitations. Keep browser correctness, source accuracy, visual judgment and evidence of learning separate. A working interaction is not proof that the learner understood it.
