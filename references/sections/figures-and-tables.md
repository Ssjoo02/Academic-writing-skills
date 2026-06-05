# Figures And Tables Principles

## Section Role

Figures and tables shape the paper's first impression and argument. They are part of the research
story, not decoration.

## Teaser Figure

Use a teaser figure when the paper benefits from an immediate visual summary of task, failure case,
method idea, benchmark setting, or surprising result.

The teaser figure should:

- make the paper look concrete and memorable,
- show the central problem or contribution,
- avoid overcrowded text,
- align with the Introduction's story.

## Pipeline Figure

A pipeline figure should highlight novelty. It is not only for explaining the workflow; the prose
should still make the method understandable.

Rules:

- If the whole pipeline is novel, show the full input-to-output structure.
- If only one module is novel, highlight novel module clearly.
- If a full pipeline figure makes the work look unoriginal, use focused subfigures.
- Connect the figure to the Method Tree and section plan.

## Result Figures

Use result figures to show qualitative differences, failure modes, stress tests, or application
potential that tables cannot communicate.

Each figure should have:

- one message,
- clear labels,
- matched comparison conditions,
- caption with setting and notation.

## Table Design

Rules:

- Put caption above the table.
- Prefer booktabs style: `toprule`, `midrule`, `bottomrule`.
- Avoid vertical rules and dense horizontal lines.
- Group columns with clear headings.
- Mark metric direction such as higher-is-better or lower-is-better.
- Use restrained highlighting for target numbers.

## Caption Rules

Captions should state experimental setting, notation, and the main reading instruction. Do not use
captions for long discussion that duplicates the main text.

## Self-Check

- Does each visual carry one message?
- Does the pipeline figure make novelty visible?
- Can the table be read without guessing metric direction or protocol?
- Is visual polish consistent with target venue expectations?
