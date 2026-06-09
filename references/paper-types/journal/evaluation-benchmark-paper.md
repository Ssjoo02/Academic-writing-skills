# Journal Evaluation / Benchmark Paper Type

Use this profile for journal papers whose main contribution is an evaluation: a benchmark that
measures a capability that prior evaluations missed, applied to a suite of models with a defined
protocol and a failure analysis. Representative shape: TPAMI MLLM evaluation benchmarks (e.g.,
measuring low-level visual perception/description/assessment across many multimodal models). The
center of gravity is the evaluation design and what it reveals, not a single new model.

## Use Only As Section Planning Reference

This file is only a section and proportional-budget reference for building a Paper Framework. It is
not a fixed paper template and does not prescribe writing style, reviewer strategy, claims,
experiments, or citations.

Adapt sections and budgets to the actual paper, venue, evidence, and user request. Do not copy this
structure mechanically. Merge, rename, split, shrink, or remove sections when the confirmed venue,
contribution, evidence package, or page budget requires it.

## Length: Defer To The Venue Card

This is a journal paper. Take absolute length from the venue card (TPAMI: double-column type limits;
JMLR: concise and complete). Plan sections as proportions first. Move full per-model result tables
and protocol details to supplemental material. Also load `references/venues/journal-vs-conference.md`.

## Section And Proportional-Budget Reference

| Order | Candidate section | Share of main text | Section role |
|---|---:|---:|---|
| Front | Abstract | ~3-5% | State the evaluation gap, the benchmark's abilities/dimensions, the model suite, and the headline finding. |
| 1 | Introduction | ~12-18% | Define what capability existing evaluations do not cover, the questions the benchmark answers, and contributions. |
| 2 | Related Work | ~8-12% | Compare prior benchmarks/evaluations by what they measure and what they miss. |
| 3 | Benchmark Construction | ~25-33% | Define the evaluation dimensions/abilities, the datasets and items, the question/task design, and the scoring/evaluation protocol (including any judge-assisted scoring). |
| 4 | Model Suite and Evaluation | ~22-30% | Define the evaluated models and access conditions, the unified protocol, and overall results across the dimensions. |
| 5 | Failure / Fine-Grained Analysis | ~10-16% | Analyze where and why models fail per dimension; this is the payload, not the leaderboard. |
| 6 | Conclusion | ~3-5% | Restate the measurement enabled, the key findings, and intended use. |
| End | Limitations | venue-dependent | Coverage limits, protocol/judge limits, contamination risks, intended non-uses. |
| Back | Appendix / Supplement | outside main budget | Full per-model tables, prompts, protocol details, and extra analyses. |

## Flexible Adjustment Notes

- The contribution is the evaluation design and what it reveals; do not let it collapse into a
  ranking table. Always include failure/fine-grained analysis.
- Specify the protocol precisely (items, conditions, scoring, any model-as-judge step) so the
  benchmark is reproducible and contestable.
- Name access conditions for each evaluated model (open weights vs API, version, date).
- If the central artifact is the data resource rather than the evaluation of models, use
  `dataset-benchmark-paper.md` instead.
