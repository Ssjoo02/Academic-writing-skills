# Related Work Principles And Template

## Section Role

Related Work should position the technical challenge and the paper's difference. It is not a
citation list.

## Template

For each related-work group:

1. Name the research line.
2. State what this line contributes to the problem space.
3. Explain the remaining limitation or mismatch.
4. Clarify how the current paper differs.
5. Avoid overstating the gap.

## Template Selection

Choose one organization:

1. Closest-baseline first: use when reviewers expect direct comparison to specific recent papers.
2. Technical-topic grouping: use when several method families explain the target challenge.
3. Task-then-technique grouping: use when the paper introduces a new setting but uses known
   techniques.

Choose the organization internally based on how the paper needs to position its technical
challenge. Do not expose template-selection notes unless the user asks for reasoning.

## Required Output

For Full Draft Workflow, write English LaTeX prose into the corresponding section file. Keep a
compact `Section Plan`, `Paragraph Plan`, and `Evidence And Risk Notes` internally unless the user
asks to see them. Every citation-dependent claim must be marked verified, not verified, partially
supports, or does not support internally, and unresolved cases must be surfaced in `Evidence And
Risk Notes`. Run reverse outlining and citation/claim-evidence mapping internally before returning.

## Principles

- Organize by contrastive roles, not by chronology.
- Use citations to support positioning, not to decorate paragraphs.
- Separate "not addressed" from "addressed differently".
- Position the technical challenge in relation to prior work.
- If a claim depends on source content, mark citation status until verified.

## Must Avoid

- "A did X; B did Y; C did Z" paragraphs with no argument.
- Dismissing prior work without evidence.
- Claiming novelty before checking citation support.

## Self-Check

- Does each paragraph explain a difference that matters for the story?
- Are citations verified or marked not verified?
- Does this section make the contribution look necessary rather than isolated?
