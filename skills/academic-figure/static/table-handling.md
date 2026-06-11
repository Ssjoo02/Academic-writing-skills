# Table Handling

Execution rules for producing every table in a paper draft. Pair this with `figure-handling.md`. The
deep reference lives at `references/tables/table-design.md`; prose/appendix placement rules live at
`references/sections/figures-and-tables.md`.

1. Read every table entry from the confirmed Figure Plan, including its `Layout` value. Load
   `references/tables/table-design.md`, classify each table by `table kind`, and record `table kind`,
   `body placement`, `target span`, `span justification`, `width budget`, `column strategy`, and
   `fallback` in `paper/framework-execution-report.md` before writing LaTeX.
2. **Always use `booktabs` rules** (`\toprule`, `\midrule`, `\bottomrule`, `\cmidrule`). Never use
   `\hline`, never use vertical rules (`|`), and never stack repeated `\hline`. A table built from
   `\hline` is a hard defect — rebuild it with booktabs.
3. **Column span follows content width, not importance.** Default to single-column `table`
   (`\columnwidth`). Use cross-column `table*` (`\textwidth`) only when the content genuinely needs
   the room: the headline/main results table, a wide model×metric matrix, any table with ≳5–6 numeric
   columns, or a table whose cells become unreadable in one column. The main results table is
   *usually* such a case, so it is *usually* cross-column — but check its actual column count instead
   of promoting reflexively. **Taxonomy / definition / example tables with a couple of columns stay
   single-column**; a prose cell wrapping to 2–3 lines is normal there and is **not** a reason to go
   cross-column.
3b. **Full-width tables require justification.** In a two-column paper, the main text should usually
   have at most one cross-column table: the load-bearing main-results table. Wide result matrices may
   also be cross-column; compact ablations, taxonomy/definition tables, setup/protocol tables, and
   qualitative examples stay single-column or move to the appendix. In a one-column paper, do not use
   `table*`; use a regular `table`, with intrinsic width for small tables and
   `tabular*{\textwidth}` / `tabularx{\textwidth}` only when a dense table actually needs the span.
   A `table*` whose `tabular` sits narrow in the middle of the page is a defect — either give it a
   real full-width layout because the content needs it, or move it back to single-column.
3c. **Size columns to content and keep cells on one line where the content reasonably allows.**
   Short/categorical columns narrow, long-text columns wide; do not give every column equal `Y`
   width. Reduce `\tabcolsep` and right-size columns before considering any width change; only widen a
   prose-heavy single-column table to `table*` if it *also* meets the cross-column test in rule 3 —
   otherwise abbreviate cell text instead.
3d. **Never let a table overflow — body or appendix.** A table wider than its container is a hard
   defect (it spills into the margin / neighbouring column and overlaps text). **Appendix tables obey
   the same rule** — do not paste a wide numeric matrix into a single-column `table`. Escalate:
   (i) exceeds `\columnwidth` but fits `\textwidth` and has a full-width justification → `table*`
   filling `\textwidth` in a two-column template, or regular `table` + `tabular*{\textwidth}` in a
   one-column template; (ii) still exceeds `\textwidth` → rotate (`sidewaystable`/`\rotatebox`),
   split by column groups, or transpose;
   (iii) only then apply `\small`/`\footnotesize`/`\resizebox` as a last touch for short-cell numeric
   tables. A numeric table with ≳6 columns or long header labels (e.g. full model names) must first
   be classified: main-results or genuine wide-matrix tables may be full-width; compact secondary
   tables should be split, abbreviated, or moved to appendix instead of being stretched.
3e. **Generate width-safe table source on the first pass.** Do not write a table first and hope the
   audit catches it later. If a table has long task IDs, definitions, examples, or notes, use
   `tabularx{\linewidth}` / `tabularx{\textwidth}` with a wrapping `Y`/`X` or fractional `p{...}`
   column; do not put prose-heavy cells in plain `l`, `c`, or `r` columns. If a table has six or more
   numeric/model columns, start from the full-width pattern only when the table is a main-results or
   genuine wide-matrix table; otherwise split it or move detail to the appendix. Abbreviate headers
   and expand names in the caption or lead paragraph. A generated `\begin{table}[H] ... \begin{tabular}{l r r r r r}`
   appendix matrix is a workflow violation, not a draft to "polish later."
3f. **Long headers overflow narrow columns even at a small column count.** A single-column table at a
   two-column venue whose header cells are verbose (e.g. `Defend Rate (\%)`, `Execution Rate (\%)`,
   `Stalled/Other (\%)`) will exceed `\columnwidth` even with only 3–4 columns — the column-count
   heuristic will not catch it, but the compiled PDF will overflow. Abbreviate numeric headers to short
   tokens (`DR (\%)`, `ER (\%)`, `Other (\%)`) and expand them in the caption or lead sentence, or
   promote the table to `table*`. Do not ship a body results table that overflows because of verbose
   headers; check the rendered width, not just the column count.
