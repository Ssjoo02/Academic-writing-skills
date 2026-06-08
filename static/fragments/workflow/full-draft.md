# Full Draft Workflow

Use this workflow when the user provides a workspace or asks for a complete first paper draft from
project materials.

## State Machine

```text
Workspace
  -> Workspace Discovery
  -> Writing Policy
  -> User confirmation
  -> Paper Framework
  -> User confirmation
  -> Full Draft LaTeX Project
```

## Stage Outputs

Create each output only when its stage is reached and its upstream gate has been satisfied.

| Stage | Output |
|---|---|
| Writing Policy | `writing-policies/<paper-slug>-writing-policy.md`; optional complete translated sibling artifacts only when requested |
| Paper Framework | `writing-policies/<paper-slug>-paper-framework.md`; optional complete translated sibling artifacts only when requested |
| Full Draft | complete `paper/` LaTeX project with `main.tex`, `sections/*.tex`, `references.bib`, and `math_commands.tex` |

## Execution Contract

| Stage | Required output | Hard stop |
|---|---|---|
| Writing Policy | `writing-policies/<paper-slug>-writing-policy.md` | **STOP HERE and wait for user response.** Do not generate Paper Framework until confirmed. |
| Paper Framework | `writing-policies/<paper-slug>-paper-framework.md` | **STOP HERE and wait for user response.** Do not create `paper/` until confirmed. |
| Full Draft | complete `paper/` LaTeX project | Return generated files, unresolved markers, and citation/template/compile risks. |

Mandatory gate behavior:

- A user request for a complete paper draft authorizes the workflow, not automatic passage through
  the gates.
- Do not "compress", "batch", "assume", or "silently satisfy" the Writing Policy or Paper
  Framework confirmation gates.
- After writing the Writing Policy, return only the concise policy summary, stage ledger, and the
  required user action. **STOP HERE and wait for user response.** Do not load paper type, venue,
  domain evidence adapter, section, figure, template, example, or check references until the user
  confirms the Writing Policy.
- After writing the Paper Framework, return only the concise framework summary, stage ledger, and
  the required user action. **STOP HERE and wait for user response.** Do not create `paper/`, draft
  sections, generate figures/tables, or write BibTeX until the user confirms the Paper Framework.

## 1. Intake And Workspace Discovery

Ask only the most blocking question. If the user provides a workspace path, use it. If the
workspace is ambiguous, ask for the paper project workspace.

Minimum discovery targets:

- paper type,
- optional domain evidence adapter, or `none / no matching profile`,
- core contribution and central claim,
- evidence boundary: available results, source evidence, and unsupported claims,
- key terms and naming conflicts,
- source conflicts affecting claims, evidence, terminology, or paper identity.

Optional context, record only when visible:

- target venue, otherwise `generic / venue TBD`,
- existing draft files and progress,
- figures, tables, bibliography, code/data artifacts,
- Image Renderer Preference for picture figures: user-configured `GPT-image2`, user-configured
  `Gemini`, current executing agent, or other explicit renderer,
- style sources or previous papers supplied by the user,
- existing weakness or review notes found in workspace materials.

Inspect compact, high-signal files before large logs or source trees:

- `NARRATIVE_REPORT.md`, `STORY.md`, `PAPER_PLAN.md`, `CLAIMS_FROM_RESULTS.md`
- `EXPERIMENT_LOG.md`, `EXPERIMENT_TRACKER.md`, `findings.md`
- `docs/research_contract.md`, `README.md`, `CLAUDE.md`, `AGENTS.md`
- `paper/`, `sec/`, `sections/`, `*.tex`, `*.bib`
- `results/`, `outputs/`, `figures/`, `tables/`, `logs/`, `configs/`
- JSON, CSV, TSV, Markdown result tables, manifests, metric scripts, baseline configs, and raw
  result or annotation files.

If no usable workspace evidence exists, ask the user for a 3-5 sentence contribution and evidence
summary before writing the Writing Policy. Do not infer a paper story from an empty workspace or
from generic repository metadata.

