# Appendix And Supplement Guide

Use this guide when drafting, revising, or assembling appendix / supplement material.

## Appendix Is Support, Not A Second Main Paper

The appendix carries material that supports verification, reproducibility, completeness, or reader
trust without being required for the main argument's first-pass comprehension.

Put here:

- full taxonomy, inventory, prompt, protocol, or configuration lists after the body states the
  argumentative summary,
- full proofs when the main body gives the statement and proof sketch,
- extended result matrices, robustness sweeps, secondary ablations, or qualitative example sets,
- extra implementation or dataset details needed for reproducibility.

Do not hide main evidence. If a result is needed to believe the Abstract, Introduction, central
Method claim, or headline experiment, keep the compact evidence in the main text and move only the
full version to the appendix or supplement.

## Required Appendix Plan

Before writing appendix content, create or update `paper/appendix-plan.md`. Each row records:

| Item ID | Type | Claim backed | Source availability | Fill status | Main-text anchor | Fallback |
|---|---|---|---|---|---|---|

- `Claim backed`: the exact claim, section, figure, or table this item supports.
- `Source availability`: existing source path, confirmed user-provided source, or missing.
- `Fill status`: `filled`, `partial`, or `omitted`.
- `Main-text anchor`: the body sentence/table/figure that points to the item.
- `Fallback`: compress, omit, move to separate supplement, or mark evidence missing.

No stubs. Do not write "see supplementary material", "details omitted", or an empty appendix section
when the source exists. If the source is missing, omit the claim or mark the evidence risk instead of
inventing content.

## Writing Shape

Every appendix subsection needs a 2-4 sentence lead paragraph before any float, list, or proof. The
lead says what the item is, how to read it, and which main-text claim it backs.

Keep appendix prose concise:

1. Lead paragraph.
2. Full table/proof/list/example set.
3. Optional one-sentence note on scope or interpretation.

Do not repeat the main paper's motivation or result narrative. Cross-reference labels normally:
`Appendix~\ref{...}`, `Table~\ref{...}`, `Figure~\ref{...}`.

## Placement And Venue Rule

Follow the confirmed Venue Assembly Plan. Some venues allow appendices after references; some journals
require separate supplementary files; some venues count appendix pages or forbid main-PDF appendices.
If appendix movement is forbidden or counted against the active limit, do not use appendix movement as
a page-budget fix.

For figures and tables, use the `academic-figure` table placement and figure planning references for
span, overflow, and float-order rules. Appendix placement is not permission to exceed the printable
area.

## Self-Check

- Is every appendix item listed in `paper/appendix-plan.md`?
- Is every item source-backed or explicitly omitted?
- Does each item have a main-text anchor?
- Does each subsection have a real lead paragraph?
- Is no central evidence hidden outside the main reading path?
