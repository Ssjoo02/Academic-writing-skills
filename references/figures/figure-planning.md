# Figure Planning

Use this reference only when a Paper Framework, full draft, or revision needs figures or tables.
Do not load it for purely textual Writing Policy work unless the user explicitly asks about figures.

## Purpose

Figure and table planning decides four things:

1. what visual asset the paper needs,
2. where it should be inserted,
3. which layout width it targets,
4. how it should be generated or sourced.

It does not decide the paper's core claims. Claims and evidence come from the Writing Policy.

## Display Item Contract

A publication-quality academic figure or table is a visual argument, not decoration. Before filling
the Figure Plan routing table, establish the contract below for each planned display item. This
applies to data plots, architecture diagrams, pipeline figures, teaser pictures, qualitative grids,
and LaTeX tables.

### The Five-Point Display Contract

Before assigning a generation route or writing code, establish:

1. **Core conclusion**: the one-sentence claim this figure must defend. Every panel, label, and
   visual choice must serve this conclusion. If a planned panel does not carry a unique piece of
   evidence for the conclusion, drop it or merge it.

2. **Evidence chain**: map each planned panel/subfigure to a specific piece of evidence from the
   Writing Policy. A panel without a mapped claim or evidence source is decoration and should be
   removed. The chain must trace back to concrete workspace result files or confirmed paper facts.

3. **Display type**: classify the item into one of:
   - `quantitative comparison`: bar, line, scatter, heatmap, or table driven by result data,
   - `pipeline-architecture`: ordered stages, system components, or workflow with node-edge
     relationships,
   - `teaser-composite`: overview illustration combining problem, method, and evidence visually,
   - `qualitative-grid`: example cases, screenshots, or image panels showing representative outputs,
   - `latex-table`: taxonomy, result matrix, qualitative examples, or benchmark statistics rendered
     directly in LaTeX.
   The display type determines the generation route, not the other way around.

4. **Backend**: for data-driven plots, confirm the plotting backend. Python (matplotlib/seaborn) is
   the default. If R (ggplot2/patchwork) is preferred, the user must explicitly request it. For
   non-data pictures **and pipeline / architecture / teaser concept figures**, the backend is the
   configured picture API for the illustration plus a deterministic LaTeX/TikZ text overlay for all
   labels (the hybrid pattern in `picture-generation.md`) — the image model never renders text.
   Use a pure TikZ/FigureSpec schematic only when the user explicitly asks for an editable diagram.
   Do not hand-draw pipeline boxes in matplotlib; that route produced faint boxes, broken arrows,
   and overflowing text.

5. **Export contract**: set final dimensions (single-column or double-column), primary output format
   (PDF for LaTeX data charts; PNG for AI-generated pictures; SVG for editable diagrams), target
   DPI, color space, and whether editable text is required. For data charts, PDF is the canonical
   output with PNG as raster fallback.

### Display Width Contract

Every planned figure or table must declare one layout target:

- `single-column`: insert with `\includegraphics[width=\linewidth]`, `\columnwidth`, or a table
  whose tabular environment is bounded by `\linewidth`.
- `double-column`: use `figure*` or `table*` and bound content by `\textwidth`.
- `appendix`: still choose `single-column` or `double-column`; appendix material must not exceed
  the printable area.
- `supplement`: use when the item is too wide or dense to stay readable in the paper.

Long-text tables must use wrapping columns (`tabularx` or `p{...}` widths tied to `\linewidth` or
`\textwidth`). Pure `l/c/r` columns are allowed only when every cell is short enough to fit the
declared layout. Scaling a table down with `\resizebox` is a last resort for numeric tables, not a
default for prose-heavy tables.

### Display Review Gate (executable — render, look, regenerate)

A figure is not done when the script runs without error. It is done when its **rendered
PNG** has been opened and inspected. Judging a figure from the code alone is the main
reason generated figures ship ugly. After every data-driven figure (and after any change
to one), run this loop:

