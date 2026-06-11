# Figure Handling

Execution rules for producing every figure in a paper draft. Pair this with `table-handling.md` for
tables. The deep references live under `references/figures/`.

**Before generating any data-driven figure, load these in order:**
1. `references/figures/plot-style.md` — venue-agnostic shared rules (rcParams, colors,
   per-chart-type rules, legend rules, multi-panel architecture).
2. Venue-specific sizing:
   - Conference: `references/figures/conference/figure-sizing.md`
   - Journal: `references/figures/journal/figure-sizing.md`
3. `references/figures/chart-patterns.md` — reusable Python helpers (`save_figure`,
   `grouped_bars`, `trend_lines`, `heatmap`, `radar_chart`, etc.).
4. `references/figures/figure-planning.md` — Display Item Contract, Display Review Gate,
   failure signatures, generation routes.
5. Journal only: `references/figures/journal/figure-contract.md` — journal-specific
   archetypes, panel logic, aesthetic integration, reviewer-risk checklist.
**After all figures pass their individual review gates:**
6. `references/figures/qa-contract.md` — submission-readiness cross-figure checklist
   (statistics minimum, image-integrity, export bundle).

**Before any concept figure (teaser / pipeline / architecture / workflow):** load
`references/figures/picture-generation.md`. These are **illustrations**, not
matplotlib boxes: the image API draws the scene and may render the short labels
directly, which are then **verified for correct spelling and terminology**
(generate-then-verify); the TikZ overlay is a fallback for a label the model
misspells. Do **not** hand-draw pipeline boxes in matplotlib.

**Framework-to-artifact alignment is a hard gate.** The confirmed Paper Framework's Figure Plan is
an execution contract, not a suggestion. Before drawing or inserting anything, create
`paper/framework-execution-report.md` with one row per planned main-paper figure/table: planned ID,
type, layout, target section, expected artifact(s), LaTeX label, status, and QA notes. This report is
updated as each item is generated and inserted. A planned main-paper display item may not be left as
`not yet generated`, a registry comment, or a missing placeholder. If an item cannot be generated or
must move to appendix/supplement, update the Paper Framework and ask for user confirmation before
returning `paper/`.

1. Read the confirmed Figure Plan from the Paper Framework and initialize
   `paper/framework-execution-report.md`.
2. Resolve the Image Renderer Preference. If the user configured a picture API (GPT-image2, Gemini),
   use it for picture figures after the Picture Brief. Otherwise the current executing agent draws
   the picture from the brief.
3. **Data-driven plots**: follow `references/figures/plot-style.md` (rcParams, colors,
   per-chart-type rules) and the venue-specific sizing file:
   - Conference: `references/figures/conference/figure-sizing.md`
   - Journal: `references/figures/journal/figure-sizing.md`
   Default to Python; do not create shared style modules, scripts directories, derived
   data folders, or audit files by default. Read data from workspace result files; do not
   hardcode results from memory. Use `save_figure()` from
   `references/figures/chart-patterns.md` to export SVG (primary, editable text) + PDF
   (LaTeX inclusion) + PNG (raster preview, >=300 DPI). Write chart files under
   `paper/figures/`.
4. **Concept figures (teaser / pipeline / architecture / workflow)**: follow
   `references/figures/picture-generation.md`. Write the Picture Brief to
   `paper/figures/prompts/<figure-id>.md` first, with a clean illustrative Direct Image Prompt (a
   scene, not rounded-rectangle boxes) that names the exact short labels to render, spelled
   correctly, plus a Label Verification Plan. Prompt for a **wide, short banner that fills the frame**
   (target aspect ~3:1 double-column) so the figure is ~4.5–6 cm tall, not ~10 cm with empty bands.
   Generate `paper/figures/<figure-id>.png` via the configured image API (or current-agent fallback)
   with its labels, then **verify every visible label against the Writing Policy terminology**;
   regenerate (or fix that label with the TikZ overlay fallback) if any word is misspelled, wrong, or
   duplicated. When an overlay is used, **clamp the `tikzpicture` bounding box to the image**
   (`\useasboundingbox (img.south west) rectangle (img.north east);`) and **inset edge labels
   anchored inward** so no overlay node pushes the figure into the margin (the Overlay Bounding-Box
   Rule). If a render is mis-shaped, cap the height (`height=...,keepaspectratio`) or trim baked-in
   whitespace (`trim=...,clip`). Use a pure TikZ/FigureSpec schematic only when the user explicitly
   wants an editable diagram. Do not leave a planned figure blank, and do not ship a misspelled or
   unsupported label.
5. **Screenshots/qualitative examples**: use existing workspace assets and record their source.
6. **Inspect every rendered figure before accepting it.** After rendering, open the PNG and run the
   executable Display Review Gate in `references/figures/figure-planning.md`: check the data-chart
   signatures (muddy overlap, clipped elements, low contrast, label collision) and, for concept
   figures, the illustration signatures (misspelled / wrong in-image labels, boxy flowchart, empty
   bands / too tall, out-of-bounds overflow, overlay misalignment). After compiling, also confirm `main.log` has
   **no `Overfull \hbox` for the figure** (a figure overflowing the margin — "出界" — is a blocking
   defect that `audit_draft.py` fails on). Regenerate until all clear. A script that runs without
   error is not a passing figure; the looked-at PNG is.
   Compact single-column heatmaps, coverage matrices, and secondary data grids should normally be
   inserted at `0.60--0.70\linewidth` in one-column templates. Treat `>0.70\linewidth` as a layout
   defect unless the confirmed Framework explicitly budgets it as a large main evidence figure.
7. Insert each figure/table only in the section specified by the confirmed Paper Framework, then mark
   the corresponding `paper/framework-execution-report.md` row as inserted with its final `\label`.
8. After all figures pass the gate, confirm the unified visual family (one palette, one type system,
   consistent encodings) and collect inclusion blocks into `paper/figures/latex_includes.tex`. This
   file is a registry of completed inclusion blocks; it must not contain `not yet generated`,
   `FIGURE_NEEDED`, or any planned item without a real artifact.
9. Captions must state the figure's message and supported claim, not merely describe visual content.
10. After every figure has passed its individual Display Review Gate and the unified visual family
    check, run the cross-figure submission-readiness checklist in
    `references/figures/qa-contract.md` (statistics minimum, image-integrity, export bundle,
    venue-specific notes). This is the final gate before figures are accepted.

For how figures and tables sit in the prose and in the appendix (placement, captions, appendix float
discipline), see `references/sections/figures-and-tables.md`.
