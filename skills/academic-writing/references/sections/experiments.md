# Experiments Principles And Templates

## Section Role

Experiments provide evidence for the paper's claims. They should answer research questions, not
only report numbers.

## Three Questions

Before writing Experiments, answer:

1. Is the method better than strong baselines? — comparison experiments against strong and recent
   baselines, standard metrics on main benchmarks, fair protocol.
2. Which modules/design choices make the gain? — ablation studies for each key module/design
   choice, remove/replace/disable variants, report delta to full model.
3. How far can the method generalize? — harder settings, stress tests, failure modes, realistic
   boundaries.

## Experiment Planning

Plan experiments from two directions:

1. **Claim-driven**: each contribution in the Writing Policy → one validation experiment.
2. **Module-driven**: each component in the Method Tree → one ablation study.

This ensures every claim has evidence and every module has a reason to exist.

## Evidence Package

For empirical method-style papers, check whether the section includes:

1. comparison experiments against strong and relevant baselines,
2. ablation studies for key modules or design choices,
3. applications or demos when practical value, robustness, or realism is claimed,
4. stress tests, failure analysis, or limitations when safety/generalization is claimed.

For benchmark or analysis papers, adapt the package to coverage, reliability, evaluation protocol,
taxonomy validity, and insight quality.

## Section Organization

Standard method evaluation: setup → main comparison → ablation → analysis → failure cases.
Benchmark evaluation: benchmark statistics → model evaluation → breakdown → controls → limits.
Analysis paper: research questions → findings → supporting experiments → caveats.
New-task setting: protocol → adapted baselines/variants → diagnostics → demos.

These flows are **content blocks and paragraph roles, not mandatory numbered subsections**. Prefer
flowing prose; turn a block into a `\subsection` only when it spans multiple paragraphs or owns a
distinct table/figure. Keep Experiments to roughly 0–4 subsections — do not emit one numbered
subsection per analysis step (no `4.1 … 4.6`); a single-paragraph step should stay a paragraph,
optionally with a `\paragraph{}` run-in or bold lead-in.

**Statistics are tables, not prose.** "Benchmark statistics" and per-category breakdowns (per-app,
per-vector, per-harm, per-split counts) belong in **one table or figure**, not enumerated in
sentences. In prose, lead with the point and cite only the figures that carry an argument — the
total, the dominant or surprising share, the headline coverage — then point to the table. Do not
transcribe a table into running text. See the Salience And Compression rules in
`references/sections/paragraph-flow.md`.

## Comparison Version 1 (direct baselines exist)

Use when direct baseline methods exist.

Template:

1. State dataset/task/protocol.
2. Explain baseline selection and fairness.
3. Report standard metrics.
4. Explain the primary comparison result.
5. State caveats such as run failures, missing baselines, or protocol differences.

## Comparison Version 2 (no direct baselines)

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

## Figure And Table Rules

Good tables and figures are part of experiment communication quality, not decoration.

### Hard Rules

1. Put caption above the table.
2. Avoid vertical lines (`|`) in tabular columns.
3. Do not use double rules or dense `\hline` stacks.
4. Use `booktabs` style (`\toprule`, `\midrule`, `\bottomrule`) for clean structure.
5. Use as few horizontal rules as possible; lines separate groups, not every row.
6. Highlight key numbers (best/second-best or target rows) with subtle color emphasis.

### Readability Rules

1. Label metric direction in column headers (e.g., `PSNR ↑`, `LPIPS ↓`).
2. Add units when needed so values are interpretable without guessing.
3. Align text columns left; keep numeric columns consistently aligned.
4. Keep numeric precision consistent (same decimal places within a metric column).
5. Group multi-dataset or multi-setting results using `\multicolumn` + `\cmidrule`, not vertical
   separators.
6. One table or figure should carry one message; do not mix unrelated results in a single table.
7. If rows represent different attributes/ablations, encode that explicitly in row names or
   attribute columns.
8. Keep caption focused on setting/protocol/notation, not long discussion.
9. If there is little detail to explain, use one concise sentence to summarize the main result.
10. For single-column figures/tables in two-column papers, prefer placing them in the right column
    when layout allows, so readers can enter the page from left-top text without breaking flow.

### Caption Rules

- State experimental setting and notation.
- Explain metric direction and units when needed.
- State the main takeaway, not just a visual description.
- Keep discussion concise; do not duplicate the main text.

## Template Selection

Select an experiment organization before writing:

1. Standard method evaluation: setup → main comparison → ablation → analysis → failure cases.
2. Benchmark evaluation: benchmark statistics → model evaluation → breakdown → controls → limits.
3. Analysis paper: research questions → findings → supporting experiments → caveats.
4. New-task setting: protocol → adapted baselines/variants → diagnostics → demos.

Choose the organization internally based on paper type, available evidence, and reviewer risk.
Do not expose template-selection notes unless the user asks for reasoning.

## Required Output

For Full Draft Workflow, write English LaTeX prose into the corresponding section file. Keep a
compact `Section Plan`, `Paragraph Plan`, and `Evidence And Risk Notes` internally unless the user
asks to see them. Each result claim must identify metric, denominator, source artifact, and whether
the evidence is raw evidence or derived evidence. Run reverse outlining and claim-evidence mapping
internally before returning.

## Rigor Checklist

1. Are baselines recent and relevant?
2. Are metrics sufficient and standard for this task?
3. Is ablation tied to every key design claim?
4. Are claims in Abstract/Introduction supported by reported numbers?
5. Are limitations of evaluation scope explicitly stated?
6. Do main results support the Abstract and Introduction?
7. Are missing baselines, controls, or metrics recorded as evaluation risks or limitations?
8. Are per-category statistics confined to a table/figure, with prose citing only the numbers that
   carry an argument, rather than enumerated in sentences?