1. **Render** all three formats (SVG, PDF, PNG) via `save_figure`.
2. **Look** at the PNG (open/read the image, do not infer from code).
3. **Score against the failure signatures** below. Any HIT means revise the script and
   regenerate — do not accept the figure until every signature is clear.

**Failure signatures (the four that make figures ugly):**

| Signature | What to look for in the PNG | Fix |
|---|---|---|
| **Muddy overlap** | Filled radar/area/series blur into an indistinct blob; can't separate methods. | Radar: ≤4 traces, drop fills, per-spoke normalize, or split into small multiples. Areas: lower alpha or switch to lines. |
| **Clipped elements** | Error-bar whiskers, caps, value labels, or markers touch or cross the axis/figure edge. | Use the error-bar-aware `ylim` (include `vals ± err` + label headroom); never compute limits from bar heights alone. |
| **Low contrast / color-only** | A foreground series is grey/washed out; cell/in-bar text disappears into its background; series are told apart by hue alone (fails in grayscale / for colorblind readers); a rainbow/jet colormap is used. | Grey only for neutral/receding series; give compared series distinct hues from a luminance-balanced, colorblind-safe palette plus a redundant marker/hatch; pick text color by luminance of the rendered color; never use rainbow/jet. |
| **Label collision** | Tick labels, spoke labels, radial ticks, legend, or annotations overlap each other or the data. | Offset spoke labels beyond the outer ring; rotate/`ha` x-ticks; move legend below; remove default polar grid/ticks. |

**For illustration / pipeline / teaser figures (AI-generated), also score these:**

| Signature | What to look for in the PNG | Fix |
|---|---|---|
| **Garbled in-image text** | Any word rendered by the image model; misspellings like `Indulator`, `Missformation`; a prompt header such as `Message:` drawn into the figure. | The image model must render **no text**. Regenerate with the no-text instruction; add every label via the TikZ overlay (`picture-generation.md`). |
| **Boxy flowchart** | Just rounded rectangles in a row with arrows — a slide diagram, not an illustration. | Rewrite the Direct Image Prompt toward a scene (devices, UI, icons, actors); drop "rounded rectangles / boxes in a row". |
| **Empty bands / off-center** | A large blank strip (e.g. top or right ~40%) while content crowds one side. | Re-prompt for an evenly filled, balanced composition; set the canvas/aspect to the target column width. |
| **Overlay misalignment** | After TikZ overlay, a label floats off its element or runs off the image. | Open the PDF, nudge the normalized `(x,y)` coordinates, recompile, re-inspect. |

Then confirm the contract checks:

- All planned panels appear and serve the core conclusion,
- No extra claim, dataset, metric, or module was invented by the renderer,
- Visible text is readable at paper scale and matches the allowed labels from the Writing Policy,
- The item fits its declared single-column or double-column width,
- Arrows, relationships, and data direction are correct,
- The item is paper-ready rather than slide-deck decorative,
- The generated file is non-empty and stored at the recorded output path.

If any check or signature fails, revise and regenerate. Keep rejected versions only when
useful for audit.

### Unified visual family

All figures in one paper must read as a set, not as figures from different papers. Before
finalizing the figure set, confirm across every figure:

- **One palette**: the same method → the same color in every figure; reuse `PEER_PALETTE`
  / `HERO_PALETTE` consistently, never remap.
- **One type system**: the same font family and a consistent size hierarchy (axis vs tick
  vs annotation) across figures.
- **Consistent encodings**: the same metric uses the same axis orientation, unit, and
  colormap everywhere; shared legends use the same ordering.

After all figures pass the review gate, write a single `paper/figures/latex_includes.tex`
that collects each figure's `\includegraphics` + `\caption` + `\label` block, so the main
draft can `\input` them and inclusion stays consistent.

## Figure Plan Format

Use a compact table in the Paper Framework:

```markdown
| ID | Type | Layout | Section | Message | Source | Generation route |
|---|---|---|---|---|---|---|
| Fig. 1 | overview / pipeline | double-column | Introduction | Shows the paper's problem-setting-method-evidence arc. | Writing Policy + method notes | FigureSpec MCP or manual SVG |
| Fig. 2 | main result plot | single-column | Experiments | Shows the primary comparison supporting C1. | `results/main.csv` | reproducible plot script |
| Tab. 1 | taxonomy table | single-column | Method | Defines task categories with examples. | benchmark manifest | LaTeX `tabularx` |
```

