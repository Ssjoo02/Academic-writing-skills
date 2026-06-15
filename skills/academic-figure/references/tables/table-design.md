# Table Design

Use this reference whenever the confirmed Paper Framework contains a table. The goal is to make
table type, visual grammar, LaTeX structure, and emphasis predictable instead of left to taste.
Use `table-placement.md` for body-vs-appendix, span, width, overflow, and supplement decisions.

## Table Contract

Before writing LaTeX for a table, record these fields in working notes or
`paper/framework-execution-report.md`:

```text
Table ID:
Table kind:
Message:
Data source:
Source artifact:
Body-vs-Appendix Decision:
Placement summary:
Visual grammar:
Column strategy:
Numeric precision:
Metric direction status:
Highlight rule:
Fallback:
```

One table should carry one message. If a table mixes taxonomy definitions, aggregate metrics, and
error analysis, split it or move the complete version to the appendix. If a table is only a glossary,
inventory, complete task list, or name/definition dump, it normally belongs in the appendix; keep only
a compact body summary when the taxonomy is needed for the argument.

`Placement summary` is a short pointer to the decision recorded from `references/tables/table-placement.md`.
Do not duplicate placement rules here.

`Data source` is the human-readable origin of the numbers or cells. `Source artifact` is the concrete
workspace file, result table, manifest, config, or user-provided data path used to build the table.
Never invent or "clean up" values that are not in the source artifact.

## Classification Flow

Classify from evidence role first, then data shape. Ask what core claim or reader task the table
serves: headline comparison, cross-dataset generality, metric tradeoff, component necessity,
robustness to a setting, dataset/protocol transparency, benchmark scope, or reproducibility setup.
Then inspect headers and rows: methods/models imply comparison; datasets/tasks imply a matrix;
components or variants imply ablation; one hyperparameter with ordered values implies sensitivity;
split names and counts imply data splits; key-value settings imply configuration. If no Figure Plan is
available, record this as a provisional classification and revise after render inspection.

## Universal Table Visual Grammar

The polished table style is a reusable grammar, not fitted to one dataset, one benchmark, or one
paper's literal model names. Start every paper table from the same clean base: booktabs-only rules,
no vertical boxes, compact but readable spacing, consistent numeric precision, metric directions
where applicable, and a caption that states the evidence role and expands abbreviations.

Then adapt the grammar by table type:

- For scorecards and comparison tables, bold every header level, including the first semantic column,
  spanner headers, and leaf metric headers. Use `\multicolumn` + `\cmidrule` only when metrics or
  datasets form real groups.
- For method-vs-baseline tables, use one explicit separator before an own/proposed/full-method final block.
  If that final block carries the primary win, combine bold best values with one pale
  grayscale-safe row or cell shade.
- For ablations and sensitivity tables, keep the layout compact and emphasize the full/default
  setting instead of decorating every numeric maximum.
- For split, benchmark-summary, and configuration tables, preserve the same booktabs/header/spacing
  polish, but do not use performance-table highlighting; use restrained section labels, totals,
  wrapping prose columns, or phase groups as appropriate.
- For any new paper, infer the table type first and reapply this grammar to the paper's own metrics,
  baselines, tasks, and venue width constraints.

## Metric Direction And Uncertainty

Metric direction belongs in headers or captions whenever the table uses best-value emphasis. Use
arrows (`$\uparrow$`, `$\downarrow$`) or explicit wording. If a numeric metric's direction is not
provided by the source, record `Metric direction unknown` in the contract. In that case, do not guess
metric direction: ask the user, mark the direction as unknown, or omit best-value styling for that
column.
In short: do not guess metric direction.

Counts, dataset sizes, IDs, hyperparameters, latency, and configuration values are not automatically
performance metrics. Do not bold a number just because it is numerically largest.

## Cross-table consistency

Before returning a draft, check table consistency across the paper:

- Keep method order stable across main results, ablations, and robustness tables unless a local
  ordering has a stated reason.
- Use one public method name for the proposed method; do not leak internal run names or aliases.
- Keep metric precision consistent for the same metric across tables.
- Reuse abbreviations and expand them once in captions or prose.
- Keep highlight conventions stable: same own-method row style, same best-value bolding rule, and
  same treatment of default/selected settings.
- Use the same baseline family labels and group ordering when comparable tables share baselines.

## Table Type Pattern Library

Use these reusable patterns for common paper tables. The examples are table types, not fixed layouts;
adapt widths and grouping to the venue and data.

