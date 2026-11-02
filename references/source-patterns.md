# Source-specific teaching patterns

Read the relevant section, not the whole catalog by default.

## Pull requests and code

Start from the behavior the change affects. Inspect the exact PR revision, diff, callers and relevant tests before choosing a trace. Follow the repository's review, local-change and tool instructions when interacting with a repository.

For a standalone implementation or model, begin with the architecture: each major component's responsibility, what passes between components, what state is retained, and which design choices affect behavior or tradeoffs. Use the code to ground that explanation, not as a list of functions to cover. A tensor-heavy source does not require a tensor-arithmetic lesson. Explain an equation or numerical trace only when it resolves a connection needed for the current question; otherwise keep that detail optional or omit it.

For an explainer of a PR, explain the change as a whole before zooming into a helper: the old behavior and data flow, what the PR replaces or removes, the new behavior, and the practical consequence for the same input. A short trace of only the new code is a mechanism illustration, not a complete explanation of the PR. Distinguish changed behavior from retained dependencies and safeguards. Let chapters provide depth without making the learner hold every detail at once; do not use brevity to omit the before/after comparison they asked to understand. A film can trace one consequential difference in depth when it states that scope and briefly maps the other significant changes; accompanying source notes can hold further detail without requiring a webpage.

When a trace helps, use the same scenario through the before and after versions. Show the trigger → branch/operation → intermediate state → externally visible result at the relevant level of abstraction. Keep identifiers consistent with the source and include file/line or diff anchors outside the visual when the rendering surface requires prose there.

Connect the changed line to the requirement or failure it addresses: what would happen to the same input if that line were removed? Use the diff or issue for documented motivation. Code alone can show a consequence, but does not prove why the author chose the implementation.

Separate intended behavior, directly inspected code behavior and behavior verified by execution. A synthetic trace is not a passing test. Where appropriate, expose the boundary that makes the change necessary: empty input, final date, duplicate event, concurrent access or failure. Inspect the actual contract rather than inventing a boundary for visual interest.

Depth means being able to explain why the changed line changes the result, predict a different input, and identify an assumption the change depends on. It does not require narrating every unrelated line. Keep any animation an explanation of the PR, not a substitute for an authorized review or an implicit request to edit/push code.

## Papers and research articles

Keep the question → proposed mechanism/method → evidence → scope-of-claim visible. Explain the method's organization and design choices before choosing which mathematical details matter. Use a small numerical example if an essential equation remains unclear; a mathematical paper does not automatically need worked arithmetic. Reveal assumptions that change the meaning of the method or its evidence, even when omitting the derivation.

Distinguish an author's hypothesis, empirical result, explanatory interpretation and established background. Do not turn a correlation into an animated causal arrow. If the paper does not observe a mechanism, depict it as a proposed mechanism, or animate the study/data flow instead. Preserve uncertainty, baseline comparisons and what the reported experiment does not establish. Label toy values and conceptual diagrams as such.

For invented examples, say which pattern was constructed and what it cannot establish about the real study. A counterexample can show that an observation admits another explanation; it does not establish that explanation or the opposite of the original claim. Compute displayed numbers from the actual toy values. Keep hypotheses conditional: adjustment alone does not prove causality, and randomization balances confounders in expectation rather than guaranteeing identical groups in a finite sample.

A useful check asks the learner to predict what a changed assumption would alter, or which finding supports a particular claim. For an empirical claim, connect the explanation back to the actual figure/table/method passage, not only an analogy.

For a method detail, explain which uncertainty or threat to the claim it addresses. Distinguish a study-design counterfactual (what this design could establish) from a causal intervention the data never tested.

## Frameworks and libraries

Explain the framework's major responsibilities, boundaries, and consequential design choices. Choose a representative operation when it helps connect those parts: a request, state update, dependency resolution, model call, or build step. Trace its lifecycle through the actual components and show where the framework takes over from user code, without covering every helper or branch. Use current official documentation or source for version-sensitive behavior.

Keep the runtime trace distinct from static module organization. Introduce abstractions only when they explain the operation in the example. Tie a tiny runnable example to the state transitions when execution is useful and authorized. Avoid setting up a whole application merely to teach one mechanism.

Use a Python or Java comparison only if a known construct makes this particular concept easier to connect; do not duplicate every example in both languages. Show where semantics differ.

Connect an abstraction to the work it performs: what would the user have to implement manually without it? Compare languages or designs around the same constraint, and state where the analogy stops matching.

## General articles and concepts

Identify whether the explanation is a causal mechanism, an argument, a classification, or a comparison. Match the representation: causal motion, claim/evidence map, static hierarchy, or controlled comparison. Avoid forcing motion onto a taxonomy. Connect details back to the central question and retain exceptions instead of flattening them into a catchy analogy.
