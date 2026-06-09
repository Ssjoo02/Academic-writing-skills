# Figures And Tables Principles

## Section Role

Figures and tables shape the paper's first impression and argument. They are part of the research
story, not decoration.

## Teaser Figure

Use a teaser figure when the paper benefits from an immediate visual summary of task, failure case,
method idea, benchmark setting, or surprising result.

The teaser figure should:

- make the paper look concrete and memorable,
- show the central problem or contribution,
- avoid overcrowded text,
- align with the Introduction's story.

## Pipeline Figure

A pipeline figure should highlight novelty. It is not only for explaining the workflow; the prose
should still make the method understandable.

Rules:

- If the whole pipeline is novel, show the full input-to-output structure.
- If only one module is novel, highlight novel module clearly.
- If a full pipeline figure makes the work look unoriginal, use focused subfigures.
- Connect the figure to the Method Tree and section plan.

## Result Figures

Use result figures to show qualitative differences, failure modes, stress tests, or application
potential that tables cannot communicate.

Each figure should have:

- one message,
- clear labels,
- matched comparison conditions,
- caption with setting and notation.

## Table Design

Rules:

- Put caption above the table.
- **Use booktabs rules** (`\toprule`, `\midrule`, `\bottomrule`, `\cmidrule`). Never use `\hline`,
  never use vertical rules (`|`). A table built from `\hline` is a defect — rebuild it.
- Avoid vertical rules and dense horizontal lines.
- Group columns with clear headings.
- Mark metric direction such as higher-is-better or lower-is-better.
- Use restrained highlighting for target numbers.

#### Single-column vs. cross-column (`table` vs. `table*`)

In a two-column venue, **column span is a deliberate choice driven by how wide the content truly
is — it is not a property of how "important" the table is.** Default to single-column; widen only
when the content needs it.

- **Keep it single-column (`table`, `\columnwidth`)** when the content fits one column at a normal
  font. This is the right home for most **taxonomy / definition / example / ablation-with-few-columns**
  tables. A prose cell wrapping to **2–3 lines is normal and acceptable** in a single-column table —
  do **not** promote a table to `table*` merely to remove a little prose wrapping.
- **Use cross-column (`table*`, `\textwidth`)** only when the table genuinely needs the horizontal
  room: the **headline/main results table**, a **wide model×metric matrix**, any table with **≳5–6
  numeric columns**, or a table whose cells become unreadable in one column (e.g., wrapping to one
  word per line). The main results table is *usually* such a table, so it is *usually* cross-column —
  but verify against its actual column count rather than promoting reflexively.
- When you do use `table*`, it **must fill `\textwidth`** (see Width Contract) — a `table*` that
  floats narrow in the middle of the page span is a defect. If a table is too narrow to fill
  `\textwidth` cleanly, that is a signal it should have stayed single-column.
- **Decide per table — never blanket-promote.** Do not convert every table in the paper to `table*`
  just because one of them (the main results) needs it. A definition table with a single prose
  column (e.g. `ID | Name | Description`) belongs in one column even if Description wraps; only when a
  cell genuinely cannot fit — confirmed by a compile-time overfull `\hbox` *and* failure to recover
  by abbreviating headers/cells — do you escalate. **Measure, don't guess:** after sizing a table,
  render the page and look (the `≳5–6 columns` heuristic is a prompt to check, not an order to widen).

#### Column widths

- **Size columns to content.** Short or categorical columns (an index, a count, a yes/no) stay
  narrow; long-text columns get the width. Aim to keep each cell on **one line** where the content
  reasonably allows — avoid unnecessary mid-cell wrapping caused by giving every column equal width.
- With `tabularx`, do not make every column an equal-weight `Y`: keep short columns as `l`/`c`/`r`
  and let only the genuinely long column(s) be `Y` (or weight them, e.g.
  `>{\hsize=.6\hsize}X` vs `>{\hsize=1.4\hsize}X`).
