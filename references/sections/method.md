# Method Principles And Templates

## Section Role

The Method section explains how the contribution works and why each design choice supports the
paper's claims. It should be reproducible, motivated, and connected to the Method Tree.

## Pre-Writing Questions

Before writing Method, answer:

1. What modules, benchmark components, systems, algorithms, or analysis units exist?
2. What is the workflow of each module?
3. Why is each module needed?
4. Why does each module work?
5. Which claim and experiment does each module support?

## Method Writing Workflow

1. Draw a Pipeline Figure Sketch.
2. Use the sketch to decide Method subsections.
3. For each subsection, plan motivation, module design, and technical advantage.
4. Write module design first to build the concrete backbone.
5. Add motivation and technical advantage.
6. Add implementation details needed for reproduction.

## Pipeline Figure Sketch

Before prose, sketch:

- input,
- major processing blocks,
- novel module or novel benchmark component,
- output,
- evidence or evaluation linkage.

The figure should help highlight novelty. If the full pipeline is not novel, highlight the novel
module or use focused subfigures.

## Module Triad

Every important subsection should contain the module triad:

1. Motivation: what problem or challenge requires this component?
2. Design: what is the concrete input-step-output process?
3. Technical advantage: why does this design help, and how can that advantage be verified?

## Overview Template

Use at the start of Method:

1. One or two sentences for task setting.
2. One or two sentences for core contribution.
3. Pipeline/framework figure pointer if useful.
4. A map of what each subsection covers.

## Module Design Template

Use to explain concrete design:

1. Define representation, data structure, network, prompt, benchmark artifact, or protocol object.
2. Given input, describe step 1, step 2, step 3 in execution order.
3. State the output and how it is used downstream.

## Module Motivation Template

Use problem-driven motivation:

1. State a remaining problem or challenge.
2. Explain why previous/current practice has difficulty.
3. State why this module is needed.

## Technical Advantage Template

After design, explain:

1. what advantage the module creates,
2. why the advantage follows from the design,
3. which metric, ablation, analysis, or qualitative evidence will verify it.

## Implementation Details

Put practical details near the end or in a dedicated implementation/protocol subsection:

- hyperparameters,
- model or system settings,
- feature dimensions,
- coordinate transforms or normalization,
- annotation protocol,
- task construction rules,
- evaluation scripts or environment constraints.

## Method Clarity Check

Check at three levels:

1. Logic: summarize Method in a few bullets and test whether the flow is smooth.
2. Paragraph: each paragraph has one message and a clear opening sentence.
3. Sentence: each sentence has an explicit motivation; term names remain consistent.

## Must Avoid

- Listing implementation details without motivation.
- Introducing modules that do not support any claim.
- Hiding reproducibility-critical details.
- Making the figure carry explanation that the prose should provide.

## Template Selection

Select the Method organization before writing:

1. Pipeline organization: input -> modules -> output.
2. Component organization: benchmark/data/protocol components or system components.
3. Module-on-prior-pipeline organization: prior pipeline overview -> new module -> integration.
4. Analysis/protocol organization: definitions -> taxonomy/protocol -> measurement pipeline.

Choose the organization internally based on the paper type and Writing Policy. Do not expose
template-selection notes unless the user asks for reasoning.

## Required Output

For Full Draft Workflow, write English LaTeX prose into the corresponding section file. Keep a
compact `Section Plan`, `Paragraph Plan`, and `Evidence And Risk Notes` internally unless the user
asks to see them. Each method paragraph must map to a Method Tree node and include motivation,
design, technical advantage, or implementation detail as its role. Run reverse outlining and
claim-evidence mapping internally before returning.

## Self-Check

- Can a reader reconstruct the workflow?
- Does each component map to the Method Tree?
- Does each module have motivation, design, and technical advantage?
- Are assumptions and limitations explicit enough for reviewer scrutiny?
