# Chart Taxonomy And Design Gate

Use this reference for data-driven paper plots after the Display Item Contract is written and before
plotting code is created. It turns a claim + data shape into a chart family, layout target, palette
strategy, label strategy, statistics note, and export bundle.

## Data-Chart Design Gate

Do this before any plotting script:

1. **Core conclusion first.** Write one sentence with a verb. Example: "The proposed method improves
   average accuracy while keeping latency near the baseline." Do not start from a favorite chart type.
2. **Evidence chain.** Map every panel to one concrete source file/table and one claim. If a panel
   does not add unique evidence, remove or merge it.
3. **Data and statistics contract.** Record columns, metric direction, unit, denominator, sample size
   or seed count, center/spread definition, and whether uncertainty is std/sem/CI/IQR/bootstrap.
4. **Layout contract.** Pick `single-column`, `double-column`, `appendix`, or `supplement`; for
   one-column templates, record the `\linewidth` fraction instead of using `figure*`.
5. **Palette and label contract.** Fix method-to-color/marker mapping once for the paper, choose the
   palette family from the data structure, and decide axis labels, direct labels, legend placement,
   units, and metric-direction arrows.
6. **Export and QA contract.** Export SVG (primary editable text), PDF (LaTeX), and PNG (review);
   open the PNG/PDF page and run the Display Review Gate.

Add a compact design record to `paper/framework-execution-report.md` or the figure plan:

```markdown
| ID | Core conclusion | Panel | Chart | Source | Statistic | Layout | Palette | Label strategy | Export |
|---|---|---|---|---|---|---|---|---|---|
| Fig. 2 | Ours improves accuracy at similar latency. | a | grouped bar | results/main.csv | mean +/- 95% CI over 5 seeds | double-column | hero-baseline | shared legend below, units in axes | SVG/PDF/PNG |
```

## Palette Presets

Choose by data structure, not by personal taste.

| Preset | Use for | Colors / rule |
|---|---|---|
| `peer` | equal-status methods, tasks, datasets | restrained qualitative palette + one marker/hatch per entity; use saturated Okabe-Ito colors only when equal-status separation is more important than journal visual calm |
| `hero-baseline` | one proposed method vs baselines | muted baseline colors + one saturated hero color; hero appears last |
| `semantic-risk-capability` | two opposite metrics such as risk vs capability | deep blue for capability, brick red for risk; do not use grey for either foreground metric |
| `sequential` | ordered magnitude, rank, scale, ablation depth | single-hue ramp, darker = larger or later |
| `diverging` | signed delta, z-score, gain/loss around zero | `RdBu_r` with zero-centered normalization |
| `distribution-neutral` | boxes, violins, densities where shape matters | neutral fill + colored median/mean/focus marker; avoid rainbow groups |
| `composition-muted` | stacked bars, pie, donut | 3-7 muted categorical fills; sort by semantic order or descending share; use short codes when labels are long |
| `shared-legend-radar` | radar comparisons that reuse one method set | muted blue, teal-green, gold, coral, purple, grey with white-filled markers; no filled polygons; coral is the focus/proposed method when one exists |

Global rules: same entity means same `(color, marker)` across all figures; green/red are directional
annotations only; no rainbow/jet; add markers or hatches when color alone would carry identity.

## Chart Type Pattern Library

