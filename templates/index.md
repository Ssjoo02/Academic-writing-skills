# Venue Template Index

Use this file only when a workflow needs to initialize a LaTeX paper project or record the selected
venue template in the Paper Framework. Do not load template `.tex`, `.cls`, or `.bst` files as
writing references unless editing the LaTeX project itself.

## Template Mapping

| Venue target | Primary template | Required companion files | Citation style | Notes |
|---|---|---|---|---|
| Generic / venue TBD | `generic_article.tex` | `math_commands.tex` | natbib numeric | Non-submission draft template used only when the target venue is not selected. Replace with the official target-venue template before submission. |
| ICLR | `iclr2026.tex` | official `iclr2026_conference.sty` must be available in the output project | natbib-style author-year | Template source noted in file header. |
| NeurIPS | `neurips2025.tex` | official `neurips_2025.sty` must be available in the output project | natbib-style author-year | Template source noted in file header. |
| ICML | `icml2025.tex` | official `icml2025.sty` must be available in the output project | natbib-style author-year | Template source noted in file header. |
| IEEE conference | `ieee_conference.tex` | `IEEEtran.cls`, `IEEEtran.bst` | numeric `\cite{}` | References usually count toward the page limit. |
| IEEE journal | `ieee_journal.tex` | `IEEEtran.cls`, `IEEEtran.bst` | numeric `\cite{}` | Usually not anonymous; journal-specific limits vary. |

## Common File

- `math_commands.tex`: common math macro starter copied into the output `paper/` project.

## Selection Rules

1. Select the template from the confirmed target venue in the Writing Policy or Paper Framework.
2. If the target venue is not selected, use `generic_article.tex` only as a non-submission draft
   template and record that the official venue template remains unresolved.
3. If no matching preloaded template exists, use a user-provided official template or the official
   template source recorded in the venue profile or maintenance records.
4. Do not invent venue formatting from memory.
5. When the selected template has fixed default section includes, update `main.tex` to match the
   confirmed Paper Framework section list.
