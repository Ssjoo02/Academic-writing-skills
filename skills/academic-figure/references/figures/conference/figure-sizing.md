# Conference Figure Sizing

Load this file for **conference papers** after `plot-style.md`. It contains the
conference-calibrated figure sizes, font size hierarchy, LaTeX inclusion rules,
and height budget. All other plotting rules (rcParams, colors, per-chart-type
rules, legend rules, multi-panel architecture) are in `plot-style.md`.

## Figure Sizes

Match figure width to the target venue's column layout. "Single-column" means
different things in different venues: ~3.0–3.4 in for a two-column conference
(ICML, ACL, CVPR), but ~5.5 in for a one-column venue (NeurIPS, ICLR). Always
check the selected template's actual column width before picking a `figsize`.
The values below assume standard US Letter CS venues; A4 venues (ACL) are
slightly narrower — reduce the width by ~0.2 in.

| Layout context | Example venues | `figsize` (width, height) | Notes |
|---|---|---|---|
| Two-column venue, single column | ICML, CVPR, AAAI, IJCAI, ACL | `(3.25, 2.2)` to `(3.5, 2.8)` | Narrow; ≤4–5 bars side by side; use `\columnwidth` |
| One-column venue, full text width | NeurIPS, ICLR | `(5.5, 3.0)` to `(6.0, 4.5)` | Wider column; can fit more bars or a wider heatmap; use `\textwidth` or `\linewidth` |
| Two-column venue, cross-column (`figure*`) | ICML, CVPR, AAAI (full page) | `(6.5, 3.5)` to `(7, 5)` | Wide enough for grouped bars, heatmaps, radar; use `\textwidth` |
| Square (radar, scatter matrix) | Any | `(5, 5)` to `(6, 6)` | Keep legend inside or directly below the axes |
| Wide multi-panel figure (3+ panels) | Any (full page or cross-column) | `(12, 8)` to `(22, 17)` | Scale proportionally to panel count; see `chart-patterns.md` |

### LaTeX Inclusion

Prefer `width=\columnwidth` or `width=\linewidth`; do not use absolute
`\textwidth` in a two-column context (it overflows the column). For cross-column
figures in a two-column template, use `figure*` with `width=\textwidth`.

### Column-Span Quick Rule (see `figure-planning.md` for the full decision)

In a two-column venue, decide span by role and width need, not figure number:

- **Single-column** (`figure` + `\columnwidth`): the teaser / first concept figure that fits ~3 in, a
  single small plot, a narrow taxonomy/setup table.
- **Cross-column** (`figure*` + `\textwidth`, top/bottom of page): pipeline / framework / architecture
  / system-overview diagrams; multi-panel figures (e.g. two radars side by side); wide grouped-bar /
  heatmap / radar comparisons or wide result tables that go illegible at column width.

A pipeline/framework diagram squeezed into one narrow column is the most common span mistake — give it
`figure*`. Two related comparison charts go in one `figure*` multi-panel with a shared legend, not two
single-column floats. In one-column venues (NeurIPS, ICLR) there is no `figure*`; size by fraction of
`\linewidth` instead.

### Height Budget

At `\textwidth` a 16:9 image is ~9–10 cm tall — too tall for a teaser or
pipeline banner. For concept / banner figures target aspect ~3:1 to 4:1
(~4.5–6 cm tall at double-column width). See `picture-generation.md` for the
height and trim mechanics. For data figures, a useful starting ratio is width ≈
1.5–2× height for comparison plots, 1:1 for radar/scatter, and width ≈ 3–4×
height for bar panels with many categories.

## Font Size Hierarchy

Choose the base `font.size` according to figure type, panel count, and the
venue's column width. Start from the table below; adjust per-figure for
readability at the target column width. The values assume the figure is placed
at the column's native width (`\columnwidth` or `\linewidth`) without shrinking.

| Figure type | Base `font.size` | Axis label | Tick label | In-bar / cell annotation |
|---|---|---|---|---|
| Dense multi-panel (3+ panels, two-column venue single-column) | 7–8 | 8 | 7 | 7–8 |
| Standard single-panel (bar, line, scatter — two-column venue) | 9–10 | 9–10 | 8–9 | 8–9 |
| Standard single-panel (bar, line, scatter — one-column venue: NeurIPS, ICLR) | 10–12 | 10–12 | 9–10 | 9–10 |
| Hero / teaser figure (full page width, single-column venue or `figure*`) | 11–12 | 11–12 | 10 | 10–11 |
| Heatmap with cell text | 8–9 | 9 | 8 | 7–8 (contrast-adaptive) |
| Radar / polar (6+ spokes) | 9 | 9 | 8 | — |

### Venue Adaptation

Two-column venues (ICML, CVPR, AAAI, ACL, IJCAI) have narrow single columns
(~3.0–3.4 in) — start from the "two-column venue" rows above. One-column venues
(NeurIPS, ICLR) have a ~5.5 in text block — use the "one-column venue" row;
9 pt base is the floor, 10–12 pt is typical and reads more comfortably. When a
figure is placed in `figure*` spanning both columns of a two-column venue, use
the "hero / teaser" font row.

**Minimum legibility rule**: No text element may render below 6pt at final column
width. Labels below 7pt should be rare and only for secondary information (tick
labels, legend entries for 5+ methods). When in doubt, render the PNG and check
readability at 100% zoom — the figure will be printed at roughly the same size.

## QA Notes

- **NeurIPS / ICLR (single-column)**: figures fill the 5.5 in text block; base
  font 10–12pt. No `figure*` needed. Use `width=\textwidth`.
- **ICML / CVPR / AAAI / IJCAI (two-column)**: single-column figures ~3.25 in
  wide; use `figure*` only for genuine full-page figures. Most data figures stay
  in one column.
- **ACL (two-column, A4)**: single-column ~3.0 in wide (narrower than US Letter
  venues); reduce figsize width ~0.2 in and check wrapping.
- **IEEE (two-column, US Letter)**: similar to ICML/CVPR; journal mode may be
  single-column.

## Cross-Reference

- `plot-style.md` — rcParams, colors, per-chart-type rules, legend rules,
  multi-panel architecture (load first)
- `chart-patterns.md` — reusable Python plotting helpers
- `picture-generation.md` — AI-generated picture workflow
- `figure-planning.md` — Display Item Contract, Display Review Gate, generation
  routes
- `qa-contract.md` — submission-readiness checklist