| Chart family | Use when the conclusion is about | Prefer this design | Avoid / switch when |
|---|---|---|---|
| Vertical bar chart | one metric across <=6 short-named methods/categories | Sort by claim order; use `hero-baseline` for one proposed method; show error bars when repeated runs exist | Long labels or many categories: use horizontal bars or a table |
| Horizontal bar chart | rankings, ablations, long method names, delta contributions | Sort top-to-bottom by value or pipeline order; use single-hue alpha for ordered ablations | Time/scale trends: use a line chart |
| Grouped bar chart | methods x datasets/metrics with shared categories | Use shared legend, thin outlines, restrained related hues plus optional subtle hatches for grayscale; keep groups <=4 series or span full width | Too many groups/metrics: use heatmap or table |
| Stacked bar chart | composition of a total (percent/count parts) | Normalize to 100% only for share comparisons; label total denominator in caption; use `composition-muted` | Comparing exact segment values across many bars: use grouped bars or heatmap |
| Line chart | trend over ordered x: time, steps, scale, data size | Use markers plus color; add confidence band for seeds; direct-label 2-3 lines when stable | Unordered x categories: use bars or dot plot |
| Scatter plot | relationship/tradeoff between two continuous variables | Use semantic quadrants, reference lines, optional bubble size; label only focus/frontier points | Dense overplotting: use hexbin/density or summarize with bins |
| Pareto frontier plot | performance-cost/latency/size tradeoff | Declare direction (`x` lower better, `y` higher better), sort frontier, draw connected frontier, label non-dominated and focus points | No real tradeoff or only one axis varies: use bar/line |
| Radar chart | 3-4 methods over 5-8 capability axes, or up to 6 methods when using the shared-legend radar preset | Per-spoke normalization when ranges differ; light rings; no heavy fills; caption states normalization; use one shared legend for multi-panel radars | >6 methods or >8 spokes: use grouped bars or heatmap |
| Heatmap | matrix values: model x task, hyperparameter grid, confusion matrix | Use `Blues`/`Reds`/`RdBu_r` by metric semantics; white cell gridlines; luminance-aware cell text | Reader must compare exact row values: use table |
| Box plot | distribution summary with median/IQR/outliers | Show median, IQR, whisker rule, optional jittered points for small n | n is tiny (<5 per group): show points or table |
| Violin plot | distribution shape, multimodality, spread | Pair with median/IQR markers; use restrained fills; keep groups <=6 | Exact quartiles matter more than shape: box plot |
| Histogram | one variable's empirical distribution | State bin rule; use step outlines for two-series comparison; align shared bins | Comparing many groups: use density/ECDF or small multiples |
| Density plot | smoothed continuous distribution | State bandwidth/kernel; use transparent lines/fills; show rug/median if useful | n is small or discrete: use histogram/ECDF |
| Pie chart | a single simple whole-part snapshot | Max 5 slices plus Other; label percentages + total n; no 3D/exploded wedges | Any comparison across groups: use stacked bar |
| Donut chart | same as pie, with a stronger label/legend system | Use muted fills, white separators, outside percentage labels, and either a blank center or a compact total/count label | More than 7 categories or any comparison across groups: use stacked bar |

## Named Chart Style Presets

Use these when the Figure Plan names the matching chart form. They are stricter than the generic
chart-family rows above, so later figures in the same paper inherit a consistent visual grammar.

### Preset: shared-legend radar

Use for two related radar panels that compare the same methods across two taxonomies or metric
families. The intended visual grammar is a wide, clean, review-ready radar comparison:

- Use **two polar panels** side by side with bold panel titles such as `(a) ASR by Attack Vector`
  and `(b) ASR by Harm Category`.
- Use one method-to-color and method-to-marker mapping across both panels; lines may mix solid and
  dashed styles when six methods need separation.
- Use the local shared-legend radar palette by default: muted blue, teal-green, gold, coral, purple,
  and neutral grey (`#5E9BC9`, `#59AE8B`, `#E0AF45`, `#CF7968`, `#8E78BE`, `#9A9A9A`). Reserve the
  coral line for the focus/proposed method when one exists.
- Use **no filled polygons**. Keep only colored traces, white-edged markers, light grey rings, and
  light grey spokes so overlapping methods remain legible.
- Use a common radial scale when all spokes are the same unit (for example 0--100 ASR). If spokes
  have different units, normalize per spoke and state that in the caption.
- Put **one shared legend below the figure**, not one legend per panel. The legend should carry the
  full method names; panel spokes may use compact axis labels with line breaks.

### Preset: compact labeled donut

Use for one composition snapshot with 5--7 semantically important categories, especially benchmark
coverage or taxonomy coverage where a bar chart would overstate ranking.

- Use a **thick ring** with a blank center unless a compact `n=...` center label is needed.
- Use muted categorical fills with **white separators** between wedges.
- Place **outside code-percentage labels** such as `H2 (31.0%)` around the ring, connected by thin
  grey leader lines; keep the long category names out of the wedges.
