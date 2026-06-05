# Paper Review Principles

## Section Role

Use this file for whole-paper self-review, review reports, or final revision after a draft exists.
The goal is adversarial writing: read as a skeptical reviewer, identify rejection risks, and revise
before submission. Do not load this file during Writing Policy generation unless the user explicitly
asks for a formal review.

## Acceptance Drivers

The paper should have:

1. sufficient contribution,
2. strong enough empirical effect or insight,
3. sufficient comparison experiments and ablation studies for its archetype,
4. clear writing and reproducible details,
5. reasonable method or benchmark design.

## Five Review Dimensions

### Contribution

Check whether the paper gives readers new knowledge:

- novel task,
- novel pipeline,
- novel module,
- novel design choice,
- new experimental finding,
- new insight.

Failure signals: common failure case, well-explored technique, predictable improvement, or
straightforward design.

### Writing clarity

Check whether readers can understand and reproduce the work:

- clear story,
- motivated modules,
- stable terminology,
- enough technical detail,
- one paragraph, one message.

### Experimental strength

Check whether the effect is meaningful:

- improvement is not marginal,
- absolute performance is credible,
- evidence supports main claims,
- failure modes are discussed.

### Evaluation completeness

Check whether evaluation covers what reviewers expect:

- important baselines,
- important metrics,
- ablation studies,
- controls,
- hard enough datasets or settings.

### Method design soundness

Check whether the design is reasonable:

- realistic setting,
- no hidden technical flaw,
- robust enough without per-case tuning,
- benefits outweigh added limitations,
- no negative net value.

## Claim Support Rule

Every major claim, especially in Abstract and Introduction, needs claim support from experiments,
verified source text, or confirmed evidence. Unsupported claims must be weakened, removed, or moved
to future work.

## Output Requirement

Use this output only when the user explicitly asks for a review report or when a blocking issue
must be shown. During the full workflow, run this review internally before returning the final
draft.

When showing full-paper review, produce:

| Dimension | Reviewer question | Current answer | Risk level | Required revision |
|---|---|---|---|---|

Use exactly these five dimensions:

1. Contribution,
2. Writing clarity,
3. Experimental strength,
4. Evaluation completeness,
5. Method design soundness.

Risk level vocabulary: `low`, `medium`, `high`, `blocking`.

When a risk comes from missing evidence, state whether the fix is prose revision, claim weakening,
citation verification, additional analysis, or a new experiment.