| Table type | Evidence role | Default design | Emphasis rule |
|---|---|---|---|
| central scorecard / main result table | Headline method-vs-baseline comparison | Model/method rows, metric-group spanners, baseline-family labels, Avg./rank if supported; placement comes from `table-placement.md` | Proposed method as final block with separator, bold best values, and light row shade when best |
| multi-dataset comparison table | Shows generality across datasets/tasks | Spanner per dataset or metric family; abbreviate dataset names and expand in caption; placement comes from `table-placement.md` | Bold best per dataset/metric; avoid shading every best cell if it creates noise |
| multi-metric comparison table | Shows tradeoffs across several metrics | Metric directions in headers; group related metrics when the grouping is real; placement comes from `table-placement.md` | Bold best/target values; use spanners only when metric families are natural |
| ablation table | Shows component or design-choice necessity | Compact single-column by default; rows progress from baseline/removed components toward full method; use checkmarks or short variant labels sparingly | Separate and shade the full method only if it is the proposed final row; otherwise bold the decisive deltas |
| hyperparameter sensitivity table | Shows robustness to a parameter or threshold | Single-column ordered sweep; keep the parameter column left/center and metrics aligned; include the selected/default setting row | Highlight the selected/default setting row; do not force best-value styling if the point is stability |
| data split table | Documents train/dev/test or source/domain composition | Setup/protocol table; counts and percentages; group by dataset/domain/task; use integer formatting and compact headers | No performance highlights; bold only split names or totals when helpful |
| benchmark summary table | Summarizes benchmark scope, tasks, or annotation attributes | `tabularx`/wrapping columns for descriptions; compact codes plus counts; full-width only when many attributes must be compared | Use restrained category labels; not performance highlights |
| training configuration table | Documents reproducibility settings | Key-value or phase-grouped layout, often single-column or appendix; group optimization, data, hardware, and inference settings | No best-value styling; bold setting names or phase labels only |

Sensitivity, split, benchmark, and configuration tables are not result scorecards: use the
selected/default setting row for sensitivity, counts and percentages for split tables, a key-value or
phase-grouped layout for training configuration, and not performance highlights for benchmark/setup
summaries.
For training configuration specifically, use a key-value or phase-grouped layout.

## LaTeX Patterns

Single-column prose table:

```tex
\begin{table}[t]
\centering
\caption{...}
\label{tab:...}
\small
\setlength{\tabcolsep}{3pt}
\begin{tabularx}{\linewidth}{@{}l r Y@{}}
\toprule
Code & Count & Definition \\
\midrule
...
\bottomrule
\end{tabularx}
\end{table}
```

Double-column numeric table:

```tex
\begin{table*}[t]
\centering
\caption{...}
\label{tab:...}
\small
\setlength{\tabcolsep}{3pt}
\begin{tabular*}{\textwidth}{@{\extracolsep{\fill}}l r r r r r@{}}
\toprule
Model & ASR $\downarrow$ & TCR $\uparrow$ & Exec & Def & RF \\
\midrule
...
\bottomrule
\end{tabular*}
\end{table*}
```

## Style Rules

- **Polished scorecard default.** The polished style is not example-specific: for any future paper,
  adapt the same visual grammar to the paper's metrics, baselines, and venue constraints. Use
  booktabs, bold headers, metric-group spanners when natural, restrained category labels, a separator
  before the own-method row, and redundant bold-plus-light-shade emphasis for the proposed method
  when it is the final best row.
- Use `booktabs`; never use `\hline` or vertical rules.
- For polished main tables, use **heavier top/bottom booktabs rules** by setting `\heavyrulewidth`
  modestly or replacing only the outer rules with `\specialrule`; keep interior rules fine and
  **never box the table**.
- Caption goes above the table and before `\label`.
- Numeric columns use `r`, `c`, or `siunitx S`; do not stretch numbers with `X`/`Y`.
- Prose cells use wrapping `X`/`Y` or fractional `p{...}` widths tied to `\linewidth` or
  `\textwidth`.
- Keep numeric precision consistent within each metric column.
- Mark metric direction in headers or caption (`ASR $\downarrow$`, `TCR $\uparrow$`).
- For polished scorecards, use **multi-level column headers** when metrics naturally form groups:
  create `\multicolumn` spanners with `\cmidrule`, use **bold spanner headers**, and use **bold leaf
  column headers** for the metric names. Keep the first column header bold as well.
  In short: use bold spanner headers and bold leaf column headers.
- Use bold for best/target values sparingly. If the proposed method is the final row and is best on
  the primary comparison, use one light `\rowcolor`/`\cellcolor` shade on the row or target cells;
  the shade must be **redundant with bold**, pale, single-hue, and grayscale-safe.
- When the proposed method is the final block, add a visual separator **before the own-method row**:
  separate it with a `\midrule` or fine `\specialrule` before the shaded/bold row. This makes the
  method row read as a deliberate conclusion rather than another baseline.
- For a category comparison, use italic group labels, `\addlinespace`, and fine grouping rules such
  as `\cmidrule`; do not create boxed blocks or repeated heavy rules.
- `\resizebox` is a last resort for short-cell numeric tables. Do not use it to shrink prose-heavy
  tables into unreadable text.

## QA Gate

After compilation, render the page containing every table and inspect it. A table fails if:

- it crosses a margin or overlaps another column,
- a `table*` does not fill `\textwidth`,
- prose appears in non-wrapping `l/c/r` columns,
- numeric columns have inconsistent precision or ragged alignment,
- metric direction / best-value convention is unclear,
- the caption is a long discussion instead of setting + notation + message.
