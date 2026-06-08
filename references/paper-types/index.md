# Paper Type Index

First decide the paper type, then load the corresponding profile before building the Paper
Framework. The user may select the paper type. If not selected, infer it from the main contribution,
evidence package, target venue, and requested output, then mark the inference in the Writing Policy.
Do not default to `generic-paper.md` before checking the specific profiles.

Paper type profiles are section and page-budget references only. They help the agent decide which
sections a paper probably needs and how much main-text space each section may require. They are not
fixed templates, and they must be adapted to the actual paper, venue, evidence, and user request.

## Type Selection Map

Use the most specific matching profile. If a paper has multiple contribution types, choose the one
that controls the main evidence burden and page budget, then borrow individual sections from another
profile only when needed.

| Paper Type | Profile | Story center |
|---|---|---|
| Algorithmic / methodological innovation paper | `method-paper.md` | A new algorithm, architecture, training paradigm, objective, or method is the main contribution. |
| Systems / implementation engineering paper | `systems-implementation-paper.md` | A working system, platform, runtime, module, or engineering implementation is the main contribution. |
| Benchmark / dataset paper | `benchmark-dataset-paper.md` | A dataset, benchmark, evaluation suite, or measurement framework is the main contribution. |
| IMRaD / empirical original research | `imrad-paper.md` | A research question, study design, data collection or experiment, results, and interpretation are the main contribution. |
| Survey paper | `survey-paper.md` | A taxonomy, literature synthesis, research map, or future agenda is the main contribution. |
| Generic research paper | `generic-paper.md` | Use when the type is unknown, mixed, or better handled by a flexible common research-paper structure. |

## Common Mappings

| If the manuscript looks like... | Prefer this profile | Adjustment note |
|---|---|---|
| Algorithm, model, architecture, objective, training or inference procedure | `method-paper.md` | Protect method explanation, main results, ablations, and failure analysis. |
| Platform, runtime, agent framework, deployed tool, infrastructure, or engineering module | `systems-implementation-paper.md` | Protect system design, implementation details, workload, scalability, and reliability evidence. |
| Dataset, benchmark, evaluation suite, protocol, leaderboard, annotation study, or measurement framework | `benchmark-dataset-paper.md` | Protect construction, quality control, task design, metrics, baselines, and empirical findings. |
| IMRaD, scientific report, controlled experiment, observational study, user study, or empirical original-data paper | `imrad-paper.md` | Protect methods, results, discussion, validity, and reproducibility details. |
| Survey, review, taxonomy, systematic literature review, scoping review, tutorial survey, or research roadmap | `survey-paper.md` | Protect scope, selection method, taxonomy, comparative synthesis, and future directions; assume longer than a normal short conference paper unless the venue says otherwise. |
| Position paper, theory note, hypothesis essay, mixed contribution, early draft with unclear evidence, or unusual venue format | `generic-paper.md` | Rename sections as needed and keep the page budget explicitly venue-aware. |