- If trimming `\tabcolsep` and right-sizing columns still leaves heavy wrapping in a single column,
  *consider* (not require) cross-column — but only if the table also meets the cross-column test
  above. Otherwise shorten cell text (abbreviate names, move detail to a footnote) instead.

#### Never let a table overflow (body *and* appendix)

A table whose content is wider than its declared container is a **hard defect**: it prints into the
margin or the neighbouring column and overlaps text. This applies **equally to appendix and
supplementary tables — the appendix is not exempt** (most overflow defects hide there, because
authors paste wide numeric matrices into a plain single-column `table`). When a table does not fit,
escalate in this order:

1. **Exceeds `\columnwidth` but fits `\textwidth` → make it cross-column `table*` filling
   `\textwidth`.** Most many-column numeric tables, per-model/per-app/per-category result matrices,
   and any table with long header labels (e.g. full model names) belong here, **including in the
   appendix**. Do not leave them as a single-column `table`.
2. **Still exceeds `\textwidth` → rotate or split.** Rotate with `rotating` (`sidewaystable`) /
   `\rotatebox`, split the table by column groups into two tables, or transpose so the long dimension
   becomes rows.
3. **Only after the layout is correct**, `\small`/`\footnotesize` or a final
   `\resizebox{\textwidth}{!}{...}` may be a last touch for numeric tables with short cells — never
   the first fix, and never for prose-heavy tables.

Rule of thumb: a numeric table with **≳6 columns**, or with long header text, will not fit one
column — default it to `table*`. A table with **≳10 columns** usually needs rotation or splitting
even at full width. Treat any compile-time overfull `\hbox` originating in a `tabular` as this defect.

#### The appendix has the opposite failure: sparse, scattered floats ("太空")

In the **body** the risk is *overflow* (content too wide for its budget). In the **appendix** the
page budget is gone, so the dominant defect flips to *under-density*: short floats scatter across the
page with large empty vertical bands, and each appendix "section" is a one-line pointer (`Table~N
provides ...`) followed by a bare float. The result reads as half-empty pages and a table dump, not
supporting material. Treat a sparse, float-only appendix as a defect to fix, the same way you treat
an overflowing body table.

Causes and fixes:

- **Stacked full-width `table*[t]` floats scatter.** Three `table*` with `[t]` placement and nothing
  between them get pushed to page tops and spread with `\textfloatsep`/`\floatsep` fill, leaving big
  white gaps. Fix by (a) **not reflexively widening** — most appendix definition / config / boundary
  tables fit one column and pack tight as plain `table` (apply the body's single-vs-cross-column
  test to appendix tables too); (b) **anchoring each float with real prose** so the surrounding text
  fills the page; and/or (c) **placing appendix tables non-floating** under their heading so they sit
  where written instead of drifting.
