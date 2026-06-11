---
name: academic-figure
description: Use when creating, revising, auditing, or polishing figures and tables for a research paper — data-driven plots (bar/line/heatmap/radar/scatter), concept/teaser/pipeline/architecture illustrations, multi-panel composites, and publication LaTeX tables (booktabs, span/overflow/appendix layout). Triggers on figure/table requests with or without a full draft, including Chinese phrasings like 论文配图、科研绘图、画图、作图、出图、论文图表、画个图、配图、表格排版、做表. Part of the academic-writing collection; the academic-writing hub delegates all figure/table work here.
---

# Academic Figure & Table — Router

This skill produces and audits every **figure and table** for a paper. It is independently
invokable ("just make this figure", "fix this table's layout") and is also the subsystem the
**`academic-writing`** hub delegates to whenever a draft needs a display item.

It is split into two layers:

- A **static layer** under `static/` with the figure and table execution rules
  (`figure-handling.md`, `table-handling.md`).
- A **dynamic layer** (this file + `manifest.yaml`) plus deep references under `references/`
  (figure planning, plot style, chart patterns, sizing, QA, table design, prose/appendix placement).

Cross-skill stance and integrity rules live in `../../_shared/core/`. Do not draw figures from
memory or from this router — load the rules from disk.

## ⚠️ Scope and integrity

Figures and tables present existing evidence; they never invent it. Read data from workspace result
files; **do not hardcode numbers from memory**, and do not "improve" results. A figure with an
unsupported or fabricated value is a defect, not a polish. Mirror the user's interaction language
(see `../../_shared/core/stance.md`).

## Routing protocol

1. **Load the core layer.** Read `manifest.yaml` and the `always_load` file
   (`../../_shared/core/stance.md`) for language and integrity policy.
2. **Classify the display item.** Decide which execution fragment applies:
   - Any figure (data-driven plot or concept illustration) → `static/figure-handling.md`.
   - Any table → `static/table-handling.md`.
   A request with both loads both.
3. **Resolve the venue kind** (conference or journal) — it selects the sizing reference and, for
   journal, the figure-contract. Default to conference unless the caller says journal.
4. **Build the item using the loaded fragment**, then open the deep references it points to on demand
   (see the `references.on_demand` table in the manifest): `references/figures/plot-style.md` and the
   venue sizing file before any data plot, `references/figures/picture-generation.md` before any
   concept figure, `references/figures/chart-patterns.md` for reusable helpers,
   `references/figures/figure-planning.md` for the Display Review Gate, `references/tables/table-design.md`
   for table span/QA, `references/sections/figures-and-tables.md` for prose/appendix placement, and
   `references/figures/qa-contract.md` for the final cross-figure check.
5. **Inspect every rendered item before accepting it.** A script that runs without error is not a
   passing figure; the looked-at PNG / compiled PDF page is. Run the Display Review Gate and, for
   tables, the overflow/appendix inspection.

## Optional MCP figure server

`mcp-servers/paper-figure/` provides an optional image-generation server for concept figures
(teaser / pipeline / architecture). Use it when the user has configured a picture API; otherwise the
executing agent draws from the Picture Brief. See `references/figures/picture-generation.md`.

## Why this split

- The figure/table subsystem is self-contained and heavy, so it lives in its own skill and can be
  invoked alone.
- Each invocation loads only the relevant handling fragment plus the references that step needs,
  instead of the whole figure corpus.