- Put a **bottom legend maps codes to full labels** in two or three columns.
- State the denominator or total count in the caption or nearby text; do not rely on percentages
  alone.

**Body compact mode.** When the donut is a supporting main-text coverage figure rather than the
central evidence figure, size it as a quiet inset-style display: include it at
`0.45--0.60\linewidth` in a one-column paper/single-column journal, or about
`0.58--0.72\textwidth` when it is one panel inside a two-column-width multi-panel figure. Keep the
canvas around 2.0--2.4 in tall and **omit the bottom legend** when full code definitions live in the caption, appendix, or nearby table.
Keep only short code-percentage labels around the rings; long labels belong outside the main graphic.

## Extended Patterns From `type.md`

| Pattern | Use / rule |
|---|---|
| Error-bar plot | Use for mean +/- std/sem/CI when the interval is the message; define interval in caption. |
| Line with confidence band | Use for multi-seed training or scaling curves; alpha 0.10-0.20 and one marker per series. |
| ROC / PR curve | Use only for thresholded classifiers/retrieval; include AUC/AP and class balance. |
| Calibration / reliability diagram | Use when confidence quality is the claim; include bin counts or show sparse bins. |
| Confusion matrix | Treat as a heatmap; normalize by row/column only after stating the denominator. |
| Ablation / delta plot | Prefer horizontal bars sorted by pipeline order or absolute delta; zero line must be visible. |
| Ranking / leaderboard plot | Horizontal bar or dot plot with consistent method order and metric direction. |
| Slope chart | Use for before/after or two-setting comparisons; direct-label endpoints, avoid legends. |
| CDF / ECDF | Use for sample-level error/success distribution; show reference thresholds and report n. |

## Label And Annotation Strategy

- Put the message in the caption, not as a plot title.
- Axis labels must include readable names, units, and direction when relevant (`Accuracy (%) up`,
  `Latency (ms) down`).
- Use horizontal bars for labels that would require >30 degree x-tick rotation.
- Annotate only values that matter to the conclusion: focus method, frontier points, thresholds,
  selected/default setting, or best/worst rows. Too many value labels become texture.
- Legends are frameless. For multi-panel figures, use one shared legend or a legend-only panel.
- For pies/donuts/stacked bars, always state total `n` or denominator; shares without denominators
  are weak evidence.
- If uncertainty is shown, the caption or source-data note must define what the interval means.

## Layout And Size Notes

Use the venue sizing reference for exact dimensions. As a rule:

- low-density single plots: single-column, usually `0.45--0.65\linewidth` in one-column templates;
- standard line/scatter/distribution/Pareto plots: usually `0.60--0.78\linewidth` in one-column
  templates unless labels or legends prove they need more room;
- grouped bars, heatmaps, radars, and multi-panel evidence: double-column in two-column venues; in
  one-column templates, use `0.65--0.80\linewidth` for moderate-density cases and
  `0.90--1.00\linewidth` only for dense or central evidence;
- when a radar or small heatmap is promoted to a two-column `figure*`, use a centered
  `0.65--0.78\textwidth` inclusion for moderate-density single-panel evidence instead of filling
  the full span by default;
- pie/donut and other composition snapshots: never allocate a full-width main figure unless the
  composition is the paper's central evidence; for a supporting body pie, start around
  `0.32--0.45\linewidth` in one-column templates or `0.45--0.58\columnwidth` in two-column
  templates, then inspect the rendered page;
- combine related small charts into one multi-panel figure with shared encodings instead of emitting
  many disconnected floats.

## Failure Signatures To Check

In addition to the Display Review Gate:

- bar/grouped/stacked: labels or error bars clipped; bars too thin; segments unlabeled or denominator
  missing;
- line: crossing series distinguished only by color; uncertainty band hides the trend;
- scatter/Pareto: wrong dominance direction; too many point labels; frontier line drawn through
  dominated points;
- heatmap: unreadable cell text; rotated labels; color scale not tied to metric semantics;
- distribution: box/violin/hist/density used without n or spread definition;
- pie/donut: too many slices, no total n, or used where comparison across groups is required.
