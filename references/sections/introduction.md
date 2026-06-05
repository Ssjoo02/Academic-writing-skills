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
8. Experiments and contribution bullets.

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
5. Summarize evidence.

## Task/Application Version 1

Use when the task is niche.

Template:

1. Define the task as output from input.
2. Explain objective or scope.
3. List two or three applications.

## Task/Application Version 2

Use when the task is familiar to the venue.

Template:

1. Start directly from applications or importance.
2. Add target requirement such as accuracy, efficiency, robustness, safety, or reliability.

## Task/Application Version 3

Use when the general task is known but this paper's setting is new.

Template:

1. Start from general task value.
2. Narrow to the paper's specific setting.
3. Define exact input/output and boundary.

## Task/Application Version 4

Use when the task is familiar and the first paragraph can immediately expose the target challenge.

Template:

1. State application importance.
2. Briefly state how representative previous methods/current systems work.
3. State their failure case.
4. Explain the technical reason.

## Technical-Challenge Version 1

Use for an existing task with existing methods.

Template:

1. General challenge for the task.
2. Traditional methods and their limitation.
3. Recent method family 1 and its limitation with technical reason.
4. Recent method family 2 and its limitation with technical reason.
5. Ensure the final limitation is the exact challenge this paper solves.

## Technical-Challenge Version 2

Use when the paper's insight has historical or traditional-method backing.

Template:

1. State mainstream method limitation.
2. Introduce the older idea or traditional insight that points toward the solution.
3. Explain why that older line remains insufficient.
4. Return to recent methods and the unresolved technical challenge.
5. Bridge to the paper's contribution.

## Technical-Challenge Version 3

Use for a novel task with no direct prior method.

Template:

1. State the goal.
2. Say the problem is challenging for several reasons.
3. Use separate challenge points such as first, second, and finally.
4. For each point, state observable difficulty and technical reason.

## Pipeline Version 1

Use when there is one contribution with multiple advantages and a teaser figure.

Template:

1. Introduce the framework/representation/system for the task.
2. Point to the teaser or basic-idea figure.
3. State the key novelty in one readable sentence.
4. Briefly explain how it works.
5. State advantage 1.
6. State advantage 2.

## Pipeline Version 2

Use when there are two contributions.

Template:

1. Introduce the framework or pipeline.
2. State contribution 1 and its core novelty.
3. Explain the basic idea with a figure if useful.
4. Describe contribution 1 concretely enough to be understood.
5. State the technical challenge that remains.
6. Introduce contribution 2 as the answer to that challenge.

## Pipeline Version 3

Use when the contribution is a new module added to a prior pipeline.

Template:

1. Name the prior-style pipeline.
2. State the new module.
3. Explain why the existing pipeline lacks the capability.
4. Describe how the module operates.
5. Explain why the module improves the relevant metric or behavior.

## Pipeline Version 4

Use when the contribution comes from a key observation.

Template:

1. State the innovation.
2. State the observation that motivates it.
3. Explain why the observation is easy to understand and technically meaningful.
4. Describe the implementation of the observation.
5. Tie the advantage to evidence.

## Do Not Use: naive solution -> patch improvement

Do not first present a naive solution and then describe the paper as a small patch on top of it.
This can make the idea look obvious because the writing itself leads the reviewer step by step.
Frame the paper through the real technical challenge and the insight needed to solve it.

## Contribution Bullets

Each bullet should be a claim, not a component inventory:

- contribution,
- why it matters,
- evidence or section pointer,
- boundary if the claim is easy to overstate.

## Template Selection

Before writing, select one Task/Application version, one Technical-Challenge version, and one
Pipeline version internally. If the paper is a benchmark or new setting, consider Task/Application
Version 3 and Technical-Challenge Version 3 before using existing-task templates. Do not expose
template-selection notes unless the user asks for reasoning.

## Required Output

For Full Draft Workflow, write English LaTeX prose into the corresponding section file. Keep a
compact `Section Plan`, `Paragraph Plan`, and `Evidence And Risk Notes` internally unless the user
asks to see them. The paragraph plan must label each paragraph as task/application, challenge,
prior-work bridge, pipeline, evidence, contribution, or limitation. Run reverse outlining and
claim-evidence mapping internally before returning.

## Self-Check

- Is the first-page story visible without hidden context?
- Does every prior-work mention help lead to the technical challenge?
- Are contribution bullets evidence-backed and non-overlapping?
- Does the Introduction avoid naive solution -> patch improvement framing?
