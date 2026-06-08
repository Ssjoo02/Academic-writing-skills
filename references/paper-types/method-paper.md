# Algorithmic / Methodological Innovation Paper Type

Use this profile for papers whose main contribution is a new algorithm, model architecture,
training paradigm, objective, inference procedure, or methodological design.

## Use Only As Section Planning Reference

This file is only a section and page-budget reference for building a Paper Framework. It is not a
fixed paper template and does not prescribe writing style, reviewer strategy, claims, experiments,
or citations.

Adapt sections and page budgets to the actual paper, venue, evidence, and user request. Do not copy
this structure mechanically. Merge, rename, split, shrink, or remove sections when the confirmed
venue, contribution, evidence package, or page budget requires it.

## Section And Page-Budget Reference

Assume an 8-page main-text conference paper when no venue-specific budget is known.

| Order | Candidate section | Typical budget | Section role |
|---|---:|---:|---|
| Front | Abstract | 0.15-0.25 page | Summarize background, gap, method idea, main result, and scoped conclusion. |
| 1 | Introduction | 1.0-1.5 pages | Establish the problem, prior limitation, research question, core method insight, and contributions. |
| 2 | Related Work | 0.75-1.25 pages | Group related algorithms or methods by technical line and clarify the gap this method targets. |
| 3 | Method | 2.0-3.0 pages | Explain algorithm structure, architecture, training/inference flow, equations, pseudocode, and module rationale. |
| 4 | Experimental Setup | 0.5-0.75 page | State datasets, baselines, metrics, implementation settings, and hyperparameters needed for reproducibility. |
| 5 | Results and Analysis | 1.5-2.5 pages | Present main results, ablations, robustness checks, efficiency, qualitative analysis, and failure cases. |
| 6 | Conclusion | 0.25-0.5 page | Summarize the method contribution, strongest evidence, and future direction. |
| End | Limitations | venue-dependent | Discuss failure cases, compute/resource cost, assumptions, and settings where the method may not transfer. |
| Back | Appendix | outside main budget when allowed | Put long proofs, extra derivations, extra tables, implementation details, and extended qualitative examples here. |

## Flexible Adjustment Notes

- If the method is mathematically heavy, reserve more Method or Appendix space for derivations and reduce Related Work.
- If the core claim depends on empirical gains, protect enough Results and Analysis space for ablation and failure analysis.
- If the venue has a required limitations or ethics section, account for it in the venue-aware Page Budget Summary.
