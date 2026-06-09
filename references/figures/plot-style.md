# Plot Style

Use this reference when the confirmed Figure Plan contains data-driven plots,
metric visualizations, ablations, scaling curves, heatmaps, or generated
tables.

## Backend Gate

Python is the default plotting backend. Python (matplotlib/seaborn) is the default plotting backend. If the user prefers
R (ggplot2/patchwork), they must explicitly request it before any plot is
generated. Once a backend is selected, use it exclusively for all plotting,
previewing, and exporting. Do not cross-render with the other language. If the
selected backend's runtime or packages are missing, stop and report the blocker
before rendering.

Do not hardcode results from memory. Every chart must read from a concrete
workspace result file or table recorded in the Figure Plan.

## Output Format

**SVG is the primary output.** SVG preserves editable text (when `svg.fonttype='none'`),
supports lossless scaling, and allows post-hoc text adjustment in vector editors
(Illustrator, Inkscape). PDF is the LaTeX inclusion format. PNG is the raster preview.

```text
paper/figures/
  <figure-id>.svg       # primary — editable vector, text as <text> nodes
  <figure-id>.pdf       # LaTeX inclusion
  <figure-id>.png       # raster preview, dpi=300
```

Save order:
```python
fig.savefig('figures/name.svg', bbox_inches='tight')
fig.savefig('figures/name.pdf', bbox_inches='tight')
fig.savefig('figures/name.png', dpi=300, bbox_inches='tight')
plt.close(fig)  # always close to free memory
```

DPI guide (PNG only): 300 standard, 600 for dense bar panels with many methods.

Do not create shared style modules, scripts directories, derived data folders, or
audit files by default. Create extra reproducibility packaging only when the user
requests it or when a complex result figure cannot be regenerated otherwise.

## Python Style Contract

**Apply these rcParams before any figure drawing. This is mandatory, not optional.**
Failure to apply them produces figures with wrong fonts, low resolution, and
unreadable text.

```python
import matplotlib as mpl

mpl.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans", "sans-serif"],
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
    "svg.fonttype": "none",       # keeps text as editable <text> nodes
})
```

### Figure Sizes

Match figure width to the target column layout. These are starting points;
adjust for the specific figure's aspect ratio and content density.

| Layout | `figsize` (width, height) | Notes |
|--------|--------------------------|-------|
| Single-column (ACL, EMNLP, NAACL) | `(3.25, 2.2)` to `(3.5, 2.8)` | Narrow; avoid more than 4-5 bars side by side |
| Double-column / full-page width | `(6.5, 3.5)` to `(7, 5)` | Wide enough for grouped bars, heatmaps, radar |
| Square (radar, scatter matrix) | `(5, 5)` to `(6, 6)` | Keep legend inside or directly below the axes |

Use `\includegraphics[width=\columnwidth]` or `\linewidth` in LaTeX; do not
scale figures with absolute `\textwidth` that ignores column layout.

### Font Size Hierarchy

Choose the base `font.size` according to figure type and panel count. Start from
the table below; adjust per-figure for readability at target column width.

| Figure type | Base `font.size` | Axis label | Tick label | In-bar / cell annotation |
|---|---|---|---|---|
| Dense multi-panel (3+ panels, journal-width) | 7–8 | 8 | 7 | 7–8 |
| Standard single-panel (bar, line, scatter) | 9–10 | 9–10 | 8–9 | 8–9 |
| Hero / teaser figure (full page width) | 11–12 | 11–12 | 10 | 10–11 |
| Heatmap with cell text | 8–9 | 9 | 8 | 7–8 (contrast-adaptive) |
| Radar / polar (6+ spokes) | 9 | 9 | 8 | — |

All sizes assume the figure will be placed at `\columnwidth` or `\textwidth` in a
two-column CS conference layout. Adjust upward for single-column venues with wider
text blocks.

**Minimum legibility rule**: No text element may render below 6pt at final column
width. Labels below 7pt should be rare and only for secondary information (tick
labels, legend entries for 5+ methods).

