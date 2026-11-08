# Reusable visual arguments

Use a pattern when it fits the source. These are mechanisms to adapt, not a required scene list or a substitute for reading the topic. A static diagram can explain a pivotal operation when its before-state, relationship and result are inspectable. Motion is useful when it makes that connection easier to follow.

## Change a representation without losing the object

Useful for reshapes, head splits, grouped records and coordinate changes.

Keep one selected object visibly identified while expanding its internal structure. For a tensor, distinguish the axes that count objects from the axis that counts components. If one of six positions is expanded, label that focus and retain the other positions quietly; eight heads must not look like eight newly created tokens.

For an illustrative 512-component vector split into eight heads of 64, draw eight contiguous segments before separating them. Preserve segment colors/labels and map component `d` to head `floor(d / 64)`, component `d % 64`. Interpolate the same segment's position between these layouts; do not swap a shape label for an unrelated grid. A learned projection is a preceding operation that changes values; a reshape preserves those projected values. Show that distinction rather than presenting both as identical copying.

Return the selected object's result to its place in the parent picture before moving on. The learner should be able to point to which object was transformed and which axis changed organization with captions hidden.

## Append one item while reusing a prefix

Useful for caches, logs, queues and incremental computations.

Keep the retained prefix in place. Follow the one new input through the operation that creates the appended representation, then move that representation into the first empty slot. A token ID and a derived K/V pair have different meanings; transform and relabel at that boundary rather than depositing an ID directly into a vector cache.

Show the active input and retained state together at the consuming operation. Mark the resulting boundary: emitted output may await another pass before entering retained state. Count stored items and visible outputs separately when the mechanism distinguishes them. The final picture should expose that difference without relying on a sentence that says it happened.

## Separate a logical dependency from completed work

Useful for lazy arrays, query plans, futures and queued execution.

Declare early whether the picture traces logical dependencies or actual evaluation. Use the same nodes throughout: an outlined pending operation can become filled when evaluation occurs, while its dependencies remain visible. Show the trigger that requests work at that boundary. Avoid presenting numerical results as already available and explaining much later that nothing has run. Invented evaluated values can illustrate the dependency, provided that convention is stated before the first such result.

## Review a transformation, not only its endpoint

Inspect a pivotal transformation just before, during and after its operation. Progressive appearance of labels alone does not show how identities and values relate across a reshape, multiplication, append or feedback loop. A held diagram may already show those relations clearly; leave time to inspect it. If a needed connection is absent, add that connection or stage its operation. Do not infer a problem from twenty or thirty seconds of stillness or animate a readable diagram merely to keep it moving.

Split captions at complete phrase or sentence boundaries. Keep negation and its claim together. A character-count wrap can leave an isolated final word such as “parallel.”; revise the grouping and hold a meaningful complete phrase at the settled frame. Check actual rendered captions after regrouping or timing changes.