Do not run environment setup, dependency installation, registry smoke checks, benchmark execution,
or `.venv` creation during Writing Policy generation. Writing Policy may read scripts, configs,
metadata, and existing result files as evidence, but it should not execute experiments or test the
runtime unless the user explicitly asks for execution verification.

## 2. Full Draft Clarification Boundaries

Use the global Clarification Protocol from `static/core/gates.md`. The global protocol decides
whether to ask; this section decides which Full Draft stage owns the question.

Stage boundaries:

| Stage | Ask now only for | Defer or default |
|---|---|---|
| Writing Policy | paper identity, core story, claim/evidence boundary, key terminology, decisive source conflict | venue if unspecified, page budget, section order, figure placement, caption wording, optional ablations |
| Paper Framework | user-required venue-specific planning with missing/contradictory venue, missing official/preloaded template, blocking Writing Policy decision that changes section structure | template choice, page budget, section order, and figure/table plan when the agent can choose conservatively |
| Section Drafting | facts needed to write the section correctly without false claims | weaken the claim, defer the decision, or insert a precise LaTeX marker |

Ask about venue at most once. If unspecified, use `generic / venue TBD` and
`generic_article.tex (non-submission single-column draft template)`.

Ask at most 1-3 questions per round. Normal Writing Policy generation should need at most one round.

Prefer confirm/correct questions over open-ended questions:

```text
Before Writing Policy, I need one decision: should this be treated as a method paper?
I infer method paper from the README and ablation-heavy results. Please confirm or correct.
Default if unanswered: use `method-paper.md` because the evidence strongly supports it; correct this
before Paper Framework if the paper identity is different.
```

## 3. Writing Policy

Load only `references/principles/research-strategy.md`. Do not load venue, paper type, domain
evidence adapter, template, section, figure, style, or check references by default. Only load
`references/checks/claim-evidence.md` if the user explicitly asks for a claim audit or if a
central claim is high-risk.

The Writing Policy is a compact writing contract. Save it to:
`writing-policies/<paper-slug>-writing-policy.md`

File format:

1. **Source Snapshot**: project name, workspace path, files inspected, evidence snapshot date, and
   source traces for facts used in the paper contract.
2. **Paper Identity**: target venue, paper type, paper type profile filename when available,
   optional domain evidence adapter filename or `none / no matching profile`, intended reader, core
   research question, and venue/template constraints if already known.
3. **Core Story**: problem, failure case or motivating gap, technical challenge, insight,
   proposed method/benchmark/system/study, one-sentence contribution, and final takeaway.
4. **Claims And Evidence**: a compact table with `claim`, `evidence`, `status`, `drafting action`,
   and `risk`. The drafting action must say whether to state, weaken, verify, defer, or avoid the
   claim.
5. **Key Terms**: a compact table with `term`, `definition`, `source`, `use policy`, and `status`.
   Include only terms that affect the title, abstract, contribution, method identity, dataset/task,
   benchmark, metric, or system components.
6. **Assets And Constraints**: only visible assets or constraints that affect drafting.
7. **Open Decisions**: only unresolved decisions that can change the paper identity, central claim,
   evidence boundary, key terminology, figure/table plan, or venue/template choice.

Record venue status as one of: `confirmed: <venue>`, `generic / venue TBD`, or `conflict: <options>`.

Paper type must be resolved before confirming the Writing Policy. Use `references/paper-types/index.md`
before defaulting. Do not use `method-paper.md` as a global default.

Writing Policy checkpoint summary must include:

- paper identity: working name, paper type, optional domain evidence adapter, and target venue status,
- research content: core research question, one-sentence contribution, and central claim boundary,
- evidence snapshot: key source-evidence types and what they support,
- experiment/result snapshot: current datasets/tasks/models/metrics/result ranges found,
- top risks: 2-3 claim, evidence, terminology, result, or citation risks,
- decisions to confirm: split into Required and Optional.

Gate: the user must confirm the Writing Policy before Paper Framework generation.

## 4. Paper Framework

The Paper Framework is a concise section-level plan. It is not a paragraph plan and not prose.

