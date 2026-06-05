# Experiments Principles And Templates

## Section Role

Experiments provide evidence for the paper's claims. They should answer research questions, not
only report numbers.

## Three Questions

Before writing Experiments, answer:

1. How do we prove the method/system/benchmark is stronger or more useful than prior practice?
2. How do we prove that each core module or design choice is effective?
3. How do we show the upper bound, potential, or practical value of the work?

## Evidence Package

For empirical method-style papers, check whether the section includes:

1. comparison experiments against strong and relevant baselines,
2. ablation studies for key modules or design choices,
3. applications or demos when practical value, robustness, or realism is claimed,
4. stress tests, failure analysis, or limitations when safety/generalization is claimed.

For benchmark or analysis papers, adapt the package to coverage, reliability, evaluation protocol,
taxonomy validity, and insight quality.

## Comparison Version 1

Use when direct baseline methods exist.

Template:

1. State dataset/task/protocol.
2. Explain baseline selection and fairness.
3. Report standard metrics.
4. Explain the primary comparison result.
5. State caveats such as run failures, missing baselines, or protocol differences.

## Comparison Version 2

Use when the task is new and direct baselines are unavailable.

Template:

1. Explain why direct baselines do not exist.
2. Construct meaningful variants, simple baselines, adapted methods, or diagnostic controls.
3. Report what each comparison is meant to test.
4. Avoid claiming broad superiority over a nonexistent baseline set.

## Ablation Package

A strong ablation package usually has two levels:

1. A main ablation table for core contributions and major components.
2. Smaller focused ablations for module-level design choices, sensitivity, input quality, or
   protocol variants.

Each ablation should state:

- which claim it tests,
- what is removed/replaced/changed,
- expected effect,
- observed effect,
- whether the claim remains supported.

## Applications Or Demos

Use applications or demos to show practical value, difficult settings, or the work's upper bound.
They are especially important when the paper claims real-world usefulness, generality, safety, or
impact beyond a standard benchmark.

## Caption Rules

Figure and table captions are part of experiment writing:

- State experimental setting and notation.
- Explain metric direction and units when needed.
- Keep discussion concise; do not duplicate the main text.
- If there is little detail to explain, summarize the main result in one sentence.

## Layout Rules

- One table or figure should carry one message.
- Use clean table formatting and avoid visual clutter.
- Put caption above the table.
- Prefer booktabs-style rules for LaTeX tables.
- Place single-column figures or tables in locations that do not interrupt first-pass reading flow.

## Template Selection

Select an experiment organization before writing:

1. Standard method evaluation: setup -> main comparison -> ablation -> analysis -> failure cases.
2. Benchmark evaluation: benchmark statistics -> model evaluation -> breakdown -> controls -> limits.
3. Analysis paper: research questions -> findings -> supporting experiments -> caveats.
4. New-task setting: protocol -> adapted baselines/variants -> diagnostics -> demos.

Choose the organization internally based on paper archetype, available evidence, and reviewer risk.
Do not expose template-selection notes unless the user asks for reasoning.

## Required Output

For Full Draft Workflow, write English LaTeX prose into the corresponding section file. Keep a
compact `Section Plan`, `Paragraph Plan`, and `Evidence And Risk Notes` internally unless the user
asks to see them. Each result claim must identify metric, denominator, source artifact, and whether
the evidence is raw evidence or derived evidence. Run reverse outlining and claim-evidence mapping
internally before returning.

## Self-Check

- Do main results support the Abstract and Introduction?
- Are ablations tied to the Method Tree?
- Are applications or demos aligned with downstream value?
- Are missing baselines, controls, or metrics recorded as evaluation risks or limitations?
