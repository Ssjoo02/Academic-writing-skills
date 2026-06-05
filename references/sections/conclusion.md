# Conclusion Principles And Template

## Section Role

The Conclusion closes the argument. It should restate the contribution, evidence, and limitations
without expanding the claim beyond the paper.

## Template

1. Restate the problem and contribution in one sentence.
2. Summarize the strongest evidence.
3. State the scoped implication.
4. Acknowledge key limitations or future work when needed.

## Limitation Policy

A limitation should usually come from task goal or task setting, similar to future work. Do not
voluntarily frame the paper around a technical defect unless the defect is already central to the
honest evaluation.

Decision rule:

- If a weakness does not damage existing important metrics relative to current SOTA or the paper's
  promised evaluation target, it can often be written as task/setting scope or future work.
- If a weakness damages an important metric, breaks a key claim, or creates negative net value, it
  is a technical defect and must be addressed in Experiments, Reviewer Risk, or claim weakening.
- A limitation statement should be precise enough to avoid overclaiming but not so broad that it
  supplies an avoidable rejection argument.

## Principles

- Close the story opened by the Introduction.
- Keep claims within demonstrated evidence.
- Mention limitations with precision, not apology.
- do not inflate the paper into solving a broader field problem.

## Must Avoid

- New claims, new citations, or new experimental interpretations.
- Unsupported future impact language.
- Repeating the Abstract mechanically.
- Presenting a serious technical defect as harmless future work.

## Template Selection

Select one conclusion mode:

1. Standard close: contribution -> evidence -> scoped implication.
2. Limitation-aware close: contribution -> evidence -> task/setting limitation -> future work.
3. Benchmark/resource close: artifact -> coverage/evidence -> intended use -> boundary.

Choose the conclusion mode internally based on the Writing Policy and evidence boundary. Do not
expose template-selection notes unless the user asks for reasoning.

## Required Output

For Full Draft Workflow, write English LaTeX prose into the corresponding section file. Keep a
compact `Section Plan`, `Paragraph Plan`, and `Evidence And Risk Notes` internally unless the user
asks to see them. The limitation paragraph must state whether the limit comes from task goal or task
setting, and whether it affects existing important metrics. Run reverse outlining and claim-evidence
mapping internally before returning.

## Self-Check

- Does the conclusion reinforce the Writing Policy's final takeaway?
- Are all claims already supported earlier?
- Does the limitation come from task goal or task setting rather than hidden method failure?
- Would a reviewer see honest scope control?