Load only the references needed to resolve paper structure and physical format:

- Template selection: `templates/index.md`,
- Venue framework constraints: `references/venues/<venue>.md` when a target venue is confirmed,
- Paper type section/page-budget reference: `references/paper-types/<paper-type>.md`,
- Optional domain evidence adapter: `references/domains/<domain>.md` only when a clear match exists,
- Figure/table planning: `references/figures/figure-planning.md`.

Build the framework in this order:

1. **Venue first**: apply venue constraints as a framework constraint card. If no target venue is
   confirmed, use a generic framework with `generic_article.tex` and a soft 6-8 main-text-page
   drafting budget.
2. **Paper type second**: use the paper type profile as a flexible section/page-budget reference,
   not a fixed template.
3. **Domain evidence adapter third, optional**: when a clear adapter matches, add evidence pressure,
   metrics, baselines, figures/tables, and claim/evaluation risks.
4. **Writing Policy last**: keep only sections and claims supported by available evidence.

File format:

1. **Inputs Used**: Writing Policy path, target venue, selected template, venue format summary,
   page/length budget, paper type, optional domain evidence adapter, evidence snapshot.
2. **Page Budget Summary**: total venue or generic page budget, what counts toward the limit,
   planned main-text total, overflow or compression decisions.
3. **Section Framework**: ordered section list with section name, main content, Page budget, key
   evidence or figure/table, and writing cautions.
4. **Figure Plan**: a short table with `ID`, `type`, `section`, `message`, `source`, and
   `generation route`. Keep only likely main-paper figures and tables.
5. **Venue Assembly Plan**: post-main order, required statements or checklists, optional appendices,
   and `not verified` venue fields.
6. **Open Decisions**: only blocking missing evidence, uncertain section choices, terminology,
   figure/table choices, or user decisions.

For the Figure Plan, load `references/figures/figure-planning.md`. Deciding whether the main paper
needs figures or tables and how they will be generated is part of the framework. Do not generate
figures during framework writing.

Generic fallback: keep the main Figure Plan to 3-5 figures/tables for the generic draft.

Show the framework to the user for confirmation. Use the checkpoint summary shape from
`static/core/gates.md`.

Gate: the user must confirm the Paper Framework before full-draft writing.

## 5. Full Draft LaTeX Project

Use the confirmed Writing Policy, confirmed Paper Framework, relevant section guides,
`references/sections/paragraph-flow.md`, relevant experiment/figure/table materials, and
`references/figures/figure-planning.md` only when figures or tables will be generated.

### LaTeX Project Setup

Default layout:

```text
paper/
  main.tex
  math_commands.tex
  references.bib
  sections/
    0_abstract.tex
    1_introduction.tex
    ...
  figures/
```

Before creating LaTeX files:

1. If `paper/` already exists, back it up to `paper-backup-<timestamp>/`.
2. Copy the selected template from `templates/` into `paper/main.tex`.
3. Copy required companion files (`.sty`, `.cls`, `.bst`).
4. Replace official sample or instruction body text with the confirmed Paper Framework section
   inputs. Preserve the document class, venue options, package/style setup, and bibliography commands.
5. Create `paper/sections/` files matching the confirmed section list.
6. Update `paper/main.tex` input calls to match the confirmed section files.
7. Assemble post-main material according to the Venue Assembly Plan.
8. Remove stale section files not referenced by the updated `paper/main.tex`.

### Figure Handling

1. Read the confirmed Figure Plan from the Paper Framework.
2. Resolve the Image Renderer Preference. If the user configured a picture API (GPT-image2, Gemini),
   use it for picture figures after the Picture Brief. Otherwise the current agent draws the picture.
3. **Data-driven plots**: default to Python, drawn directly by the current agent from workspace
   result files. Load `references/figures/plot-style.md`. Write chart files as
   `paper/figures/<figure-id>.pdf` plus `.png` preview. Do not hardcode results from memory.
4. **Architecture/pipeline/workflow/system diagrams**: use the configured paper-figure MCP for
   FigureSpec skeleton + rendering when available. Keep the source spec in
   `paper/figures/specs/`. If the MCP or renderer is unavailable, the current agent draws the
   diagram directly.
