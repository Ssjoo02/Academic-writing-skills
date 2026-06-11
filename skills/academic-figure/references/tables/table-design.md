# Table Design

Use this reference whenever the confirmed Paper Framework contains a table. The goal is to make
table span, column layout, and emphasis predictable instead of left to taste.

## Table Contract

Before writing LaTeX for a table, record these fields in working notes or
`paper/framework-execution-report.md`:

```text
Table ID:
Table kind:
Message:
Body placement:
Target span:
Span justification:
Width budget:
Column strategy:
Numeric precision:
Highlight rule:
Fallback:
```

One table should carry one message. If a table mixes taxonomy definitions, aggregate metrics, and
error analysis, split it or move the complete version to the appendix. If a table is only a glossary,
inventory, complete task list, or name/definition dump, it normally belongs in the appendix; keep only
a compact body summary when the taxonomy is needed for the argument.

## Span Decision

Choose span from content width and reader task, not importance alone. Do not stretch sparse content
across the page just because it is important.

| Table kind | Default span | LaTeX structure | Column strategy | Promote / split when |
|---|---|---|---|---|
| taxonomy / definitions | single-column or appendix | `table` + `tabularx{\linewidth}` | short code/count columns plus one wrapping prose column | prose wraps to one-word lines or the body table becomes a glossary dump |
| compact ablation | single-column | `table` + `tabular` | method/setting column plus 2-4 aligned numeric columns | >=6 numeric columns or long headers |
| main results | full-width when dense | `table*` + `tabular*{\textwidth}` in two-column templates; `table` + `tabular*{\textwidth}` in one-column templates | model column plus aligned numeric columns, use `@{\extracolsep{\fill}}` only when columns need the width | if sparse, keep single-column and state the main number in prose; if >=10 columns, split, rotate, or move full version to appendix |
| model x dataset matrix | double-column / rotated | `table*`, split tables, or rotated table | abbreviate column headers; explain full names in caption/prose | still unreadable at `\textwidth` |
| qualitative examples | single-column by default | `table` + `tabularx{\linewidth}` | one short key column plus wrapping example/notes column | examples become paragraph-length: move to appendix |
| appendix full matrix | double-column / split | same width rules as body | never leave a wide matrix in single-column `table` | dense or very wide: split by metric/category |

In a two-column paper, the main text should usually have at most one cross-column table: the
load-bearing main-results table. Other body tables stay single-column unless they are genuine wide
matrices. In a one-column paper, do not use `table*`; use a normal `table`, with intrinsic width for
small tables and `tabular*{\textwidth}` / `tabularx{\textwidth}` only for dense full-width tables.

Full-width tables need a span justification. A `table*` whose `tabular` sits narrow in the middle of
the page is a defect; use a real full-width layout only when the content needs it, or keep the table
single-column. An unjustified double-column table plan is also a defect: compact ablations,
taxonomy/definition tables, setup/protocol tables, and qualitative example lists should be
single-column or appendix material.

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

- Use `booktabs`; never use `\hline` or vertical rules.
- Caption goes above the table and before `\label`.
- Numeric columns use `r`, `c`, or `siunitx S`; do not stretch numbers with `X`/`Y`.
- Prose cells use wrapping `X`/`Y` or fractional `p{...}` widths tied to `\linewidth` or
  `\textwidth`.
- Keep numeric precision consistent within each metric column.
- Mark metric direction in headers or caption (`ASR $\downarrow$`, `TCR $\uparrow$`).
- Use bold for best/target values sparingly. Color is optional and must be pale, redundant, and
  grayscale-safe.
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
