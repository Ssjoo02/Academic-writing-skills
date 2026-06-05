# ICML Venue Profile

## Source Status

- Official template/guideline source status: `official source found`; see `../../maintenance/source-provenance.md`.
- Profile guidance source status: `generic cross-venue guidance pending representative-paper analysis`.
- The guidance below is `starter guidance`, not advice extracted from ICML papers or reviews.

## Reviewer Expectations

- Make the learning contribution precise: method, objective, theory, evaluation, or system.
- Connect claims to learning behavior, sample efficiency, optimization, generalization, or robustness.
- Use experiments and analysis to separate the proposed idea from implementation details.
- Keep assumptions, limitations, and reproducibility constraints visible.

## Typical Story Rhythm

- Learning problem and why it matters.
- Gap in existing methods or theory.
- Core idea and formal or algorithmic statement.
- Method details needed to reproduce the result.
- Evidence through benchmarks, ablations, analysis, or proofs.
- Scope, limitations, and practical constraints.

## Evidence Pressure

- Main result should validate the learning claim, not just a surface metric.
- Ablations should test objective terms, architecture choices, data choices, or training procedure.
- Theory should state assumptions and explain practical relevance.
- Comparisons should be fair, recent, and matched to the stated setting.

## Claim Strength Preferences

- Use strong claims for directly demonstrated learning improvements or proven guarantees.
- Use moderate claims for gains shown in constrained settings.
- Avoid implying general ML progress from a narrow benchmark slice.

## Common Reviewer Risks

- Method novelty is hard to separate from engineering choices.
- Theoretical framing does not match experiments.
- Empirical gains lack ablations or robustness checks.
- Baselines or hyperparameter budgets are unfair.
- Reproducibility details are incomplete.

## Writing Policy Effects

- Fill `Venue constraints`.
- Adjust `Claim Strength Policy`.
- Adjust `Metric And Evidence Policy`.
- Add venue-specific risks to `Reviewer Risk Register`.