Keep only likely main-paper figures and tables. Put appendix-only or optional visuals in drafting
notes, not the main framework.

## What To Draw

Choose figures by paper need, not decoration:

| Need | Recommended visual | Usual section |
|---|---|---|
| Reader needs the whole idea early | teaser / overview figure | Introduction |
| Method has ordered stages | pipeline diagram | Method / System |
| System has components or interfaces | architecture diagram | Method / System |
| Benchmark has task/data construction | benchmark construction flow or taxonomy | Benchmark / Dataset |
| Claim depends on a comparison | bar, line, scatter, heatmap, or table | Experiments / Evaluation |
| Claim depends on robustness | stress-test plot, ablation table, failure taxonomy | Experiments / Analysis |
| Claim depends on examples | qualitative case grid or example table | Analysis / Discussion |

Avoid figures that only restate text, repeat a table without adding comparison value, or introduce
unsupported claims.

## Insertion Rules

- Put the first overview/teaser figure in the Introduction only when it helps a skim reader
  understand the contribution before Method.
- Put architecture and pipeline figures where the corresponding mechanism is defined.
- Put main-result figures before ablations and secondary analyses.
- Put failure cases near the claim they limit or explain.
- Do not reference a figure before the paper has defined the terms needed to understand it.
- If a figure would force a different section order, update the Paper Framework and ask the user to
  confirm.

## Generation Routes

Use the lightest reliable route:

| Route | Use for | Output |
|---|---|---|
| existing asset | screenshots, qualitative examples, already-drawn diagrams | copied asset under `paper/figures/` |
| reproducible plot script | numeric results, ablations, scaling, heatmaps | Python script following `plot-style.md` rules and `chart-patterns.md` patterns + SVG/PDF/PNG |
| LaTeX table | result tables, feature comparison, benchmark statistics | `.tex` table or inline table |
| AI illustration + TikZ overlay (default for concept figures) | teasers, conceptual method illustrations, **pipeline / architecture / workflow** overview figures | text-free PNG from the picture API + TikZ overlay supplying every label |
| TikZ / FigureSpec schematic | only when the user explicitly wants an editable node-edge diagram or a formal graph/state machine | `.tex`/JSON spec + SVG/PDF |
| current-agent drawing | fallback when no image API exists | agent-created illustration plus Picture Brief; still overlay text deterministically |

For plots, data-driven plots default to Python. Do not hardcode numbers from memory. Read from
result files and follow `plot-style.md`. For diagrams, keep the source specification or source file
so the figure can be revised. For AI-generated pictures, follow `picture-generation.md`: always
write `paper/figures/prompts/<figure-id>.md` before rendering, and do not let the image renderer
invent claims, modules, datasets, results, or labels.

## MCP Contract

If a `paper-figure` or FigureSpec-compatible MCP is available, use it only for figure-specific
tasks:

- classify a proposed visual into a route,
- write a FigureSpec JSON skeleton,
- validate or render a deterministic diagram,
- record figure metadata for later LaTeX insertion.

The MCP must not invent paper claims, experiment results, citations, or section structure. It works
from the confirmed Writing Policy, confirmed Paper Framework, and concrete source files.

Suggested MCP outputs:

```text
paper/figures/figure-plan.md
paper/figures/specs/<figure-id>.json
paper/figures/prompts/<figure-id>.md
paper/figures/<figure-id>.svg
paper/figures/<figure-id>.pdf
paper/figures/<figure-id>.png
paper/figures/latex_includes.tex
```

If the MCP is unavailable, continue with current-agent drawing for pictures and direct Python
generation for data charts.

## Caption Rule

Every caption should state:

1. the figure's message,
2. the comparison or mechanism shown,
3. the claim or section argument it supports.

Avoid captions that merely list visual elements.