4. Use `single-column` `table` only when the full table fits within `\linewidth` / `\columnwidth`.
5. **Column types must match cell content.** Use `r` (or `c`, or `siunitx` `S` for decimal
   alignment) for numeric columns — never stretch numbers with `tabularx` `Y`/`Z`, which left-rags
   and unevenly spaces them. Reserve `tabularx` `Y`/`Z` columns for long labels, example text,
   taxonomy descriptions, qualitative cases, and prose-heavy cells only. A numeric results table
   normally needs no `tabularx` at all: `\begin{tabular}{l rrrrr}` with booktabs is correct.
6. Mark metric direction in headers (`ASR ↑`, `LPIPS ↓`) and **bold** the best (or target) value per
   column. For "baselines vs. ours" tables, put your method in the last row below a `\midrule`. Color
   is optional and must stay redundant with bolding: at most a single light `\rowcolor`/`\cellcolor`
   (pale gray/blue) on the "ours" row or best cell, readable in grayscale; never saturated or
   multi-hue. When unsure of venue norms, use bolding alone.
7. Use fixed `p{...}` columns only when the widths are expressed as fractions of `\linewidth` or
   `\textwidth`; avoid absolute widths that can exceed a venue column.
8. Use `\resizebox{\linewidth}{!}{...}` only for compact numeric tables with short labels and only
   after checking that the rendered text remains readable; never as the primary fix for a too-wide
   table — promote it to `table*` first.
9. Split the table or move the complete version to supplementary material when neither single-column
   nor double-column layout is readable.
10. After compiling, inspect **every** PDF page containing a figure or table — **body, appendix, and
    supplementary alike**. If any item crosses a margin, overlaps another column, has clipped
    labels/columns, uses `\hline`, or becomes unreadable, treat it as a **blocking** defect: apply the
    overflow ladder in rule 3d (table* → rotate/split → resize), revise, and recompile before
    returning the draft. A compile-log overfull `\hbox` whose source is a `tabular` is this defect —
    do not dismiss it as cosmetic.
10b. **No unresolved rendered references.** After compiling, inspect the PDF text and compile log for
    `Table ??`, `Figure ??`, `Section ??`, undefined references, and undefined citations. Any `??`
    marker or LaTeX undefined-reference/citation warning is a **blocking** defect: fix the missing
    `\label{...}` / `\ref{...}` / BibTeX entry, remove invalid LaTeX such as `\end{section}`, and
    recompile until the rendered PDF contains no unresolved reference markers. Never return text like
    `Table ?? provides ...` to the user.
10c. **Never hard-code structural numbers in source.** Write `Section~\ref{...}`,
    `Table~\ref{...}`, `Figure~\ref{...}`, and `Appendix~\ref{...}`; do not write `Section~5.4`,
    `Table 2`, or similar manual numbers. Add labels at generation time for every section, subsection,
    figure, table, equation, and appendix target that is referenced. Hard-coded structural numbers are
    stale-reference defects and are blocked by `audit_draft.py` (run from the `academic-review` skill).
11. **Design the appendix against the opposite defect — sparseness, not overflow.** Once the page
    budget is gone, the failure mode flips: short floats scatter across half-empty pages and each
    appendix section becomes a one-line pointer (`Table~N provides ...`) plus a bare float ("太空").
    On the same inspection pass, treat a half-empty / table-dump appendix page as a defect to fix.
    (a) **Do not reflexively widen** — appendix definition / config / boundary / example tables that
    fit one column stay single-column `table` and pack tight; apply the same single-vs-cross-column
    test as the body. (b) **Anchor every appendix (sub)section with a real lead paragraph** (2–4
    sentences: what it is, how to read it, the pattern worth noticing, which main claim it backs), not
    a pointer.     (c) **Pin float placement and keep order — never use bare `[h]`.** `[h]` ("here only") defers
    when it does not fit, and because figures and tables sit in **separate float queues**, deferred
    floats resurface out of section order (a later figure printing above an earlier section's table),
    which reads as "图顺序乱". In the appendix (one float per section), lock each float under its
    heading with `[H]` (the `float` package), or use `[ht]`/`[tbp]` plus a `\FloatBarrier`
    (`placeins`) / deliberate `\clearpage` after each appendix section. Add `\usepackage{float}` /
    `\usepackage{placeins}` to the generated preamble when needed. Never pad with blank `\vspace`.
    A wide appendix matrix must first go `table*`/rotate/split (rule 3d) — a single-column `[h]` wide
    table overflows into the next column and compounds the disorder.
    **Two balances:** (i) *Venue limits* — some templates forbid `\usepackage{float}` and `\clearpage`
    (e.g. the AAAI author kit). When forbidden, do not add them; fall back to `[!ht]`/`[tbp]` (still
    never bare `[h]`) + `\FloatBarrier` if allowed, and rely on natural order. (ii) *Do not over-pin*
    — `[H]` does not float (it strands preceding text or overflows if it does not fit), and a
    `\clearpage` before every section leaves near-empty pages (the "太空" defect of rule 11 above).
    Size each pinned float to share its page with its heading + lead paragraph, and apply
    `[H]`/`\clearpage` only to the float-heavy sections that actually reorder.
    (d) **Carry the full version, never a stub** — no `see supplementary material` placeholder in
    place of content that exists, and no sketch-only appendix. See `references/sections/figures-and-tables.md`
    ("The appendix has the opposite failure") for the substantive-material menu and float discipline.