### No Content Outside Figure Bounds

**All content — labels, legends, annotations, titles — must stay within the
figure canvas.** Check these before saving:

- Legend: prefer `loc='upper right'` or `loc='best'` inside axes, or
  `bbox_to_anchor=(0.5, -0.12), loc='upper center'` below the axes.
  **Never** anchor a legend outside the figure at coordinates like 1.35.
- Labels: all bar/point annotations must fit within `set_ylim` with headroom.
- `tight_layout(pad=...)` before every `savefig` is mandatory.

### Colors

Color is an **encoding**, not decoration. Three mistakes make generated figures look
amateur (all banned by journal figure practice — no rainbow/jet colormaps; hue must not be
the *only* encoding; grayscale print must stay readable):

1. **Shipping the library default cycle.** matplotlib's `tab10` / seaborn's default
   (saturated mid orange `#ff7f0e` + mid blue `#1f77b4`, etc.) is the single most common
   "this looks like a generated/Excel chart" tell. **Never rely on the default color cycle —
   set an explicit palette before plotting every figure.** A two-series chart in raw
   `tab:orange`/`tab:blue` is a defect even though it is "only two colors."
2. a **rainbow of maximally-distinct, saturated hues** with no hierarchy (the "Excel"
   look) — caused by hand-mixing colors of unequal luminance, and
3. using **hue as the only channel**, which collapses in grayscale print and for
   colorblind readers.

Publication palettes are **deep and slightly muted, not neon**. When a color looks
vivid/saturated on screen, desaturate or deepen it — saturated primaries are what make a
figure read as amateur. **Reduce saturation before adding categories.**

Pick color in three steps: choose the palette family **from the data structure**, add a
**redundant channel**, then **verify**.

#### Step 0 — one palette for the whole paper (define once, reuse everywhere)

Every figure in the paper should read as **one visual system**, not a set of unrelated
charts. Before generating the first plot, fix a single palette and reuse it across the bar
chart, line plot, radar, and heatmap accents. **Family consistency beats maximal hue
separation:** keep baselines in one cool family and the proposed method in one hero family.

- **One entity → one (color, marker) pair across *every* figure.** If "Gemini3-Pro" is the
  deep-blue series in Figure 3, it is deep blue everywhere it appears — never remapped.
- Group related entities into **families** and color by family (e.g. all "Frontier LLM"
  baselines in cool blues, all "Specialist agent" baselines in warm neutrals), rather than
  giving N equal entities N unrelated hues.
- Reserve green/red for *direction* (gain/drop/threshold), never for entity identity.
- If two figures legitimately need different palettes (different entity sets), still keep
  the same saturation level and neutral family so they look related.

#### Step 1 — choose the palette family from the DATA (not the paper, not the chart)

| Data structure | Examples | Palette family |
|---|---|---|
| **Categorical / nominal** — distinct entities of equal status | methods, models, datasets, tasks, conditions | **Qualitative** (`PEER_PALETTE`) |
| **Ordered / sequential** — one quantity that increases | ablation depth, model scale, dose, rank, magnitude | **Single-hue sequential ramp** |
| **Diverging** — signed values around a reference | z-score, gain/loss vs baseline, correlation | **Diverging colormap** (`RdBu_r`) |
| **Emphasis** — one focus entity vs the rest | "our method" vs baselines | **Hero-baseline** (1 saturated + muted family) |

Two hard mismatches to avoid:
- **Never use a sequential ramp for unordered categories** — adjacent shades become
  indistinguishable and it implies an order that does not exist. (A peer comparison of
  N equal methods is categorical, so it takes the qualitative palette, *not* a ramp.)
- **Never use a qualitative palette for an ordered magnitude** — it throws away the
  ordering the reader needs.

#### Categorical → Qualitative palette (default for equal peers)

Use the Okabe–Ito set: it is colorblind-safe by construction and **luminance-balanced**,
so no series jumps out — which is exactly what "equal peers" requires:

