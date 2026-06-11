# Introduction Principles And Templates

## Section Role

The Introduction builds the paper's story. It should make reviewers understand the task, the
technical challenge, why prior/current practice is insufficient, what this paper contributes, why
the contribution works, and what evidence will support it.

## Introduction Logic Map

Plan the section around this chain:

1. Task and application or setting.
2. Target metric, target capability, or evaluation goal.
3. Prior/current methods or practice.
4. Failure case and limitation.
5. Technical reason behind the limitation.
6. Proposed contribution or pipeline.
7. Why the contribution works.
8. One brief experiment mention, then contribution bullets.

## Backward-Then-Forward Planning

Use backward-then-forward reasoning before drafting the section.

Backward:

1. What contribution should reviewers remember?
2. What benefit or new insight does it provide?
3. What technical challenge makes the contribution necessary?
4. Which prior-work/current-practice discussion makes the challenge natural?

Forward:

1. Introduce task or setting.
2. Lead to the technical challenge.
3. Present contributions that solve the challenge.
4. Explain technical advantage and new insight.
5. Summarize evidence in one brief mention.

## Section Skeleton

The Introduction contains exactly these five blocks, in order. Treat this skeleton as a hard
boundary on scope and length: do not add a separate results-recap paragraph, a roadmap paragraph,
or a difference-from-prior-work section to the Introduction by default.

```latex
\section{Introduction}
% Task and application
% Technical challenge for previous methods (limitation + technical reason)
% Our pipeline for solving the challenge
% Experiment (one brief mention)
% Contributions
```

The `% Experiment` block is **one brief sentence** that signals the evidence exists; the detailed
numbers belong in the Experiments section. Do not repeat the same statistic in both the experiment
mention and the contribution bullets — any given number appears at most once in the Introduction.

## Part A: Introduce Task and Application

### Version 1 (niche task)

Use when the task is niche. Define the task first, then introduce applications.

Template:

1. Define the task as output from input.
2. Explain objective or scope.
3. List two or three applications.

Sentence skeleton:

1. `[xxx task] targets at recovering/reconstructing/estimating [xxx output] from [xxx input].`
2. `[xxx task] has a variety of applications such as [xxx], [xxx], and [xxx].`

Matching example: `references/sections/examples/introduction/task-then-application.md`.

### Version 2 (familiar task)

Use when the task is familiar to the venue. Skip formal definition; open with applications.

Template:

1. Start directly from applications or importance.
2. Add target requirement such as accuracy, efficiency, robustness, safety, or reliability.

Sentence skeleton:

1. `[xxx task] has a variety of applications such as [xxx], [xxx], and [xxx].`

Matching example: `references/sections/examples/introduction/application-first.md`.

### Version 3 (general-to-specific)

Use when the general task is known but this paper's setting is new. Start broad, then narrow.

Template:

1. Start from general task value.
2. Narrow to the paper's specific setting.
3. Define exact input/output and boundary.

Sentence skeleton:

1. `[general task] has a variety of applications such as [xxx], [xxx], and [xxx].`
2. `This paper focuses on the specific setting of recovering/reconstructing/estimating [xxx output] from [xxx input].`

Matching example: `references/sections/examples/introduction/general-to-specific-setting.md`.

Expert note:

1. Version 3 is personally recommended when the setting is relatively new. It gives readers a familiar entry point before introducing the novel constraints.

### Version 4 (open with challenge)

Use when the task is familiar and the first paragraph can immediately expose the target challenge.

Template:

1. State application importance.
2. Briefly state how representative previous methods/current systems work.
3. State their failure case.
4. Explain the technical reason.

Sentence skeleton:

1. `[Task/application importance sentence].`
2. `Given input ..., previous methods usually ...`
3. `Although they work in many cases, they fail at ... because ...`

Matching example: `references/sections/examples/introduction/open-with-challenge.md`.

Expert note:

