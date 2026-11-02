# Designing an animation that preserves the connections

## Small storyboard before implementation

Choose the learning target, useful architecture or process diagrams, relevant design choices, and useful level of detail. Separate diagrams can serve different aspects; a single persistent map is optional. Add a persistent example, consequential transition, or prediction boundary when it helps the explanation. Review each section's relevance to the central question before generating narration, as described in the main skill. Keep this as an authoring note rather than a long preamble for the learner. An animation can answer “why are these components separate?” or “what does this design make possible?” as well as a question about a particular execution step.

Use one current visual and compact controls. Add complexity only when the concept needs it. Reveal details progressively without losing their place in the larger map. Keep essential meaning in labels and observable states, not motion alone.

Keep the current state and open connection recoverable when playback is stopped or the learner returns after an interruption. Integrate this into the existing map/state rather than adding a duplicate dashboard. Reuse the artifact across connected chunks when practical.

## Make causality inspectable

- Each transition corresponds to an operation, not a decorative arrival. Show the value/relationship that changed and keep unaffected entities stable.
- Keep entities and input values consistent across frames. A transformed value should keep a recognizable identity; do not silently replace the example midway.
- Show the condition or cause beside the transition. Motion may represent data flow, control flow or a hypothesis; label which it is.
- Align animation states with the relevant code line, equation term or source claim. A teaching simplification must not contradict the source. Explain omitted mechanics when they matter to the current inference.
- Keep explanation adjacent to the relevant state, as compact labels. For video, place detailed source notes in accompanying materials. In an explicitly requested HTML lesson, include the teaching prose and source links needed to study without the chat; disclose longer details progressively. For inline visuals, follow that surface's content constraints and put longer prose in the conversation.
- Use colors for stable meaning and pair them with labels or shape. Avoid animated backgrounds, confetti, decorative motion, gamified scores or a wall of controls.

## Learner control

Start paused on a useful initial state. For video-style explainers, let Play run coherent animated scenes with synchronized captions; provide pause, seeking, replay, and playback speed. Keep automatic stops for agreed guided-learning boundaries or learner-selected prediction pauses. A complete explainer should remain watchable without repeated clicks or forced questions. For manual traces, previous/next and replay can be sufficient. Never loop continuously.

At a prediction boundary, the answer and its revealing next-state are initially hidden. In a complete self-paced explainer, a clearly labeled reveal is sufficient; avoid grading free-text answers with brittle keywords. In guided chat, let the tutor interpret the user's reasoning before revealing the answer. Do not send a model request on every animation step. Use a follow-up action only when the user explicitly chooses to ask the tutor.

If a learner chooses to predict, give them a way to commit before seeing the result; a local choice or mental prediction is enough for self-study. Keep a worked-step reveal available without forced entry. A reveal alone is not evidence that they predicted correctly. Respect an explicit no-quiz preference.

When a worked answer is revealed, optional local UI state may remember that it was shown, so returning to another frame does not imply an unseen prediction. Treat widget-state delivery as best-effort and never infer independence from an absent flag or a click. Describe understanding as untested unless the learner's reasoning provides evidence. Do not collect a performance profile.

Provide ordinary keyboard-operable buttons, readable labels, and an accessible description of the mechanism. Honor reduced motion by showing the same final states without movement; a zero-duration transition must preserve all information. Fit narrow layouts without shrinking labels beyond legibility. Do not rely on hover.

## Verify what matters

Exercise the important states and branches, reverse/replay, prediction reveal and source alignment. Check a narrow viewport, theme contrast, keyboard use and reduced motion when relevant. Catch runtime errors and clipping. If you cannot run the visual, say it remains untested rather than claiming verification.

Evaluate learning separately: can the learner reconstruct a link and handle a changed input without the visible answer? Interaction tests do not establish learning effectiveness.

## Optional worked example

[assets/retry-trace.html](../assets/retry-trace.html) is a synthetic, serialized-worker trace demonstrating stable state, a lost reply, a prediction boundary and a before/after comparison. Adapt its interaction pattern when useful; do not treat its pseudocode as a production idempotency implementation. Concurrent workers, crashes and persistence require additional mechanisms that this toy deliberately does not model. The example is optional, not a default lesson or a substitute for the user's source.
