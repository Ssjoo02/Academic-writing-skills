# Reference Paper Learning

Use this when the user provides papers they want to learn from.

## Learn

- Problem definition: identify how the paper names the task, motivates its importance, narrows scope, and separates the core problem from adjacent problems.
- Narrative structure: trace the sequence from motivation to gap, idea, method, evidence, and implications; record the role each section plays instead of copying its wording.
- Gap construction: observe what prior work is treated as insufficient, what evidence supports that insufficiency, and how the paper avoids overstating novelty.
- Insight placement: note where the main conceptual insight first appears, how often it is reinforced, and which sections make the insight operational.
- Method reveal timing: observe when the method is named, when its components are introduced, and how much intuition appears before formal or implementation detail.
- Evidence ordering: identify whether evidence moves from main results to ablations, qualitative examples, robustness checks, error analysis, or human evaluation.
- Section rhythm: observe section length balance, transitions between conceptual and empirical material, and where the paper slows down for definitions or interpretation.
- Reviewer-facing restraint: note hedging, scope boundaries, limitation placement, and how the paper signals evidence strength without weakening supported contributions.

## Do Not Copy

- Phrases.
- Sentences.
- Paragraphs.
- Distinctive expression.
- Paper-specific framing that would misrepresent the user's work.

## Conversion

Convert the learned structure into a profile card:

| Element | Learned pattern | How to adapt safely |
|---|---|---|
| Problem definition | Required: task name, motivation type, scope boundary, adjacent problems excluded. | Recast around the user's actual task, data, and claims; do not borrow the source paper's stakes if they do not apply. |
| Narrative structure | Required: section-by-section story role from motivation through implications. | Adapt the role sequence, not the phrasing or paper-specific transitions. |
| Gap construction | Required: prior-work limitation, evidence for the gap, novelty boundary. | State only gaps supported by the user's sources and experiments; avoid importing the reference paper's critique. |
| Insight placement | Required: first appearance of core insight, reinforcement points, operational section. | Place the user's own insight at analogous moments only when it improves clarity. |
| Method reveal timing | Required: method naming point, component introduction order, intuition-before-detail pattern. | Preserve timing logic while replacing all method content with the user's actual design. |
| Evidence ordering | Required: main-result position, secondary evidence sequence, failure or robustness placement. | Match evidence order to the user's evidence strength; do not imply missing experiments exist. |
| Section rhythm | Required: section length balance, definition density, transition pattern. | Use rhythm as a planning constraint, not as a sentence or paragraph template. |
| Reviewer-facing restraint | Required: hedging style, limitation placement, claim boundaries, risk handling. | Apply restraint according to the user's evidence and venue expectations; keep unsupported claims downgraded. |
