# Figure Planning

Use this reference only when a Paper Framework, full draft, or revision needs figures or tables.
Do not load it for purely textual Writing Policy work unless the user explicitly asks about figures.

## Purpose

Figure planning decides three things:

1. what visual asset the paper needs,
2. where it should be inserted,
3. how it should be generated or sourced.

It does not decide the paper's core claims. Claims and evidence come from the Writing Policy.

## Figure Contract

A publication-quality academic figure is a visual argument, not a decorative chart. Before filling
the Figure Plan routing table, establish the contract below for each planned figure. This applies
to all figure types: data plots, architecture diagrams, pipeline figures, teaser pictures, and
qualitative grids.

### The Five-Point Figure Contract

Before assigning a generation route or writing code, establish:

1. **Core conclusion**: the one-sentence claim this figure must defend. Every panel, label, and
   visual choice must serve this conclusion. If a planned panel does not carry a unique piece of
   evidence for the conclusion, drop it or merge it.

2. **Evidence chain**: map each planned panel/subfigure to a specific piece of evidence from the
   Writing Policy. A panel without a mapped claim or evidence source is decoration and should be
   removed. The chain must trace back to concrete workspace result files or confirmed paper facts.

3. **Archetype**: classify the figure into one of:
   - `quantitative comparison`: bar, line, scatter, heatmap, or table driven by result data,
   - `pipeline-architecture`: ordered stages, system components, or workflow with node-edge
     relationships,
   - `teaser-composite`: overview illustration combining problem, method, and evidence visually,
   - `qualitative-grid`: example cases, screenshots, or image panels showing representative outputs.
   The archetype determines the generation route, not the other way around.

4. **Backend**: for data-driven plots, confirm the plotting backend. Python (matplotlib/seaborn) is
   the default. If R (ggplot2/patchwork) is preferred, the user must explicitly request it. For
   non-data pictures, the backend is the configured picture API or current-agent drawing. For
   architecture diagrams, the backend is FigureSpec MCP + renderer or current-agent drawing.

5. **Export contract**: set final dimensions (single-column or double-column), primary output format
   (PDF for LaTeX data charts; PNG for AI-generated pictures; SVG for editable diagrams), target
   DPI, color space, and whether editable text is required. For data charts, PDF is the canonical
   output with PNG as raster fallback.

### Figure Review Gate

Before accepting a generated figure, inspect it against the contract:

- All planned panels appear and serve the core conclusion,
- No extra claim, dataset, metric, or module was invented by the renderer,
- Visible text is readable at paper scale and matches the allowed labels from the Writing Policy,
- Arrows, relationships, and data direction are correct,
- The figure is paper-ready rather than slide-deck decorative,
- The generated file is non-empty and stored at the recorded output path.

If any check fails, revise and regenerate. Keep rejected versions only when useful for audit.

## Figure Plan Format

Use a compact table in the Paper Framework:

```markdown
| ID | Type | Section | Message | Source | Generation route |
|---|---|---|---|---|---|
| Fig. 1 | overview / pipeline | Introduction | Shows the paper's problem-setting-method-evidence arc. | Writing Policy + method notes | FigureSpec MCP or manual SVG |
| Fig. 2 | main result plot | Experiments | Shows the primary comparison supporting C1. | `results/main.csv` | reproducible plot script |
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
| reproducible plot script | numeric results, ablations, scaling, heatmaps | Python script + PDF/PNG |
| LaTeX table | result tables, feature comparison, benchmark statistics | `.tex` table or inline table |
| FigureSpec MCP | architecture, pipeline, workflow, taxonomy diagrams | JSON spec + SVG/PDF |
| AI picture generation | teaser pictures, conceptual method illustrations, polished raster overview pictures | Picture Brief + generated PNG |
| current-agent drawing | necessary picture but no user-configured image API exists | agent-created PNG plus Picture Brief |

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
