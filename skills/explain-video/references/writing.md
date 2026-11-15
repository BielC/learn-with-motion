# Write an explanation the learner can follow

Use this while drafting and reviewing prose, narration and labels. Improve the reasoning before polishing vocabulary. Follow the requested audience and tone; when writing on the user's behalf, use an available writing profile without inventing personal habits or importing private samples into the lesson.

## Give each passage a purpose

Identify the actual subject and the question the explanation will answer. Establish the prerequisites needed to follow the answer. In a direct answer or status update, put the conclusion first; in a lesson, give enough orientation for that conclusion to mean something.

Each passage should contribute a necessary definition, a supported claim, an example, or a connection in the reasoning. Cut introductions that announce an explanation without beginning it, promotional adjectives and paragraphs that repeat a heading. Keep background even when its facts are uncontroversial. A learner may need them.

Use concrete actors and actions: say which component stores a record, which condition triggers a retry and what changes afterward. Support measurements and comparisons with the source. If the source gives no measurement, describe the supported behavior and leave its magnitude unknown. Preserve calibrated uncertainty and distinguish an observation from a general guarantee.

## Connect familiar information to the next idea

Begin a sentence with an entity or state the learner already recognizes, then introduce the consequential new information. Let the next sentence build on that result. Keep the subject near its verb, and replace an ambiguous "this" or "it" with the relevant object.

Use the relationship as the transition: "because" for a cause, "if" for a condition and "after" for an order. State only relationships the source supports. A heading or "next, let's explore" does not explain why one section follows another. When changing views, carry forward a recognizable entity or question.

Keep the same term for the same object across prose, code and diagrams. Define a necessary technical term through its role. Avoid ornamental synonyms that make one object sound like several. Prefer direct verbs over noun phrases such as "perform the execution of".

Keep negation, exceptions and conditions beside the claims they qualify. Split a difficult sentence at a meaningful boundary while preserving scope, causality and units. Sentence length is a diagnostic, not a quota; controlled-English word substitutions can change technical meaning.

## Edit for the delivery format

For narration, write connected paragraphs that work when heard once. Read aloud or subvocalize before synthesis. Repair stacked clauses, awkward acronym sequences and references that require rereading. Vary sentence length as the reasoning needs, without forcing fragments or a cadence score. Align labels and spoken terms, and make references such as "this arrow" unambiguous in the visible scene.

For an interactive page, use concise labels that identify the entity, state or action. A control should say what changes, and nearby prose should explain the resulting state. Keep necessary qualifications visible where the learner uses them; optional detail can be disclosed separately. The page must make sense without audio.

End a section on its consequence or the question that consequence raises. A brief recap can help reconnect a long explanation, but repeating every claim adds reading or listening time without adding understanding.

## Review meaning after editing

Check the opening's subject, the chain of reasoning and the support for consequential claims. Then remove filler and repetition, repair awkward flow and compare edited claims with the source. Confirm that simpler wording still preserves actors, conditions, uncertainty and failure behavior.

Vocabulary or cadence audits can locate passages worth reviewing. A flag does not establish poor writing or AI authorship. Keep a precise term, useful list or necessary qualification even if a checker objects. Do not optimize for zero flags, numerical rhythm targets or an arguable opinion in every paragraph. Do not add slang, errors or disagreement to simulate personality.

For example, assume a synthetic retry mechanism stores completed results by request ID:

> The client can lose the reply after the server finishes a request. The client then retries with the same request ID. If the server still has the stored result for that ID, it returns the result without repeating the operation.

The stored-result condition limits the claim. Shortening the last sentence to "Retries never repeat the operation" would change its meaning. A useful diagram should show that condition too.

This guidance adapts ideas from [claude-writing-skills at revision 75fc0239](https://github.com/nonatofabio/claude-writing-skills/tree/75fc02399884645ea8ae3e3761fdb088bcd12c38) in original prose. Its editing advice is a craft heuristic, not evidence of learning effectiveness or an authorship detector.
