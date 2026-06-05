# Abstract Principles And Templates

## Section Role

The Abstract gives reviewers the first complete version of the paper's technical problem,
contribution, evidence, and boundary. It must obey the claim-evidence contract: every important
claim must be technically correct and supported by available evidence.

## Pre-Writing Questions

Answer these before writing:

1. What technical problem does the paper solve?
2. why there is no well-established solution for this problem?
3. What is the technical contribution?
4. Why does the contribution work in essence?
5. What technical advantage or new insight should reviewers remember?
6. Which experimental evidence can be safely stated in the Abstract?

## Version 1: technical challenge -> technical contribution

Use when the paper has one clear contribution and the key task is to make the challenge legible.

Template:

1. Task or setting.
2. Technical challenge for previous methods or current practice.
3. One or two sentences introducing the technical contribution.
4. Benefit or technical advantage.
5. Experiment summary with verified evidence.

## Version 2: technical challenge -> insight -> technical contribution

Use when the main contribution is best explained through an insight. This is often stronger than
listing modules because it teaches the reviewer a new way to see the problem.

Template:

1. Task or setting.
2. Technical challenge and why prior/current methods struggle.
3. One-sentence insight that resolves the challenge.
4. One or two sentences describing the mechanism that implements the insight.
5. Technical advantage and evidence.

## Version 3: multiple technical contributions

Use when the paper has several contributions that each need a compact contribution-plus-advantage
statement.

Template:

1. Task or setting.
2. Shared technical challenge.
3. Contribution 1 + advantage.
4. Contribution 2 + advantage.
5. Optional contribution 3 + advantage.
6. Evidence summary.

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

Before writing, select exactly one of Version 1, Version 2, or Version 3 internally. If the policy
has one central insight, prefer Version 2. If the policy has several independent contributions, use
Version 3. Do not expose template-selection notes unless the user asks for reasoning.

## Required Output

For Full Draft Workflow, write the English abstract into the corresponding LaTeX section file.
Keep a compact `Section Plan`, sentence-level `Paragraph Plan`, and `Evidence And Risk Notes`
internally unless the user asks to see them. Do not create a Chinese parallel abstract during Full
Draft Workflow. Run reverse outlining and claim-evidence mapping internally before returning.

## Self-Check

- Does every sentence map to the Writing Policy?
- Is the central challenge clear before the contribution appears?
- Are all metrics and comparisons supported by raw or confirmed derived evidence?
- Would a skeptical reviewer know what is new, why it matters, and what evidence supports it?
