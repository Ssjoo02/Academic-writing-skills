# Plot Workflow

Execution-only workflow for data-driven figures: bars, grouped/stacked bars, lines, heatmaps,
radars, scatter/Pareto plots, distributions, pies/donuts, and multi-panel combinations.

## Workflow

1. Read the confirmed Figure Plan entry when present. Record or update the item's row in
   `paper/framework-execution-report.md` for paper-level runs.
2. Load `references/figures/figure-planning.md` and fill the Display Item Contract: core
   conclusion, evidence chain, display type, backend, export contract, and layout target.
3. Load `references/figures/chart-taxonomy.md` before writing code. Record chart family, source
   file, statistic/interval, palette preset, label strategy, and export bundle for each panel.
   For paper-level runs, also run a **cross-figure chart-form audit** before rendering: compare the
   planned numeric display items and avoid defaulting every numeric plot to bars. Match the chart to
   the claim first: composition / coverage snapshots may use donut, pie, stacked bar, or heatmap;
   exact across-category comparisons may still use bars; trends use lines; matrices use heatmaps.
4. Load `references/figures/plot-style.md`, then the venue sizing reference:
   - Conference: `references/figures/conference/figure-sizing.md`
   - Journal: `references/figures/journal/figure-sizing.md`
5. Load `references/figures/chart-patterns.md` only when reusable helper patterns are needed.
   Default to Python/matplotlib unless the user explicitly requests another backend.
6. Read numeric values from workspace result files. Do not hardcode or invent values.
7. Export SVG (editable text), PDF (LaTeX inclusion), and PNG (visual inspection preview) under
   `paper/figures/`.
8. Open the rendered PNG and run the Display Review Gate in `figure-planning.md`. Regenerate on
   muddy overlap, clipped elements, low contrast/color-only encoding, label collision, overflow, or
   inconsistent visual encoding.
9. Insert only in the section and width target confirmed by the Paper Framework. Captions must state
   the plotted message and supported claim.

After all plots pass their individual gates, run the cross-figure checklist in
`references/figures/qa-contract.md`.
