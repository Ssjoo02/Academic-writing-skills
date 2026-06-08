# Benchmark / Dataset Paper Type

Use this profile for papers whose main contribution is a benchmark, dataset, evaluation suite,
annotation protocol, data construction pipeline, or measurement framework.

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
| Front | Abstract | 0.15-0.25 page | Summarize the measurement/resource gap, constructed benchmark or dataset, main findings, and intended use. |
| 1 | Introduction | 1.0-1.5 pages | Define the target task or capability, limitations of existing benchmarks/resources, research questions, design considerations, proposal, and contributions. |
| 2 | Related Work | 0.75-1.25 pages | Compare prior datasets, benchmarks, protocols, and metrics by coverage, construct, annotation, and evaluation assumptions. |
| 3 | Benchmark / Dataset Construction | 1.75-2.75 pages | Explain data sources, preprocessing, synthesis or transformation pipeline, annotation/scoring rules, quality control, and validation. |
| 4 | Experiments and Empirical Findings | 2.0-3.0 pages | Define evaluation protocol, metrics, baselines, prompting/training access, overall performance, fine-grained analysis, and case studies. |
| 5 | Conclusion | 0.25-0.5 page | Summarize enabled measurement or resource value and key findings. |
| End | Limitations | venue-dependent | State dataset coverage limits, annotation limits, metric limits, intended non-uses, and ethical or access constraints. |
| Back | Appendix | outside main budget when allowed | Put full data documentation, annotation guide, extra results, prompt details, examples, and release metadata here. |

## Flexible Adjustment Notes

- If construction quality is the main contribution, allocate more space to pipeline, annotation, and validation.
- If empirical findings are the main contribution, allocate more space to research-question-driven analysis and case studies.
- If the venue requires dataset documentation, datasheets, or checklists, include them in the Page Budget Summary or appendix plan.
