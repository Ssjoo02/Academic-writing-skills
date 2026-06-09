# Generic Journal Paper Type

Use this profile when the paper is clearly a journal submission but its type is unknown, mixed,
early-stage, or not well captured by a specific journal profile. It follows a complete,
self-contained research-article structure while staying neutral about contribution type. This is the
journal fallback, parallel to the conference-side `generic-paper.md`.

## Use Only As Section Planning Reference

This file is only a section and proportional-budget reference for building a Paper Framework. It is
not a fixed paper template and does not prescribe writing style, reviewer strategy, claims,
experiments, or citations.

Adapt sections and budgets to the actual paper, venue, evidence, and user request. Do not copy this
structure mechanically. Merge, rename, split, shrink, or remove sections when the confirmed venue,
contribution, evidence package, or page budget requires it.

## Length: Defer To The Venue Card

This is a journal paper. Do NOT use a conference soft page budget. Take absolute length from the
venue card and plan sections as proportions first. Prefer a complete, self-contained article over a
compressed one. Also load `references/venues/journal-vs-conference.md`.

## Section And Proportional-Budget Reference

| Order | Candidate section | Share of main text | Section role |
|---|---:|---:|---|
| Front | Abstract | ~3-5% | State problem, gap, contribution, main evidence, and scoped takeaway. |
| 1 | Introduction | ~12-18% | Move from problem and motivation to gap, core idea, contributions, and evidence preview. |
| 2 | Related Work | ~8-14% | Provide a fair, current map of the area and clarify the difference from the closest lines. |
| 3 | Core Contribution (Method / Study / Resource) | ~22-32% | Explain the central contribution in full detail, adapted to what it is. |
| 4 | Experiments / Evaluation / Analysis | ~22-32% | Present setup, main evidence, comparisons, ablations or controls, qualitative analysis, and failure cases. |
| 5 | Discussion | ~6-12% | Interpret findings, trade-offs, implications, and boundary conditions. |
| 6 | Conclusion | ~3-5% | Summarize the contribution and supported takeaway. |
| End | Limitations | venue-dependent | Scope limits, assumptions, evidence gaps, risks. |
| Back | Appendix / Supplement | outside main budget | Extra details, proofs, extended tables, and additional examples. |

## Flexible Adjustment Notes

- If the contribution is clearly theory, method/scaling, systems/tool, evaluation, dataset,
  application, survey, or position, prefer that specific journal profile under
  `references/paper-types/journal/`.
- Favor completeness and thorough evidence over conference-style compression; this is a journal.
- Keep the absolute length governed by the venue card, not by this file.
