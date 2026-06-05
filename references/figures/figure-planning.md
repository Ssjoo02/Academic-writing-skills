# Figure Planning

Use this reference only when a Paper Framework, full draft, or revision needs figures or tables.
Do not load it for purely textual Writing Policy work unless the user explicitly asks about figures.

## Purpose

Figure planning decides three things:

1. what visual asset the paper needs,
2. where it should be inserted,
3. how it should be generated or sourced.

It does not decide the paper's core claims. Claims and evidence come from the Writing Policy.

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
| reproducible plot script | numeric results, ablations, scaling, heatmaps | script + PDF/PNG |
| LaTeX table | result tables, feature comparison, benchmark statistics | `.tex` table or inline table |
| FigureSpec MCP | architecture, pipeline, workflow, taxonomy diagrams | JSON spec + SVG/PDF |
| manual drawing note | necessary visual but no reliable source/generator exists | `% FIGURE_NEEDED:` marker |

For plots, do not hardcode numbers from memory. Read from result files. For diagrams, keep the
source specification or source file so the figure can be revised.

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
paper/figures/<figure-id>.svg
paper/figures/<figure-id>.pdf
paper/figures/latex_includes.tex
```

If the MCP is unavailable, continue with local scripts or explicit `FIGURE_NEEDED` markers.

## Caption Rule

Every caption should state:

1. the figure's message,
2. the comparison or mechanism shown,
3. the claim or section argument it supports.

Avoid captions that merely list visual elements.