- **Pin placement deliberately in the appendix — and never use `[h]` alone.** `[h]` ("here only")
  is the most fragile specifier: when the float does not fit, it is pushed onto a *deferred* queue.
  Because LaTeX keeps **separate queues for figures and tables**, a deferred table can be flushed
  *after* figures that come later in the source, so the floats stop appearing in section order and
  the appendix looks scrambled (a figure surfacing above an earlier section's table). In an appendix
  where each section owns one float, **pin every float so its order follows the headings**: use
  `[H]` (from the `float` package) to lock the float exactly under its heading, or `[ht]`/`[tbp]`
  plus a `\FloatBarrier` (from `placeins`) — or a deliberate `\clearpage` — after each appendix
  section so no float migrates across a heading. Do **not** use bare `[h]`, and do **not**
  scatter-control with blank `\vspace`. (This needs `\usepackage{float}` for `[H]` and/or
  `\usepackage{placeins}` for `\FloatBarrier` in the generated preamble.)
- **Respect the venue: some templates forbid `float` / `\clearpage`.** `[H]` needs
  `\usepackage{float}` and the heading-figure unit uses `\clearpage` — but a few venues ban both
  (e.g. the AAAI author kit explicitly forbids `\usepackage{float}` and any `\clearpage`). When the
  selected template forbids them, **do not add them**; fall back to robust *floating* placement —
  `[!ht]` or `[tbp]` (still **never** bare `[h]`) plus column/section-local `\FloatBarrier` if
  `placeins` is allowed — and rely on the natural float order. Check the template's preamble comments
  before reaching for `[H]`/`\clearpage`.
- **`[H]` and `\clearpage` have sharp edges — size to fit, do not blanket-apply.** `[H]` does not
  float: if the float does not fit the remaining space it page-breaks *before* itself (stranding the
  preceding text) or overflows the bottom margin (`Overfull \vbox`). It is safe only when you
  guarantee room — pair it with a fresh page and **size the float to share the page with its
  heading + lead paragraph** (shrink the figure or trim a wide table if needed). Do **not**
  `\clearpage` before every appendix section: a `\clearpage` before a short section leaves a
  near-empty page — exactly the "太空" defect above. Use `\clearpage`/`[H]` *surgically* on the
  float-heavy sections that actually reorder, not as a blanket rule. (This is the
  pin-and-size-to-fit discipline; over-pinning trades scramble for emptiness.)
- **A wide appendix float must still be `table*`/`figure*`, not a single-column `[h]` float.** A
  many-column matrix (e.g. model × 9 apps) left in a single-column `table` overflows into the
  neighbouring column and collides with the next section's floats — which reads as "out of order"
  on top of the overflow. Apply the overflow ladder (`table*` → rotate/split) *before* pinning
  placement.
- **Every appendix (sub)section earns a lead paragraph, not a pointer.** 2–4 sentences that say what
  the material is, how to read it, the one or two patterns worth noticing, and which main-text claim
  it backs. A section whose entire prose is `Table~N gives ...` is the "太空" smell — expand it.
- **The appendix carries the *full* version, never a stub.** Do not relegate sketch-only content or
  leave `see supplementary material` pointers in place of content that exists. If the body summarizes
  a taxonomy, protocol, proof, or result matrix, the appendix holds the complete, self-contained
  version (this is also what makes the pages substantive rather than empty).

Substantive material that belongs in a well-filled appendix: full definitions / taxonomies that the
body mentions in one stroke, complete per-item / per-model / per-category result matrices, full
proofs or derivations (body keeps the sketch), dataset and annotation protocol details, exact
prompts and agent / hyperparameter configurations, extra ablations and robustness checks, and
additional qualitative examples. Group these under labeled appendix sections (A, B, C…) ordered to
mirror the main paper, each reachable by a main-text forward reference.

#### Highlighting and emphasis (general)

- For **"baselines vs. ours"** comparisons, place your method in the **last row**, separated by a
  `\midrule`, and **bold the best value per column** (optionally underline the runner-up).
- **Color is optional and must degrade gracefully.** If you shade, use a *light, single-hue*
  `\rowcolor`/`\cellcolor` (e.g. a pale gray or pale blue) only to mark the "ours" row or the
  best cell — never a saturated color, never multiple competing hues. The table must remain readable
  in grayscale and for colorblind readers, so color is always a redundant cue on top of bolding,
  never the only signal. Some venues discourage color in tables; when unsure, rely on bolding alone.
- When the table only compares external systems (no "ours" entry), do **not** force a bottom row or
  highlight — group by category and bold the extremes.

### Width Contract

Every table must declare its target layout before it is written:

- `single-column`: the table must fit within `\linewidth` or `\columnwidth`.
- `double-column`: use `table*` and **fill** `\textwidth` — a `table*` must not sit narrow in the
  middle of the two-column span. Make the tabular span the full width with
  `\begin{tabular*}{\textwidth}{@{\extracolsep{\fill}}...}` (numeric columns, no wrapping) or
  `\begin{tabularx}{\textwidth}{...}` (with `X`/`Y` columns when cells wrap). Adding a few `\fill`
  gaps is preferred over leaving a cramped table floating in white space.
- `appendix`: apply the **same width contract and the same overflow ladder as the body** — a wide
  appendix table must be `table*` (or rotated/split), never a single-column `table` left to spill.
  Appendix placement is not a license to exceed the printable area. **Also guard the opposite defect**
  (see "The appendix has the opposite failure"): do not scatter narrow `table*[t]` floats across
  half-empty pages — keep tables that fit one column single-column, anchor each with real prose, and
  pin placement so floats sit under their heading.
- `supplement`: move very wide, dense, or complete result matrices out of the paper body when even a
  rotated or split in-paper table would be unreadable.

Do not rely on `\small`, `\footnotesize`, or `\resizebox` as the primary solution for long-text
tables. Font reduction is only a secondary adjustment after the column layout is correct.

### Table Toolbox

When a draft contains any nontrivial table, ensure the generated LaTeX preamble has the portable
table toolbox below unless the selected venue explicitly forbids these packages:

```tex
\usepackage{booktabs}        % REQUIRED for any table — \toprule \midrule \bottomrule \cmidrule
\usepackage{array}
\usepackage{tabularx}
\usepackage{colortbl,xcolor}  % subtle highlight of best/target numbers
\newcolumntype{Y}{>{\raggedright\arraybackslash}X}
\newcolumntype{Z}{>{\centering\arraybackslash}X}
```

**Do not stretch numeric columns with `tabularx` `Y`/`Z`** — they left-rag and unevenly space
numbers. Numeric columns use `r`/`c` (or `siunitx` `S`); a pure-numeric results table needs no
`tabularx` at all (`\begin{tabular}{l rrrrr}` with booktabs). Use `tabularx` only when a table has a
prose column, long wrapping labels, or qualitative cells:

```tex
\begin{table}[t]
\centering
\caption{...}
\label{tab:...}
\small
\setlength{\tabcolsep}{3pt}
\begin{tabularx}{\linewidth}{@{}llrY@{}}
\toprule
...
\bottomrule
\end{tabularx}
\end{table}
```

Use fixed `p{...}` columns only when their widths are fractions of `\linewidth` or `\textwidth`;
do not use absolute widths such as `p{6.5cm}` in a two-column single-column table unless that width
has been checked against the actual column width.

Use `\resizebox{\linewidth}{!}{...}` only for numeric tables with short labels, and only when the
result remains readable. Do not use `resizebox` for taxonomy, example, limitation, or qualitative
tables with prose cells; use wrapping columns or split the table instead.

### Table Pattern Selection

- Taxonomy or example table with prose explanations: **single-column** `table` + `tabularx{\columnwidth}`
  with one `Y` column (short label columns stay `l`/`c`). 2–3 line wrapping in the prose column is fine.
- Compact metric table with short labels: normal `tabular`, optionally `\footnotesize`, bounded by
  `\linewidth`; switch to `table*` only if more than 5-6 metric columns are needed.
- Wide model-by-dataset or model-by-task table: `table*` with `\textwidth`, or split by metric.
- Complete per-task, per-example, or many-row appendix table: summarize in paper and release the
  complete table as supplementary data unless a readable table fits.

## Caption Rules

Captions should state experimental setting, notation, and the main reading instruction. Do not use
captions for long discussion that duplicates the main text.

## Self-Check

- Does each visual carry one message?
- Does the pipeline figure make novelty visible?
- Can the table be read without guessing metric direction or protocol?
- Does each figure/table fit the declared single-column or double-column width?
- Do all long table cells wrap instead of crossing into margins or neighboring columns?
- Does the appendix read as substantive (every section has a real lead paragraph, floats sit under
  their heading, no half-empty pages or bare table dumps), not just structurally correct?
- Is visual polish consistent with target venue expectations?
