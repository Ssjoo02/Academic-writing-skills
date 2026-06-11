# Journal Systems / Tools / Library Paper Type

Use this profile for journal papers whose main contribution is a usable software system, library,
toolkit, or platform. Representative shape: JMLR Open Source Software (OSS/MLOSS) track papers
(e.g., a Python causal-discovery library: state the user pain point, present a unified modular
architecture with broad algorithm coverage, and document reproducible usage). These papers are
short and dense.

## Section Structure (Paper Framework hard default)

This file gives the **default section list, order, naming, count, and budget** for this paper type.
The Paper Framework stage treats it as a **hard default, not loose inspiration**: by default,
reproduce the section table below exactly (its section column, in order) and quote it as the canonical
list in the Paper Framework's "Structure vs paper-type profile" comparison. This file does not
prescribe writing style, reviewer strategy, claims, evidence, or citations.

Deviate only when the actual contribution, evidence, venue requirement, or explicit user request
genuinely cannot fit this structure — never merely because another layout seems "cleaner" or "more
standard". Every split, merge, rename, addition, or reorder must be surfaced and approved at the Paper
Framework checkpoint; silent structural deviation is a workflow violation.

## Length: Defer To The Venue Card

This is a journal paper. The JMLR OSS/MLOSS track is SHORT (~8 pages); a tool paper in a longer
journal can be fuller. Take absolute length from the venue card and keep the writing compact and
concrete. Move exhaustive API listings and tutorials to the documentation/appendix. Also load
`references/venues/journal-vs-conference.md`.

## Priority Contract

- Primary core: Design / Architecture.
- Evidence core: Usage: Demos, APIs, Documentation, Benchmarks.
- Compress first: Conclusion, broad Introduction, exhaustive API listings, tutorials, and per-module tables.
- Core floor: protect design philosophy, architecture, module coverage, and minimal reproducible
  usage; if the venue is short, move exhaustive API detail to documentation before shrinking Design /
  Architecture below its proportional floor.

## Section And Proportional-Budget Reference

| Order | Candidate section | Share of main text | Section role |
|---|---:|---:|---|
| Front | Abstract | ~5-7% | State what the tool is, who it serves, what it covers, and where it lives (link). |
| 1 | Introduction | ~20-28% | Define the user pain point (fragmented/hard-to-use prior tools), the design philosophy (open, modular, documented), and what the tool uniquely provides. |
| 2 | Design / Architecture | ~35-45% | Present the module structure and the breadth of coverage; use a methods/feature table and clear subsections (e.g., core algorithm families, building-block modules, utilities). This is the core. |
| 3 | Usage: Demos, APIs, Documentation, Benchmarks | ~18-26% | Show minimal reproducible examples, the unified API, where the docs live, and bundled benchmark datasets / tests. |
| 4 | Conclusion | ~5-8% | Restate the value over fragmented prior implementations and the extension/maintenance path. |
| Back | Appendix / Online docs | outside main budget | Full API reference, extended examples, installation details, and per-module tables. |

## Flexible Adjustment Notes

- Lead with the user's problem and the design philosophy, then prove coverage with a structured
  table; do not narrate every function.
- Show a minimal runnable example early; "how do I use it in five lines" is a core reviewer
  question for tool papers.
- Be explicit about what the tool does, how to install/integrate it, why it beats scattered prior
  implementations, and how it can be extended — these four are the OSS reviewer checklist.
- Keep exhaustive API surface in the documentation, not the paper.
- If the contribution is a deployed end-to-end platform with operational/scalability evidence rather
  than a library, consider the conference `systems-implementation-paper.md` structure for the
  systems-engineering emphasis, adapted to journal length.