```python
PEER_PALETTE = [
    "#0072B2",   # blue
    "#D55E00",   # vermillion
    "#009E73",   # bluish green
    "#CC79A7",   # reddish purple
    "#E69F00",   # orange
    "#56B4E9",   # sky blue
    "#000000",   # black      (use only as a 7th category)
    "#F0E442",   # yellow     (weak on white; last resort / accent)
]
PEER_MARKERS = ['o', 's', '^', 'D', 'v', 'P', 'X', '*']  # pair 1:1 with colors
```

- Balanced luminance → equal visual weight (the point of a peer comparison).
- Cap at **6–8 categories**. Beyond that, group/aggregate or use small multiples; do not
  keep adding hues. **Reduce saturation before adding categories.**
- For a **2–3 series** comparison where every series matters (e.g. two metrics like
  ASR vs. TCR across models), pick from the **nature-figure palette** so the colors stay
  consistent across the paper — `#0F4D92` deep blue paired with `#B64342` brick red
  (default), or `#42949E` teal, or `#8BCF8B` soft green. Do **not** ship the matplotlib
  default orange/blue (`#1f77b4`/`#ff7f0e`) and do **not** hand-mix off-palette hues like a
  brown/clay — those read muddy. When the two series have opposite valence (e.g. ASR =
  risk/bad, TCR = capability), put the warmer/red hue on the "risk" series. Do not paint one
  series grey; keep the legend frameless (`frameon=False`).

#### Ordered → Single-hue sequential ramp

```python
import numpy as np
sequential = plt.cm.Blues(np.linspace(0.35, 0.95, n))  # low → high, darker = larger
```

Use for ablation depth, scaling, rank, or any single increasing quantity, and for
magnitude heatmaps (`Blues`; use `Reds` only when the metric is semantically
"worse/danger/error"). Never apply a ramp to unordered method identity.

#### Diverging → signed around a reference

```python
import matplotlib as mpl
cmap = plt.cm.RdBu_r
norm = mpl.colors.TwoSlopeNorm(vcenter=0)  # red = above, blue = below
```

Use for z-scores, gain/loss vs a baseline, or correlation — anything with a meaningful
zero/center.

#### Emphasis → Hero-baseline (one focus entity)

When the paper proposes a method, make the hero the **only saturated color**; baselines are
**pale and recede**. This is the pattern published Nature/NMI comparison bars use: a row of
soft, low-saturation baselines and one deep hero, with the **hero placed last** so the eye
lands on it. Misapplying this to a peer comparison of equal methods invents a hierarchy that
is not there.

```python
HERO_BLUE = "#3775BA"   # proposed method — the one advancing color (deepen to #0F4D92 for more pop)
BASELINE_PALETTE = [     # all baselines — low-saturation receding colors
    "#CFCECE",   # grey
    "#DDF3DE",   # pale green
    "#FBDFE2",   # pale pink
    "#D9B9D4",   # soft lavender
    "#DAA87C",   # warm tan
    "#B4C0E4",   # soft blue-purple
]
# usage: colors = BASELINE_PALETTE[:n_baselines] + [HERO_BLUE]  # hero last
```

This is the right fix whenever a "many methods, one metric" bar chart would otherwise become
a row of equally-saturated hues: keep the baselines pale and let one color carry the message.

#### Step 2 — add a redundant channel (mandatory when ≥4 overlapping series, or whenever grayscale/CVD matters)

Color alone fails where lines cross, in grayscale print, and for colorblind readers.
Pair each entity with a second, non-color channel so identity survives all three:

- **Lines / scatter / radar**: a fixed `marker` per entity (`PEER_MARKERS`), and a
  `linestyle` cycle if still crowded. Build legend handles with both line + marker.
- **Bars / filled areas**: a `hatch` per entity when neighboring fills are close in
  luminance or may print in grayscale.

```python
HATCHES = ['/', '\\\\', '.', 'x', 'o', '+', '*', 'O']
```

#### Step 3 — verify (folds into the Display Review Gate "low contrast" check)

- **Grayscale**: render or imagine a desaturated copy; every series must still be
  distinguishable (this is why Step 2 exists).