1. It is often good if the first paragraph already states what problem you want to solve, instead of requiring several paragraphs of prior work before the challenge appears.
2. This style needs the right conditions and is less common than Version 1–3.

## Part B: Introduce Technical Challenge (Very Important)

Purpose:

1. Discuss around the exact technical challenge we solved.
2. Build reader curiosity about how to solve this challenge.
3. Make motivation/benefit of our method clear.

Important warning:

1. Do not first present a naive solution and then describe the paper as a small patch on top of it.
   This writing style erases reader curiosity and makes the idea look obvious only because the
   writing hand-holds the reader step by step. Even if the work is actually incremental, do not
   write it this way.

### Technical-Challenge Version 1 (existing task, existing methods)

Use for an existing task with existing methods.

Template:

1. General challenge for the task.
2. Traditional methods and their limitation.
3. Recent method family 1 and its limitation with technical reason.
4. Recent method family 2 and its limitation with technical reason.
5. Ensure the final limitation is the exact challenge this paper solves.

Sentence skeleton:

1. `This problem is particularly challenging due to ...`
2. `To overcome these challenges, traditional methods ... However, they ...`
3. `Recently, ... methods ... However, they ... because ...`
4. `To overcome this challenge, ... methods ... However, they ... because ...`

Matching example: `references/sections/examples/introduction/technical-challenge-existing-task.md`.

### Technical-Challenge Version 2 (existing task + historical insight)

Use when the paper's insight has historical or traditional-method backing. Use the classical line
as conceptual backing, then show why new methods still fail.

Template:

1. State mainstream method limitation.
2. Introduce the older idea or traditional insight that points toward the solution.
3. Explain why that older line remains insufficient.
4. Return to recent methods and the unresolved technical challenge.
5. Bridge to the paper's contribution.

Sentence skeleton:

1. `Traditional/recent methods ... However, they ... because ...`
2. `To overcome this problem, a typical approach is [insight], which has long been explored ...`
3. `However, these methods still ... because ...`
4. `To overcome this challenge, newer methods ... However, they ... because ...`

Matching example: `references/sections/examples/introduction/technical-challenge-historical-insight.md`.

### Technical-Challenge Version 3 (novel task, no direct methods)

Use for a novel task with no direct prior method. Define the challenge directly and decompose it
into concrete points.

Template:

1. State the goal.
2. Say the problem is challenging for several reasons.
3. Use separate challenge points such as first, second, and finally.
4. For each point, state observable difficulty and technical reason.

Sentence skeleton:

1. `In this work, our goal is to ... This problem is challenging for three reasons.`
2. `First, ...`
3. `Second, ...`
4. `Finally, ...`

Matching example: `references/sections/examples/introduction/technical-challenge-novel-task.md`.

## Part C: Introduce Our Pipeline for Solving the Challenge

### Pipeline Version 1 (one contribution, multiple advantages)

Use when there is one contribution with multiple advantages and a teaser figure.

Template:

1. Introduce the framework/representation/system for the task.
2. Point to the teaser or basic-idea figure.
3. State the key novelty in one readable sentence.
4. Briefly explain how it works.
5. State advantage 1.
6. State advantage 2.

Sentence skeleton:

1. `In this paper, we propose a novel framework/representation, named ..., for ...`
2. `The basic idea is illustrated in Figure ...`
3. `Our innovation is in ...`
4. `Specifically, ...`
5. `In contrast to previous methods, ...`
6. `Another advantage of the proposed method is that ...`

Matching example: `references/sections/examples/introduction/pipeline-one-contribution.md`.

### Pipeline Version 2 (two contributions)

Use when there are two contributions.

Template:

1. Introduce the framework or pipeline.
2. State contribution 1 and its core novelty.
3. Explain the basic idea with a figure if useful.
4. Describe contribution 1 concretely enough to be understood.
5. State the technical challenge that remains.
6. Introduce contribution 2 as the answer to that challenge.

Sentence skeleton:

