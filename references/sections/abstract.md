# Abstract Principles And Templates

## Section Role

The Abstract gives reviewers the first complete version of the paper's technical problem,
contribution, evidence, and boundary. It must obey the claim-evidence contract: every important
claim must be technically correct and supported by available evidence.

## Pre-Writing Questions

Answer these before writing:

1. What technical problem does the paper solve, and why is there no well-established solution?
2. What is the technical contribution?
3. Why does the contribution work in essence?
4. What technical advantage or new insight should reviewers remember?
5. Which experimental evidence can be safely stated in the Abstract?

## Version 1: Challenge -> Contribution

Use when the paper has one clear contribution and the key task is to make the challenge legible.

Structure:

1. Task.
2. Technical challenge for previous methods.
3. One to two sentences introducing the technical contribution.
4. Benefits of the technical contribution.
5. Experiment summary.

Matching example: `references/sections/examples/abstract/challenge-contribution.md`.

Expert notes:

1. Discuss previous work around the technical challenge that we actually solve.
2. For the contribution sentence(s), mention the technical term/name only; do not explain every
   detailed step. The technical term must be easy to understand — readers should not feel a jump.
3. This ability is very important for writing a good abstract.

## Version 2: Challenge -> Insight -> Contribution

Use when the main contribution is best explained through an insight. This is often stronger than
Version 1 because it teaches the reviewer a new way to see the problem.

Structure:

1. Task.
2. Technical challenge for previous methods.
3. One sentence introducing the insight for solving the challenge.
4. One to two sentences introducing the technical contribution that implements the insight.
5. Benefits of technical novelty.
6. Experiment summary.

Matching example: `references/sections/examples/abstract/challenge-insight-contribution.md`.

Expert notes:

1. Discuss previous work around the technical challenge that we actually solve.
2. Introduce the insight in one clear sentence.
3. For the implementation sentence(s), mention the technical term/name only; do not explain every
   detailed step. The technical term must be easy to understand — do not create a reading jump.
4. This ability is very important for writing a good abstract.

## Version 3: Multiple Contributions

Use when the paper has several contributions that each need a compact contribution-plus-advantage
statement.

Structure:

1. Task.
2. If needed, one contrast sentence about prior methods.
3. Contribution 1 + technical advantage.
4. Contribution 2 + technical advantage.
5. Contribution 3 + technical advantage (optional).
6. Experiment summary.

Matching example: `references/sections/examples/abstract/multiple-contributions.md`.

Expert notes:

1. When there are multiple technical contributions, describe each together with its technical
   advantage. The ability to express "contribution + advantage" in one sentence is very important.

## Must Include

- Problem before method.
- Contribution in one readable sentence.
- Evidence with verified numbers or verified qualitative findings.
- Scoped implication, not broad hype.

## Must Avoid

- Unsupported claims such as broad robustness, safety, superiority, or generality.
- Citation-dependent claims that have not passed citation-integrity checks.
- Multiple competing stories in one short abstract.
- Detailed implementation steps that belong in Method.

## Template Selection

Before writing, select exactly one of Version 1, Version 2, or Version 3 internally. If the paper
has one central insight, prefer Version 2. If the paper has several independent contributions, use
Version 3. Do not expose template-selection notes unless the user asks for reasoning.

## Example Bank

After selecting a section template, open only the matching example file if a concrete writing
pattern is needed. Reuse sentence logic and structure, not exact wording, task names, claims,
metrics, or citation framing.

1. `references/sections/examples/abstract.md` (index)

## Required Output

For Full Draft Workflow, write the English abstract into the corresponding LaTeX section file.
Keep a compact `Section Plan`, sentence-level `Paragraph Plan`, and `Evidence And Risk Notes`
internally unless the user asks to see them. Do not create a Chinese parallel abstract during Full
Draft Workflow. Run reverse outlining and claim-evidence mapping internally before returning.

## Quality Checklist

1. Can a reader identify task, challenge, insight/contribution, and results in one pass?
2. Are all major claims supported by experiments?
3. Are technical names self-contained and readable?
4. Is there any sentence that mixes too many messages?
5. Does every claim map to the Writing Policy?
6. Would a skeptical reviewer know what is new, why it matters, and what evidence supports it?