- **Colorblind**: `PEER_PALETTE` (Okabe–Ito) is CVD-safe by construction. For any
  hand-picked colors, sanity-check a deuteranopia simulation.

#### Support colors

```python
DELTA_UP   = "#2E9E44"   # gains / improvement — arrows and directional labels ONLY
DELTA_DOWN = "#E53935"   # drops / degradation — arrows and directional labels ONLY
NEUTRAL_DARK  = "#4D4D4D"
NEUTRAL_MID   = "#767676"
NEUTRAL_LIGHT = "#D8D8D8"
```

#### Rules (all families)

- One entity = one **(color, marker)** pair across every figure in the paper. Never remap.
- **Grey is neutral/receding only** — never the color of a primary metric or a foreground
  series the reader must compare. Reserve grey for backgrounds, reference lines, "other"
  buckets, and de-emphasized baselines.
- Green/red (`DELTA_UP`/`DELTA_DOWN`) are reserved for direction (arrows, gain/drop), not
  entity identity.
- No rainbow/jet colormaps anywhere.
- Avoid in-figure titles; put the message in the caption.
- Axis labels must be readable labels, not raw variable names.
- One visual message per plot.
- If fewer than three data points, consider a table or text instead.

### Bar Chart Rules

These rules are mandatory for every bar chart (comparison, ablation, grouped).

**Edge and separation** — every bar must have a visible outline:
```python
ax.bar(..., edgecolor='black', linewidth=1.0)
```

**Error bars** — make them visible at print scale:
```python
error_kw = {'elinewidth': 1.5, 'capthick': 1.5, 'capsize': 4}
```

**In-bar value annotation** — luminance-aware text color for readability:
```python
def _luminance(hex_color):
    c = hex_color.lstrip('#')
    r, g, b = int(c[0:2], 16), int(c[2:4], 16), int(c[4:6], 16)
    return 0.299*r + 0.587*g + 0.114*b

for bar, color in zip(bars, bar_colors):
    val = bar.get_height()
    text_color = 'white' if _luminance(color) < 128 else 'black'
    ax.text(bar.get_x() + bar.get_width()/2, val + offset,
            f'{val:.1f}', ha='center', va='bottom',
            fontsize=8, color=text_color)
```

**Dynamic y-axis** — tighten to data range, but the limits must be computed from
the **error-bar extremes, not the bar heights**. Computing `ylim` from `vals` alone
clips the whisker tips and caps — the single most common bar-chart defect. Always
include the error reach on both ends, plus headroom for value labels:
```python
# vals: bar heights; lo_err/hi_err: lengths of the lower/upper error bars
top = (vals + hi_err)            # highest whisker tip
bot = (vals - lo_err)            # lowest whisker tip
span = top.max() - bot.min()
margin = span * 0.15
label_pad = span * 0.10          # extra room above for value labels
ax.set_ylim(max(0, bot.min() - margin),
            top.max() + margin + label_pad)
```
If there are no error bars, set `hi_err = lo_err = 0`. Never set the upper limit
from `vals.max()` when error bars or in-bar labels extend above it.

**Horizontal bars for ablation** — use alpha-graduated single color:
```python
base_rgb = (0.215, 0.459, 0.729)  # hero blue
alphas = np.linspace(0.2, 1.0, n_ablations)
colors = [(*base_rgb, a) for a in alphas]
ax.barh(..., color=colors)
```

**Print-safe hatching** for grayscale readability:
```python
hatches = ['/', '\\\\', '.', 'x', 'o']
for bar, hatch in zip(bars, hatches):
    bar.set_hatch(hatch)
```

- No grid lines on bar charts.
- No title inside the figure.
- X-ticks may be hidden when the legend names the methods: `ax.set_xticks([])`.

### Line / Trend Plot Rules

- Line width: 1.5–2.5 pt.
- Marker size: 5–8 pt. Use a **distinct marker per series** (`PEER_MARKERS`) as a redundant
  channel, not the same circle for every line.