1. `In this paper, we propose ...`
2. `Our innovation is in ...`
3. `The basic idea is illustrated in Figure ...`
4. `Specifically, ...` (contribution 1)
5. `In contrast to previous methods, ...`
6. `However, ...` (remaining challenge)
7. `Specifically, ...` (contribution 2)

Matching example: `references/sections/examples/introduction/pipeline-two-contributions.md`.

### Pipeline Version 3 (new module on existing pipeline)

Use when the contribution is a new module added to a prior pipeline.

Template:

1. Name the prior-style pipeline.
2. State the new module.
3. Explain why the existing pipeline lacks the capability.
4. Describe how the module operates.
5. Explain why the module improves the relevant metric or behavior.

Sentence skeleton:

1. `Inspired by previous methods, ...`
2. `Our innovation is introducing ...`
3. `We observe that ...`
4. `Considering that ..., we introduce ...`
5. `In contrast to ..., our module ...`

Matching example: `references/sections/examples/introduction/pipeline-new-module.md`.

### Pipeline Version 4 (observation-driven)

Use when the contribution comes from a key observation. State innovation first, then the
motivating observation, then details.

Template:

1. State the innovation.
2. State the observation that motivates it.
3. Explain why the observation is easy to understand and technically meaningful.
4. Describe the implementation of the observation.
5. Tie the advantage to evidence.

Sentence skeleton:

1. `Our innovation is ...`
2. `We observe that ...`
3. `Considering that ..., we ...`
4. `This leads to ... and achieves ...`

Matching example: `references/sections/examples/introduction/pipeline-observation-driven.md`.

## Do Not Use: naive solution -> patch improvement

Do not first present a naive solution and then describe the paper as a small patch on top of it.
This can make the idea look obvious because the writing itself leads the reviewer step by step.

If the method is simple, also do not hide concrete method design in Introduction and only describe
abstract insights to make the work look novel. The better target is to clearly explain the core
contribution implementation.

Matching example: `references/sections/examples/introduction/avoid-abstract-only-insight.md`.

## Contribution Bullets

Keep contributions compact: one bullet per contribution, each a single claim sentence (at most one
extra sentence for an evidence or section pointer). Do not expand a bullet into a four-part
mini-paragraph and do not pack statistics, model lists, or boundary caveats into the bullets — that
turns the contribution list into a dense wall. A bullet is a claim, not a component inventory.

- One claim sentence per contribution.
- At most one short evidence or section pointer.
- No repeated numbers (any statistic already used in the experiment mention stays out of the bullets).

Positioning against the closest prior work belongs in Related Work, not in a dedicated Introduction
section. A roadmap paragraph is not part of the default Introduction; add one only when the venue or
paper structure explicitly requires it (see the journal overlay).

## Example Bank

After selecting a section template, open only the matching example file if a concrete writing
pattern is needed. Reuse sentence logic and structure, not exact wording, task names, claims,
metrics, or citation framing.

1. `references/sections/examples/introduction-examples.md` (index)
2. `references/sections/examples/abstract-examples.md` (abstract examples — useful for contribution framing)

## Template Selection

Before writing, select one Task/Application version, one Technical-Challenge version, and one
Pipeline version internally. If the paper is a benchmark or new setting, consider Task/Application
Version 3 and Technical-Challenge Version 3 before using existing-task templates. Do not expose
template-selection notes unless the user asks for reasoning.

## Required Output

For Full Draft Workflow, write English LaTeX prose into the corresponding section file, following
the five-block Section Skeleton above. Run reverse outlining and claim-evidence mapping internally
before returning; do not expose internal plans unless the user asks.

## Quality Checklist

1. Does the first sentence of each paragraph state its message?
2. Does each paragraph carry one message only?
3. Are technical challenge, technical reason, and solved mechanism all explicit?
4. Are claims in Introduction aligned with experiment evidence?
5. Is terminology stable across all sections?