5. **Non-data picture figures** (teasers, conceptual illustrations, polished overview pictures):
   load `references/figures/picture-generation.md`. Always write the Picture Brief to
   `paper/figures/prompts/<figure-id>.md` before any rendering. Generate
   `paper/figures/<figure-id>.png` using the configured API or current-agent fallback.
6. **Screenshots/qualitative examples**: use existing workspace assets and record their source.
7. Insert each figure/table only in the section specified by the confirmed Paper Framework.
8. Captions must state the figure's message and supported claim, not merely describe visual content.

### Section Drafting

Load section references when drafting each section:

| Draft target | Load |
|---|---|
| Abstract | `references/sections/abstract.md`, `references/sections/paragraph-flow.md` |
| Introduction | `references/sections/introduction.md`, `references/sections/paragraph-flow.md` |
| Related Work | `references/sections/related-work.md`, `references/sections/paragraph-flow.md`; load `references/checks/citation-integrity.md` when citation support matters |
| Method / System | `references/sections/method.md`, `references/sections/paragraph-flow.md`; load `references/sections/figures-and-tables.md` when figures are used |
| Experiments / Evaluation | `references/sections/experiments.md`, `references/sections/paragraph-flow.md`; load `references/checks/metric-design.md` and `references/sections/figures-and-tables.md` when needed |
| Demo / Application | `references/sections/demo-application.md`, `references/sections/paragraph-flow.md` |
| Conclusion / Limitations | `references/sections/conclusion.md`, `references/sections/paragraph-flow.md` |
| Final full-paper check | `references/sections/paper-review.md` |

For each section, follow this drafting loop:

1. Read the confirmed Writing Policy, confirmed Paper Framework entry, and relevant source evidence.
2. Load only the current section guide and conditional references.
3. Build an internal Section Plan and Paragraph Plan.
4. Write English LaTeX prose, preserving one paragraph per message.
5. Run reverse outlining and claim-evidence mapping internally; revise before moving to next section.

Do not show internal plans unless the user asks or a blocking risk must be surfaced.

### Citation And Bibliography Rules

- Prefer existing workspace `.bib` files when available.
- Do not generate BibTeX from memory.
- If no verified `.bib` entry is available, use `% CITATION_NEEDED: <short reason>`.
- If citation lookup is allowed and performed, record the source, DOI or URL, and verification status.
- Mark unverified citations as `not verified`.
- Use `\citep{}` / `\citet{}` for natbib venues; use numeric `\cite{}` for IEEE templates.
- Keep `paper/references.bib` limited to entries actually cited.

### Missing-Support Markers

Use only when a claim, citation, figure, table, or result slot is necessary but evidence is missing:

```tex
% EVIDENCE_NEEDED: <short reason>
% CITATION_NEEDED: <short reason>
% FIGURE_NEEDED: <short reason>
% TABLE_NEEDED: <short reason>
```

Prefer weakening or removing unsupported claims when possible. Do not use markers as placeholders
for routine prose. Include remaining markers in the final summary.

### Writing Rules

- Each paragraph has one message.
- The first sentence states the paragraph's function or core information.
- Define terms before using them.
- Claims require evidence; unsupported claims are weakened or marked.
- Methods must not read as ad hoc patches.
- Captions state the message supported by the figure or table.
- Abstract and Introduction claims require extra caution.

### Before Returning

Internally check: paragraph flow, section alignment, figure/table placement, Abstract/Introduction
consistency, Introduction claim support in Experiments, Method and Experiments correspondence,
Related Work positioning, terminology, missing citations, conclusion overclaiming, venue page
counting, post-main section order, required statements/checklists, appendix/supplement handling,
anonymity-sensitive locations, and skeptical reviewer risk.

If `latexmk` or `pdflatex` is available, compile the draft once and report the result. Do not call
the draft submission-ready unless template, citation, evidence, and compilation risks are resolved.

Return a concise interaction-language summary listing generated files and any blocking risks.
