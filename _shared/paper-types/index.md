# Paper Type Index

First decide `venue_kind`, then select the corresponding paper type family. Use this top-level index
only when `venue_kind=conference`, which is the default unless the user explicitly specifies a
journal target. The user may select the paper type. If not selected, infer it from the main
contribution, evidence package, target venue, and requested output, then mark the inference in the
Writing Policy. Do not default to `generic-paper.md` before checking the specific profiles. Use
`generic-paper.md` only as a provisional fallback when the type is unknown, mixed, early-stage, or
not safely captured by a specific profile.

Paper type profiles are section and page-budget references only. They help the agent decide which
sections a paper probably needs and how much main-text space each section may require. They are not
fixed templates, and they must be adapted to the actual paper, venue, evidence, and user request.

## Conference vs Journal: Pick The Family First

Paper types are split by `Venue Kind` (see `references/venues/index.md`):

- **Conference** (`Venue Kind: conference`, the default): use the conference paper-type files listed
  in this file (`method-paper.md`, `systems-implementation-paper.md`, `benchmark-dataset-paper.md`,
  `imrad-paper.md`, `survey-paper.md`, `generic-paper.md`). These assume a hard page limit.
- **Journal** (`Venue Kind: journal`, e.g., JMLR, TPAMI): use the journal paper-type files under
  `references/paper-types/journal/` (see `references/paper-types/journal/index.md`). Journal types
  use different section conventions, are usually longer/complete, set a proportional budget, and take
  absolute length from the venue card. Also load `references/venues/journal-vs-conference.md`.

Conference and journal paper types are intentionally NOT shared. Do not draft a journal paper from a
conference paper-type file, and vice versa.

## Conference Type Selection Map

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
