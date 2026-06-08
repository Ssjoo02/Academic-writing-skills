# Venue Template Index

Use this file only when a workflow needs to initialize a LaTeX paper project or record the selected
venue template in the Paper Framework. Do not load template `.tex`, `.cls`, or `.bst` files as
writing references unless editing the LaTeX project itself.

## Template Mapping

| Venue target | Primary template | Required companion files | Citation style | Notes |
|---|---|---|---|---|
| Generic / venue TBD | `generic_article.tex` | `math_commands.tex` | natbib numeric | Non-submission single-column draft template used only when the target venue is not selected. Soft drafting budget: 6-8 main-text pages, excluding references and appendix. Replace with the official target-venue template before submission. Its default section inputs are placeholders; replace them with the confirmed Paper Framework section list. |
| ICLR | `iclr2026.tex` | `iclr2026_conference.sty`, `iclr2026_conference.bst`, `math_commands.tex` | natbib-style author-year | ICLR 2026 official template and style companions are preloaded. |
| NeurIPS | `neurips2026.tex` | `neurips_2026.sty`, `checklist.tex` | natbib-style author-year | NeurIPS 2026 official template, style file, and checklist are preloaded. Keep `neurips2025.tex` only for reproducing older drafts. |
| ICML | `icml2026.tex` | `icml2026.sty`, `icml2026.bst`, `algorithm.sty`, `algorithmic.sty` | natbib-style author-year | ICML 2026 official example, style file, and bundled algorithm helpers are preloaded. Keep `icml2025.tex` only for reproducing older drafts. |
| ACL / EMNLP / NAACL | `acl2026.tex` | `acl.sty`, `acl_natbib.bst` | ACL natbib author-year | Shared *ACL official style files. Use the exact year/venue variant if the target venue provides one. |
| CVPR | `cvpr2026.tex` | `preamble.tex`, `cvpr.sty`, `ieeenat_fullname.bst` | numeric `\cite{}` | CVPR 2026 official author-kit files are preloaded. The raw official template has fixed sample inputs; replace them with the confirmed Paper Framework section list. |
| AAAI | `aaai2026.tex` | `aaai2026.sty`, `aaai2026.bst`, `aaai2026.bib` | natbib numeric | AAAI 2026 anonymous-submission LaTeX files are preloaded. |
| IJCAI / IJCAI-ECAI | `ijcai26.tex` | `ijcai26.sty`, `named.bst`, `ijcai26.bib` | named author-year | IJCAI-ECAI 2026 formatting-guideline LaTeX files are preloaded. Do not substitute AAAI formatting for IJCAI. |
| ACM / KDD / WWW / SIGIR / CHI / UIST | `acm_mm2026.tex` | `acmart.cls`, `acm.bst` | ACM author-year or numeric depending on venue instructions | Generic ACM `sigconf` starter. Update conference metadata and review/camera-ready options from the target venue guidance before submission. |
| IEEE conference | `ieee_conference.tex` | `IEEEtran.cls`, `IEEEtran.bst` | numeric `\cite{}` | References usually count toward the page limit. |
| IEEE journal | `ieee_journal.tex` | `IEEEtran.cls`, `IEEEtran.bst` | numeric `\cite{}` | Usually not anonymous; journal-specific limits vary. |

## Common File

- `math_commands.tex`: common math macro starter copied into the output `paper/` project.

## Selection Rules

1. Select the template from the confirmed target venue in the Writing Policy or Paper Framework.
2. If the target venue is not selected, use `generic_article.tex` only as a non-submission
   single-column draft template. Record the page/length budget as a soft 6-8 main-text-page drafting
   budget, excluding references and appendix, and record that the official venue template remains
   unresolved. The template's default section inputs are placeholders; replace them with the
   confirmed Paper Framework section list before drafting.
3. If no matching preloaded template exists, use a user-provided official template or the official
   template source recorded in the venue profile or maintenance records.
4. Do not invent venue formatting from memory.
5. Official venue templates are format shells, not prose sources. After copying a template, remove
   official sample or instruction body text and keep only the format setup, required commands,
   bibliography hooks, and verified post-main hooks.
6. When the selected template has fixed default section includes, update `main.tex` to match the
   confirmed Paper Framework section list.