- `fill_between` uncertainty bands: alpha 0.1–0.2.
- Reference baseline as dashed horizontal line:
  `ax.axhline(y=..., linestyle='--', color='#767676', alpha=0.5, linewidth=1)`.
- No grid; sparse y-ticks guide the eye.
- Place one shared legend above a multi-panel row rather than repeating per axis.
- Fading alpha for temporal progression: higher alpha for later time segments.

### Heatmap Rules

For publication heatmaps, prefer `ax.pcolormesh` with white gridlines — this is
the nature-journal standard. It gives clean cell separation and high readability.

**Mandatory rules:**
- White gridlines between every cell: `edgecolors='white', linewidths=1`.
- Default colormap: `Blues` for general percentage/score data (cleanest, most common
  in CS papers). Use `Reds` only when the metric is semantically "danger/error/worse."
  Use `RdBu_r` for diverging data (positive/negative z-scores).
- Horizontal labels: `rotation=0`. Never rotate heatmap x-tick labels.
- Figure size: at least 6–10 inches wide for 6+ columns, proportional to cell count.
- Base font.size: 10–12 for readability.
- Annotations: integers with `fmt='d'` or one decimal with `fmt='.1f'`.

```python
import matplotlib.pyplot as plt
import numpy as np

# ── publication heatmap with clean cell separation ──
fig, ax = plt.subplots(figsize=(8, 5))
im = ax.pcolormesh(data, cmap='Reds', edgecolors='white',
                   linewidths=1, vmin=0, vmax=100)
ax.invert_yaxis()  # match imshow row order

# Cell annotations — luminance-aware (decide text color from the *rendered cell
# color*, not from a hardcoded value threshold). A fixed threshold like `val > 55`
# breaks whenever vmin/vmax or the colormap change; luminance always tracks the cell.
cmap = plt.cm.Reds
norm = mpl.colors.Normalize(vmin=0, vmax=100)
for i in range(n_rows):
    for j in range(n_cols):
        val = data[i, j]
        r, g, b, _ = cmap(norm(val))
        lum = 0.299*r + 0.587*g + 0.114*b
        ax.text(j + 0.5, i + 0.5, f'{val:.0f}',
                ha='center', va='center', fontsize=10,
                color='white' if lum < 0.5 else 'black',
                fontweight='bold')

# Clean ticks centered on cells
ax.set_xticks(np.arange(n_cols) + 0.5)
ax.set_xticklabels(col_labels, rotation=0, fontsize=10)
ax.set_yticks(np.arange(n_rows) + 0.5)
ax.set_yticklabels(row_labels, rotation=0, fontsize=10)

# Colorbar
cbar = plt.colorbar(im, ax=ax, shrink=0.85, pad=0.02)
cbar.set_label('Value (%)', fontsize=10)

fig.tight_layout(pad=1.5)
```

**Do not:**
- Use `imshow` without white gridlines — cells blend together.
- Rotate x-tick labels.
- Use tiny font sizes (< 8pt) for cell annotations.
- Use `magma` or `YlOrRd` for simple percentage/count data — they add visual
  noise without adding information.

### Radar / Polar Chart Rules

Radar charts fail in two specific ways that make most of them ugly. Avoid both:

1. **Too many overlaid traces.** **At most 4 methods on one radar.** Beyond 4, filled
   areas overlap into a muddy blob — split into small multiples (one radar per method,
   or 2–3 per panel). Hard ceiling 6; past 6 a single radar is unreadable.
2. **No per-spoke normalization.** When every method scores in a narrow band (e.g.
   20–60%) on a 0–100 radial axis, the data collapses near the center. **Normalize each
   spoke independently to a display band** (e.g. 20–95) so the differences spread out.
   State the per-spoke scaling in the caption since raw ring values no longer read
   directly. Use a shared scale only when methods genuinely span the full range with ≤4
   traces.

Styling:

- Start from top: `ax.set_theta_zero_location('N')`; clockwise: `ax.set_theta_direction(-1)`.
- Fill alpha: ≤0.06 (and drop fills entirely once 4 traces overlap); trace linewidth 1.5–2.0.
- Give each method a **distinct marker** (`PEER_MARKERS`), not just a distinct color, so
  overlapping traces stay separable at crossings, in grayscale, and for colorblind readers.
  Show the marker in the legend handles.
- **No heavy black outer circle.** Draw light grey contour rings (`#CFCECE`, lw 0.6) and
  light spokes (lw 0.5); remove the default polar grid and all spines.
- Offset spoke labels just beyond the outer ring so they never overlap data, rings, or
  radial tick text. Do not leave the default `20%–100%` radial ticks sitting on top of a
  data spoke.
- Limit to 5–8 spokes; beyond 8, switch to grouped bars.
- Legend below the polar axes: `bbox_to_anchor=(0.5, -0.08), ncol=min(4, n_methods)`.

Use the `radar_chart()` helper in `chart-patterns.md`, which enforces the per-spoke
normalization, the trace cap, light rings, and label offset by default.

### Legend Rules

- **No frame**: `ax.legend(frameon=False)` — always.
- **Inside axes preferred**: `loc='upper right'` or `loc='best'` when data area
  has clear empty space.
- **Below axes**: `bbox_to_anchor=(0.5, -0.12), loc='upper center', ncol=N` when
  4+ entries exist.
- **Dedicated legend panel**: for multi-axis figures (3+ metrics side by side),
  make the last subplot legend-only with `ax.set_axis_off()`.
- **Direct labels**: when only 2–3 lines/bars with stable identities, label them
  directly with text annotations rather than a detached legend.
- Never anchor a legend outside the figure canvas at coordinates beyond ~1.2.

### Multi-Panel Information Architecture

Every panel must answer a unique question. Covering one panel must leave a gap
that cannot be recovered from the others.

**Three-level progression** (recommended when a figure has 3+ panels):

| Level | Question | Typical encoding |
|---|---|---|
| Overview | What is the landscape? | Bar, stacked bar, composition |
| Deviation | What is distinctive? | Heatmap (z-score), ranked delta |
| Relationship | How do variables co-vary? | Scatter, bubble |

**Anti-redundancy** — before finalizing, check that no two panels display the
same data in different visual forms:

| Trap | Fix |
|---|---|
| Stacked bar (%) + heatmap of same % | Replace heatmap with z-score deviation |
| Two ranked bars on related metrics | Replace one with scatter / bubble |
| Same data as bar and table | Keep only the more informative one |

**Panel labels**: use bold lowercase letters (a, b, c) near the top-left of each
panel, positioned with `transform=ax.transAxes`:
```python
ax.text(-0.06, 1.02, 'a', transform=ax.transAxes, fontsize=12,
        fontweight='bold', va='bottom', ha='left')
```

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
consistent precision, grouping logic, and the target layout width. Do not
convert a table into a plot unless the visual comparison adds real value.

### LaTeX Table Toolbox

When a generated paper contains tables beyond a tiny 2-3 column numeric table,
ensure the LaTeX preamble includes:

```tex
\usepackage{array}
\usepackage{tabularx}
\newcolumntype{Y}{>{\raggedright\arraybackslash}X}
\newcolumntype{Z}{>{\centering\arraybackslash}X}
```

Use `tabularx` for long labels, prose columns, or mixed numeric/text tables:

```tex
\begin{tabularx}{\linewidth}{@{}lccY@{}}
```

For double-column tables, use `table*` and `\textwidth`:

```tex
\begin{table*}[t]
\centering
\small
\begin{tabularx}{\textwidth}{@{}lccccY@{}}
...
\end{tabularx}
\end{table*}
```

Do not place a prose-heavy table in plain `tabular` with only `l`, `c`, or `r`
columns. LaTeX will not wrap those cells, and the table can cross margins or
neighboring columns without a useful compile error.

Use `\resizebox{\linewidth}{!}{...}` only for numeric tables with short cell
contents after confirming the scaled text remains readable. Prefer splitting a
table, using `table*`, or moving complete matrices to supplementary material
over shrinking prose-heavy tables.
