# Plot Style

Use this reference when the confirmed Figure Plan contains data-driven plots,
metric visualizations, ablations, scaling curves, heatmaps, or generated
tables.

## Backend Gate

Python (matplotlib/seaborn) is the default plotting backend. If the user prefers
R (ggplot2/patchwork), they must explicitly request it before any plot is
generated. Once a backend is selected, use it exclusively for all plotting,
previewing, and exporting. Do not cross-render with the other language. If the
selected backend's runtime or packages are missing, stop and report the blocker
before rendering.

## Backend Default

Python is the default plotting backend. Use matplotlib, and seaborn only when it
reduces plot complexity. Use R only when the user explicitly requests R or the
workspace already provides an R plotting pipeline.

Do not hardcode results from memory. Every chart must read from a concrete
workspace result file or table recorded in the Figure Plan.

## Output Layout

For Full Draft projects, keep generated chart assets minimal by default:

```text
paper/figures/
  <figure-id>.pdf
  <figure-id>.png
  latex_includes.tex
```

Do not create shared style modules, scripts, derived data folders, or audit files
by default. Create extra reproducibility packaging only when the user requests it
or when a complex result figure cannot be regenerated otherwise.
The canonical chart output path is `paper/figures/<figure-id>.pdf`, with
`paper/figures/<figure-id>.png` as the preview or raster fallback.

## Python Style Contract

Use a restrained publication style:

```python
import matplotlib as mpl

mpl.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Times New Roman", "Times", "DejaVu Serif"],
    "font.size": 9,
    "axes.labelsize": 9,
    "xtick.labelsize": 8,
    "ytick.labelsize": 8,
    "legend.fontsize": 8,
    "figure.dpi": 300,
    "savefig.dpi": 300,
    "savefig.bbox": "tight",
    "savefig.pad_inches": 0.03,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "pdf.fonttype": 42,
    "svg.fonttype": "none",
})

COLORBLIND = [
    "#0072B2", "#E69F00", "#009E73", "#D55E00",
    "#56B4E9", "#CC79A7", "#999999", "#000000",
]
```

Rules:

- Prefer PDF for LaTeX inclusion; add PNG only as a preview or fallback.
- Use SVG only when the target venue or editing workflow needs it.
- Avoid in-figure titles; put the message in the caption.
- Axis labels must be readable labels, not raw variable names.
- Add units and metric direction when relevant.
- Use colorblind-safe palettes and avoid red/green as the only encoding.
- Use one visual message per plot.
- If fewer than three data points are present, consider a table or text instead.

## Chart Contract

Each chart generation pass must:

1. read input data from the source path recorded in the Figure Plan,
2. normalize labels and metric direction explicitly,
3. write output files under `paper/figures/`,
4. fail loudly if expected columns or metrics are missing,
5. avoid network calls and experiment execution unless the user explicitly asks,
6. insert the chart into the LaTeX section selected by the Paper Framework.

## Table Contract

For result tables, prefer LaTeX `booktabs` style. Record metric direction,
consistent precision, and grouping logic. Do not convert a table into a plot
unless the visual comparison adds real value.
