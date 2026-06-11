# Figure QA Contract

Use this reference before final delivery, before a revision round, and whenever
a figure contains quantitative comparisons, statistical claims, microscopy/images,
or AI-generated illustrations. It applies to both data-driven plots and concept
pictures.

This file is the **submission-readiness checklist** — the final gate after every
figure has passed the per-figure Display Review Gate (render → look → score →
regenerate) in `figure-planning.md`.

## Pre-Submission Checklist

| Check | Pass condition |
|---|---|
| Core conclusion | Every figure has a one-sentence claim; every panel maps to it |
| Evidence chain | Every panel traces to a concrete workspace result file or confirmed paper fact |
| Display type | Figure is classified (quantitative comparison / pipeline-architecture / teaser-composite / qualitative-grid / latex-table) and the generation route matches |
| Layout target | Single-column / double-column is declared and matches the venue template |
| Height budget | No figure exceeds its role's height budget; banners ~4.5–6 cm at `\textwidth`; no empty top/bottom bands |
| No margin overflow | Zero `Overfull \hbox` for figures in `main.log`; `audit_draft.py` passes |
| Text size readable | All text ≥6pt at final column width; see `plot-style.md` font hierarchy |
| Panel labels | Bold lowercase (a, b, c), positioned near top-left, consistent across figures |
| Unified visual family | Same method → same (color, marker) across all figures; same font family and size hierarchy |
| No default matplotlib cycle | Every figure sets an explicit palette before plotting first data |
| Colors: grayscale-safe | Every series distinguishable when desaturated; redundant channel (marker/hatch) present for ≥4 series |
| Colors: colorblind-safe | Palette is Okabe–Ito or a verified CVD-safe alternative; no rainbow/jet colormaps |
| Colors: green/red reserved | Green/red used only for directional markers (gain/drop), never entity identity |
| Legend | `frameon=False`; inside axes or below; dedicated panel for multi-axis figures; never anchored outside figure |
| Statistics | n, center, spread, test, correction documented (see Statistics Minimum below) |
| Source data | Every quantitative panel traces to a concrete CSV/TSV/JSON or script output |
| Export bundle | SVG (primary, editable text), PDF (LaTeX inclusion), PNG (raster preview ≥300 DPI) all present |
| AI-generated text verified | Every in-image label read and confirmed correct against Writing Policy terminology; no misspelling, no invented labels |
| AI-generated picture reviewed | No leaked prompt scaffolding; illustrative (not boxy flowchart); no invented claims/modules/datasets |
| Non-empty output | Every output file is non-empty and at the recorded path |

## Statistics Minimum

For each quantitative panel, the figure caption or accompanying source-data note
must document:

```text
n definition:
biological / experimental replicates:
technical replicates (if distinct):
center statistic:           mean / median / other
spread / interval:          std / sem / CI / IQR / range
test:                       t-test / Mann-Whitney / ANOVA / ...
multiple-comparison correction:  Bonferroni / FDR / none
p-value display:            exact p / threshold marker (*/**/***) / n.s.
source-data file:
```

For machine-learning / model evaluation figures, also capture:

```text
train / validation / test split:
number of seeds or folds:
metric definition:           formula or reference
confidence interval definition:  bootstrap / across-seeds / ...
baseline definition:         which model/config is the reference
```

## Image-Integrity Minimum

For each image panel (microscopy, screenshots, qualitative grids):

```text
raw file:
processed file:
crop:                        full frame / selected region
brightness / contrast / gamma adjustment:  none / global / local
pseudo-color:                none / LUT applied (name)
scale calibration:           scale bar present + calibrated
stitching:                   single field / stitched (N tiles)
reuse in other figures:      none / also appears in Fig. X
quantification link:         which quantitative panel uses this image
```

Global adjustments (applied to the whole image) are safer than local selective
edits. If an adjustment changes the visibility of relevant background, bands,
or features, flag it rather than silently normalizing.

## Display Review Gate (inline quick-check)

The per-figure review gate lives in `figure-planning.md` (Display Review Gate
section). It is an executable loop: **render → look at PNG → score against
failure signatures → regenerate until clean**. The failure signatures are the
operational tool for catching the four most common data-plot defects and the
five most common AI-generated-picture defects. Run that gate on every figure
before running this checklist.

## Export Checks

```python
# Verify editable SVG text
import matplotlib as mpl
assert mpl.rcParams["svg.fonttype"] == "none", "SVG text will be paths, not editable"
assert mpl.rcParams["pdf.fonttype"] == 42,    "PDF text may not be selectable"

# Open the SVG in a text editor and confirm <text> elements exist (not only <path>).
# Then render and visually inspect the PNG at 100% zoom.
```

## Cross-Reference

- `plot-style.md` — rcParams, colors, per-chart-type rules, legend rules, multi-panel architecture
- `chart-patterns.md` — reusable Python plotting helpers
- `figure-planning.md` — Display Review Gate with failure signatures, generation routes
- `picture-generation.md` — AI-generated picture workflow, label verification, overlay fallback
- `conference/figure-sizing.md` — conference column widths, figsize, font hierarchy, height budget, QA notes
- `journal/figure-sizing.md` — journal column widths, figsize, font hierarchy, display-item caps, QA notes
- `journal/figure-contract.md` — journal figure archetypes, panel logic, aesthetic integration, reviewer-risk
- `table-design.md` — analogous QA Gate for LaTeX tables
- `references/sections/figures-and-tables.md` — section-level insertion rules and width contract
