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
| Full Draft | complete `paper/` LaTeX project with `main.tex`, `sections/*.tex`, `references.bib`, and `math_commands.tex`; add `paper/citation-evidence.md` when live citation search is performed |

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
  confirms the Writing Policy. Ask exactly for confirmation or corrections to the Writing Policy
  before moving to Paper Framework.
- After writing the Paper Framework, return only the concise framework summary, stage ledger, and
  the required user action. **STOP HERE and wait for user response.** Do not create `paper/`, draft
  sections, generate figures/tables, or write BibTeX until the user confirms the Paper Framework.
  Ask exactly for confirmation or corrections to the Paper Framework before creating `paper/`.
- If the user asks for autonomous or one-shot full-draft generation, still stop at both gates. Treat
  the request as permission to complete each stage after confirmation, not as permission to skip
  confirmation.

At every stage, keep a brief stage ledger in the user-facing summary: output artifact, decisions
needing confirmation, unresolved paper blockers, and next required user action. Do not make a
checkpoint summary primarily about process mechanics, file existence, line counts, or which folders
were avoided.

Do not create a separate
confirmation file. User approval happens through the conversation checkpoint summary.

## 1. Intake And Workspace Discovery

Ask only the most blocking question. If the user provides a workspace path, use it. If the
workspace is ambiguous, ask for the paper project workspace.

Minimum discovery targets:

- venue kind (`conference` or `journal`; default `conference` unless the user explicitly specifies
  journal),
- paper type,
- optional domain evidence adapter, or `none / no matching profile`,
- core contribution and central claim,
- evidence boundary: available results, source evidence, and unsupported claims,
- key terms and naming conflicts,
- disclosure boundary: internal identifiers that must be renamed for publication (checkpoint /
  training-run / sweep / wandb names, internal tool names, unreleased model names) and entities the
  authors do not want in the paper (withheld baselines or competing methods, internal tools,
  unreleased datasets, partner/product names),
- source conflicts affecting claims, evidence, terminology, or paper identity.

Optional context, record only when visible:

- target venue, otherwise `generic / venue TBD` under `venue_kind=conference`,
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
| Writing Policy | paper identity, core story, claim/evidence boundary, key terminology, disclosure boundary (internal names to rename, entities to withhold) when an exclusion could affect comparison honesty, decisive source conflict | venue kind defaults to conference unless explicit journal; venue if unspecified, page budget, section order, figure placement, caption wording, optional ablations |
| Paper Framework | user-required venue-specific planning with missing/contradictory venue, missing official/preloaded template, blocking Writing Policy decision that changes section structure | template choice, page budget, section order, and figure/table plan when the agent can choose conservatively |
| Section Drafting | facts needed to write the section correctly without false claims | weaken the claim, defer the decision, or insert a precise LaTeX marker |

Ask about venue at most once. If the user does not explicitly specify journal, set
`venue_kind=conference`. If venue is unspecified, use `generic / venue TBD` and
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

Load `references/principles/research-strategy.md`, `references/checks/workspace-logic-audit.md`
(required this stage — it drives the audit sub-step below), and `references/checks/claim-evidence.md`
(the audit uses its strength levels to cap claim wording), plus the paper-type family index needed to
classify the paper (`references/paper-types/index.md` for `venue_kind=conference`, or
`references/paper-types/journal/index.md` for `venue_kind=journal`). Do not load venue cards,
specific paper type profiles, domain evidence adapter profiles, template, section, figure, or style
references by default.

### Workspace Logic And Evidence Audit (run before the Claims table)

After Workspace Discovery and before filling the Claims-And-Evidence table, run the skeptical audit
in `references/checks/workspace-logic-audit.md`. Discovery only collects evidence; this step verifies
that each planned claim survives contact with the raw artifacts. It is a **writing-side audit only**:
it never re-runs, modifies, or redesigns experiments. Every finding resolves into one of four
writing-only actions — downgrade, mark (`needs evidence` / `not verified`), defer to Open Decisions,
or stop-and-ask when the issue is decisive for paper identity, a central claim, key terminology, or
an evidence conflict.

Run the seven checks (trace-to-artifact / cross-file consistency / result-to-conclusion logic /
scope-integrity smells / evidence-type labeling / terminology stability / disclosure-and-naming),
then run the **default-on
independent recheck** (Step D of the audit file): a fresh zero-context subagent receives only the
intended claims and paths to raw result files, and returns per-claim support verdicts. Fold its
findings back into the Claims-And-Evidence table and Open Decisions. Skip the recheck only if the
user opts out or the runtime cannot launch a subagent (then run the fresh self second-pass fallback).

The Writing Policy is a compact writing contract. Save it to:
`writing-policies/<paper-slug>-writing-policy.md`

File format:

1. **Source Snapshot**: project name, workspace path, files inspected, evidence snapshot date, and
   source traces for facts used in the paper contract.
2. **Paper Identity**: venue kind, target venue, paper type, manifest-mapped paper type profile
   path when available, optional domain evidence adapter filename or `none / no matching profile`,
   intended reader, core research question, and venue/template constraints if already known.
3. **Core Story**: problem, failure case or motivating gap, technical challenge, insight,
   proposed method/benchmark/system/study, one-sentence contribution, and final takeaway.
4. **Audit Findings**: the result of the Workspace Logic And Evidence Audit — a compact table with
   `item`, `check`, `verdict (pass/risk/blocking)`, `source trace`, and `writing action`. Include
   the independent recheck's per-claim verdicts here. Keep it short; this section justifies the
   `status` and `risk` values in the Claims-And-Evidence table below.
5. **Claims And Evidence**: a compact table with `claim`, `evidence`, `status`, `drafting action`,
   and `risk`. The drafting action must say whether to state, weaken, verify, defer, or avoid the
   claim. Each row's `status` and `risk` must be consistent with the Audit Findings above.
6. **Key Terms**: a compact table with `term`, `definition`, `source`, `use policy`, and `status`.
   Include only terms that affect the title, abstract, contribution, method identity, dataset/task,
   benchmark, metric, or system components.
7. **Disclosure And Naming**: the publication-boundary registries from contract point 7. Two compact
   tables. **Naming Map** — `internal identifier`, `public display name`, `source trace`; one row per
   internal checkpoint / training-run / sweep / wandb / tool / unreleased-model identifier found in
   the workspace that maps to a public name. **Do-Not-Disclose** — `entity`, `kind` (baseline /
   method / tool / dataset / partner / result), `reason`, `disclosure status`
   (`do-not-disclose` / `restricted`), and for any withheld competing method an
   `integrity check` cell stating whether removing it keeps comparison claims honest (if not, it is
   an `idea-level risk` → Open Decisions / stop-and-ask, not a silent removal). Leave a table empty
   only after actively checking the workspace; record `none found` rather than omitting it. After the
   user confirms the Writing Policy, export both tables to `paper/.disclosure.yaml` (the format the
   `scripts/audit_draft.py` disclosure check reads — see that script's header) so the static gate can
   enforce them mechanically.
8. **Assets And Constraints**: only visible assets or constraints that affect drafting.
9. **Open Decisions**: only unresolved decisions that can change the paper identity, central claim,
   evidence boundary, key terminology, disclosure/naming boundary, figure/table plan, or
   venue/template choice.

Do not add a short translated confirmation summary inside the Writing Policy. If the user requested
another language version before this stage was generated, create a complete same-content translated
sibling artifact instead.

Record venue kind as one of: `conference` or `journal`. If the user has not explicitly specified a
journal target, use `conference`.

Record venue status as one of: `confirmed: <venue>`, `generic / venue TBD`, `journal-generic /
target journal TBD`, or `conflict: <options>`.

Paper type must be resolved after venue kind and before confirming the Writing Policy. Use
`references/paper-types/index.md` for conference papers and `references/paper-types/journal/index.md`
for journal papers before defaulting. Do not use `method-paper.md` or `journal-method` as a global
default.

The domain evidence adapter is an optional evidence adapter. Do not force a domain adapter match. If
there is no clear match, record `domain evidence adapter = none / no matching profile` and continue.

Writing Policy checkpoint summary must include:

- paper identity: working name, venue kind, paper type, optional domain evidence adapter, and target
  venue status,
- research content: core research question, one-sentence contribution, and central claim boundary,
- evidence snapshot: key source-evidence types and what they support,
- experiment/result snapshot: current datasets/tasks/models/metrics/result ranges found,
- audit snapshot: the Workspace Logic And Evidence Audit verdict — any `blocking`/`risk` findings
  (phantom claims, cross-file conflicts, result-to-conclusion gaps, scope/integrity smells), the
  independent recheck outcome, and how each was resolved (downgraded / marked / deferred /
  stop-and-ask),
- disclosure snapshot: how many internal identifiers are mapped to public names, how many entities
  are marked do-not-disclose, and whether any withheld comparison was flagged as an integrity risk,
- top risks: 2-3 claim, evidence, terminology, result, disclosure, or citation risks,
- decisions to confirm: split into Required and Optional.

**Compliance Self-Check (Writing Policy) — complete before showing the checkpoint.** Answer each
item yes/no internally; **any "no" means this stage is not complete — fix it before stopping at the
gate.** Do not skip a field by leaving it blank.

1. Are all six contract points (`static/core/contract.md`) resolved or explicitly listed in Open
   Decisions — none silently guessed?
2. Is venue kind resolved first (`conference` unless explicit journal), and is the paper type
   resolved against the correct family index (not defaulted to method-paper or journal-method), and
   recorded with its manifest-mapped profile path?
3. Did I run the Workspace Logic And Evidence Audit (all seven checks) and record the results in the
   Audit Findings section, with every `blocking`/`risk` finding resolved into downgrade / mark /
   defer / stop-and-ask — and no claim left untraceable to a real artifact?
4. Did I run the independent zero-context recheck (or the fresh self second-pass fallback, or note
   an explicit user opt-out), and fold its per-claim verdicts into the table?
5. Does every claim in the Claims-And-Evidence table have a `status` and a `drafting action`, and is
   each `status`/`risk` consistent with the Audit Findings (no wording exceeding its evidence
   ceiling)?
6. Are all checkpoint-summary fields above filled (no empty field), including the audit snapshot and
   the disclosure snapshot?
7. Did I build the Disclosure And Naming registries (Naming Map + Do-Not-Disclose, each `none found`
   or populated after actually checking the workspace), confirm no internal identifier or
   do-not-disclose entity leaked into the Claims-And-Evidence or Key Terms tables, and flag any
   withheld comparison that would make a claim misleading as an `idea-level risk` / Open Decision?
8. Did I avoid loading downstream references (venue, section, figure, template) not allowed at this
   stage?

Gate: the user must confirm the Writing Policy before Paper Framework generation.

## 4. Paper Framework

The Paper Framework is a concise section-level plan. It is not a paragraph plan and not prose.

#### Profile Structure Adherence (the profile is a hard default)

The resolved manifest-mapped paper type profile path defines the **default
section list, order, naming, and count**. Treat it as binding by default, not as loose inspiration.

- **Default = reproduce the profile's structure.** Match its section list, order, names, and section
  count. Do not split one profile section into two, add a section the profile does not list (e.g., a
  standalone Discussion), merge sections, rename, or reorder **for convenience**.
- **Deviation is allowed only when necessary** — when the actual contribution, evidence, venue
  requirement, or explicit user request genuinely cannot fit the profile structure. A deviation that
  is merely "cleaner" or "more standard" does not qualify.
- **Every deviation must be surfaced and approved.** At the Paper Framework checkpoint, show the
  profile's canonical section list next to the adopted section list, and give a one-line reason for
  **each** split / merge / rename / addition / reorder. Do not apply a structural deviation silently;
  the user must be able to see and approve it before `paper/` is created. If the structure matches the
  profile, state "matches profile" explicitly.

#### Subsection Granularity (avoid over-fragmentation)

Plan and present the framework at **section level**. Within-section structure is content blocks and
paragraph roles, not a numbered table of contents.

- **Do not pre-commit a deep numbered subsection breakdown** (e.g., §3.1–§3.6, §4.1–§4.6) in the
  framework. Listing every step as its own subsection fragments a section into thin pieces and reads
  like an outline dump.
- **Subsections are expected where a section is genuinely large; they are not banned.** Short
  sections (Abstract, Introduction, Related Work, Conclusion) normally use **0 subsections** and run
  as flowing prose. Large sections (Method, Benchmark/Dataset Construction, Experiments) normally use
  **2–4 subsections**.
- Promote a content block to an actual `\subsection` only when it spans multiple paragraphs or owns a
  distinct figure, table, protocol, or formal result that needs its own heading. A block that is only
  one paragraph long should stay a paragraph (optionally a `\paragraph{}` run-in or a `\textbf{}`
  lead-in), not become a subsection.
- **Subsection budget:** **0 for short sections, at most 2–4 for any one main section. Five or more
  subsections in one section is a smell** — merge related steps into one subsection, demote
  single-paragraph items to paragraphs, or move fine-grained detail to the appendix.
- In the checkpoint **Main Content** cell, describe each section as a short phrase or a few content
  blocks (e.g., "construction pipeline, quality control, coverage comparison"), **not** an enumerated
  `3.1 … 3.2 … 3.3 …` subsection list.

Load only the references needed to resolve paper structure and physical format:

- Template selection: `templates/index.md`,
- Venue framework constraints: `references/venues/<venue>.md` when a target venue is confirmed,
- Paper type section/page-budget reference: the manifest-mapped paper type profile path,
- Figure/table planning: `references/figures/figure-planning.md`,
- Journal-only (when `venue_kind=journal`): `references/venues/journal-vs-conference.md` for drafting
  posture, and `references/checks/journal-submission-elements.md` for the mandatory statements and
  display-item caps/tiers that shape the Venue Assembly Plan and the Figure Plan.

**Template Acquisition (local-first — do not web-fetch when a preloaded template exists).** The
official templates for the major venues are bundled in `templates/`. Acquire the template in this
strict priority order, stopping at the first that applies:

1. **Preloaded `templates/`** — when the target venue maps to a bundled template in
   `templates/index.md`, copy that local file. This is the **first and authoritative** source.
2. **User-provided official template** — when the user supplied template files for this project,
   use those.
3. **Targeted official-source fetch — last resort only** — *only* when the venue has **no** preloaded
   mapping **and** the user provided no template. Use the official URL recorded in the venue card /
   `maintenance/venue-template-sources.md`, and record it as a Paper Framework template risk.

**Do NOT search the web or download a template when `templates/index.md` maps the target venue to a
preloaded file** — that is the failure mode this rule exists to prevent. The official-source URLs in
venue cards and in `maintenance/venue-template-sources.md` are **provenance records (how the bundled
assets were obtained), not draft-time fetch instructions**. The venue card's "verify the current
official style file before submission" is a *pre-submission* check against the official page, not a
license to re-download the template during drafting. Never reconstruct venue formatting from memory.

Build the framework in this order:

1. **Venue first**: apply venue constraints as a framework constraint card. If no target venue is
   confirmed, use a generic framework with `generic_article.tex` and a soft 6-8 main-text-page
   drafting budget.
2. **Paper type second — the profile section list is a HARD DEFAULT, not inspiration.** Use the
   paper type profile's candidate sections, order, and naming **as the structure**. Reproduce its
   section count and granularity unless an adaptation is genuinely required (see Profile Structure
   Adherence below). Do not silently split, merge, rename, add, or reorder sections, and do not
   inflate the profile's section count for convenience.
3. **Domain evidence adapter third, optional**: when a clear adapter matches, add evidence pressure,
   metrics, baselines, figures/tables, and claim/evaluation risks.
4. **Writing Policy last**: keep only sections and claims supported by available evidence.

Page-budget arithmetic must be explicit. Start with the venue or generic total budget, subtract
fixed front/back matter only when it counts toward the limit, assign a `Page budget` to each planned
section, and ensure the total planned pages must not exceed the venue limit or generic drafting
budget. If the draft would overflow, compress or move lower-priority material to appendix before
creating `paper/`.

File format:

1. **Inputs Used**: Writing Policy path, target venue, selected template, venue format summary,
   page/length budget, paper type, optional domain evidence adapter, evidence snapshot.
2. **Page Budget Summary**: total venue or generic page budget, what counts toward the limit,
   planned main-text total, overflow or compression decisions.
3. **Section Framework**: ordered section list with section name, main content, Page budget, key
   evidence or figure/table, and writing cautions. Keep this at section level. List subsections only
   when a section genuinely needs them, and respect the Subsection Granularity budget (0, or at most
   2–4 per section); do not enumerate every paragraph as a numbered subsection.
4. **Figure Plan**: a short table with `ID`, `type`, `layout`, `section`, `message`, `source`, and
   `generation route`. Keep only likely main-paper figures and tables. The `layout` value must be
   `single-column`, `double-column`, `appendix`, or `supplement`.
5. **Venue Assembly Plan**: post-main order, required statements or checklists, optional appendices,
   and `not verified` venue fields. Record that the appendix begins on a fresh page (`\clearpage`
   before `\appendix`).
6. **Open Decisions**: only blocking missing evidence, uncertain section choices, terminology,
   figure/table choices, or user decisions.

For the Figure Plan, load `references/figures/figure-planning.md`. Deciding whether the main paper
needs figures or tables, their layout target, and how they will be generated is part of the
framework. Do not generate figures or tables during framework writing.

Generic fallback: keep the main Figure Plan to 3-5 figures/tables for the generic draft.

Optional translated output files, only when requested before generation:

```text
writing-policies/<paper-slug>-paper-framework.<language-code>.md
```

Show the framework to the user for confirmation using this exact format. Do not use a
generic dimension/content table or any other format.
```text
Checkpoint: Paper Framework
Stage result: <one sentence>
Output: <framework artifact path>

Paper Title: <confirmed working name / title from Writing Policy>

Section Plan:

| # | Section | Main Content |
|---:|---|---|
| 1 | Abstract | <main content, one sentence> |
| 2 | Introduction | <main content, one sentence> |
| ... | ... | ... |

Keep `Main Content` as a one-sentence phrase or a few content blocks. Do not list a numbered
subsection breakdown (no `3.1 … 3.6`) here; subsections, if any, follow the Subsection Granularity
budget and are decided at drafting time.

Figure Plan:

| ID | Type | Layout | Section | Message |
|---|---|---|---|---|
| Fig. 1 | <teaser/pipeline/bar/...> | <single-column/double-column> | Introduction | <what the figure shows> |
| Tab. 1 | <taxonomy/result/...> | <single-column/double-column/supplement> | Method | <what the table shows> |
| ... | ... | ... | ... | ... |

Display-Item Page Budget:

| ID | Main-paper placement | Estimated page cost | Compression fallback |
|---|---|---:|---|
| Fig. 1 | <single-column/double-column/supplement> | <0.25/0.5/1.0 page> | <shrink / merge / move to appendix> |
| Tab. 1 | <single-column/double-column/supplement> | <0.25/0.5/1.0 page> | <compress columns / move full version to appendix> |

Structure vs paper-type profile:
- Profile: <paper-type name> → <canonical section list from the profile, in order>
- Adopted: <the section list above, in order>
- Deviations: <"matches profile", OR one line per split / merge / rename / addition / reorder with its reason>

Decisions to confirm:
- Required: <section order / prose page budget / display-item page budget / venue assembly>
- Structure basis: <which paper type drove the structure; if any deviation is listed above, why it is necessary and not just "cleaner">
- Optional: <template / language variant defaults>
Unresolved blockers: <none or concise list>
User action required: Please confirm whether to proceed to paper/, or what to change. If any structural deviation is listed, confirm it explicitly before paper/ is created.
```

Do not output a separate `Content snapshot` bullet list.

**Compliance Self-Check (Paper Framework) — complete before showing the checkpoint.** Answer each
item yes/no internally; **any "no" means this stage is not complete — fix it before stopping at the
gate.**

1. Does the adopted section list match the paper-type profile, OR is every split / merge / rename /
   addition / reorder listed with a necessity reason in the "Structure vs paper-type profile" block?
   (A deviation that is only "cleaner" is not allowed.)
2. Is the `Main Content` cell free of numbered subsection dumps (no `3.1 … 3.6`), and is each
   section's planned subsection count within budget (0 for short sections, ≤4 for main sections)?
3. Is the page-budget arithmetic shown explicitly and within the venue/generic limit, including both
   prose and display-item page cost?
4. Does the Figure Plan declare a `layout` for every figure/table, does the Display-Item Page Budget
   estimate each item's main-paper page cost, and does each item map to a confirmed section?
5. For a strict page-limited conference venue, does the plan leave a practical compression margin
   rather than spending the whole limit on planned prose and floats?
6. Are all checkpoint fields filled, including the "Structure vs paper-type profile" comparison?

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
    abstract.tex
    introduction.tex
    ...
  figures/
```

Before creating LaTeX files:

1. If `paper/` already exists, back it up to `paper-backup-<timestamp>/`.
2. Copy the selected template from `templates/` into `paper/main.tex`.
3. Copy required companion files (`.sty`, `.cls`, `.bst`).
4. Replace official sample or instruction body text with the confirmed Paper Framework section
   inputs. Preserve the document class, venue options, package/style setup, and bibliography commands.
5. If the confirmed Figure Plan contains any nontrivial table, add the portable table toolbox to
   the generated preamble unless it is already present or the venue explicitly forbids it.
   `booktabs` is **required** whenever any table exists — without it the draft falls back to ugly
   `\hline` rules:

   ```tex
   \usepackage{booktabs}      % \toprule \midrule \bottomrule \cmidrule — REQUIRED for any table
   \usepackage{array}
   \usepackage{tabularx}
   \usepackage{colortbl,xcolor} % subtle highlight of best/target numbers
   \newcolumntype{Y}{>{\raggedright\arraybackslash}X}
   \newcolumntype{Z}{>{\centering\arraybackslash}X}
   ```

   Keep this as a generated-project support block; do not rewrite official source template files
   themselves just to add helper packages.
6. Create `paper/sections/` files matching the confirmed section list.
7. Update `paper/main.tex` input calls to match the confirmed section files.
8. Assemble post-main material according to the Venue Assembly Plan. **Start the appendix on a fresh
   page**: place `\clearpage` immediately before `\appendix` (most venues, including ACL, do not do
   this automatically). Keep the venue's required order for Limitations / Ethics / References /
   Appendix, and do not let the appendix run on the same page as the references or main body.
9. Remove stale section files not referenced by the updated `paper/main.tex`.

### Figure Handling

**Before any data chart:** load `references/figures/plot-style.md` and apply its
rcParams (mandatory for matplotlib data charts — bars, lines, heatmaps, radar).
Without rcParams, charts have wrong fonts, low resolution, and unreadable text.
Also load `references/figures/chart-patterns.md` for reusable code patterns and
apply its semantic color roles and legend rules.

**Before any concept figure (teaser / pipeline / architecture / workflow):** load
`references/figures/picture-generation.md`. These are **illustrations**, not
matplotlib boxes: the image API draws the scene and may render the short labels
directly, which are then **verified for correct spelling and terminology**
(generate-then-verify); the TikZ overlay is a fallback for a label the model
misspells. Do **not** hand-draw pipeline boxes in matplotlib.

1. Read the confirmed Figure Plan from the Paper Framework.
2. Resolve the Image Renderer Preference. If the user configured a picture API (GPT-image2, Gemini),
   use it for picture figures after the Picture Brief. Otherwise the current executing agent draws
   the picture from the brief.
3. **Data-driven plots**: default to Python, drawn directly by the current agent from workspace
   result files; data-driven plots default to Python. Write chart files as
   `paper/figures/<figure-id>.pdf` plus `paper/figures/<figure-id>.png` preview.
   Do not create shared style modules, scripts directories, derived data folders, or audit files by default.
   Do not hardcode results from memory.
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
7. Insert each figure/table only in the section specified by the confirmed Paper Framework.
8. After all figures pass the gate, confirm the unified visual family (one palette, one type system,
   consistent encodings) and collect inclusion blocks into `paper/figures/latex_includes.tex`.
9. Captions must state the figure's message and supported claim, not merely describe visual content.

### Table Handling

1. Read every table entry from the confirmed Figure Plan, including its `Layout` value.
2. **Always use `booktabs` rules** (`\toprule`, `\midrule`, `\bottomrule`, `\cmidrule`). Never use
   `\hline`, never use vertical rules (`|`), and never stack repeated `\hline`. A table built from
   `\hline` is a hard defect — rebuild it with booktabs.
3. **Column span follows content width, not importance.** Default to single-column `table`
   (`\columnwidth`). Use cross-column `table*` (`\textwidth`) only when the content genuinely needs
   the room: the headline/main results table, a wide model×metric matrix, any table with ≳5–6 numeric
   columns, or a table whose cells become unreadable in one column. The main results table is
   *usually* such a case, so it is *usually* cross-column — but check its actual column count instead
   of promoting reflexively. **Taxonomy / definition / example tables with a couple of columns stay
   single-column**; a prose cell wrapping to 2–3 lines is normal there and is **not** a reason to go
   cross-column.
3b. **A `table*` must fill `\textwidth`, not float narrow.** Span the full width with
   `\begin{tabular*}{\textwidth}{@{\extracolsep{\fill}}...}` for numeric tables (no wrapping) or
   `\begin{tabularx}{\textwidth}{...}` when cells wrap. A double-column table that occupies only the
   middle third of the span is a defect — either widen it, or (if its content cannot fill the width)
   move it back to single-column.
3c. **Size columns to content and keep cells on one line where the content reasonably allows.**
   Short/categorical columns narrow, long-text columns wide; do not give every column equal `Y`
   width. Reduce `\tabcolsep` and right-size columns before considering any width change; only widen a
   prose-heavy single-column table to `table*` if it *also* meets the cross-column test in rule 3 —
   otherwise abbreviate cell text instead.
3d. **Never let a table overflow — body or appendix.** A table wider than its container is a hard
   defect (it spills into the margin / neighbouring column and overlaps text). **Appendix tables obey
   the same rule** — do not paste a wide numeric matrix into a single-column `table`. Escalate:
   (i) exceeds `\columnwidth` but fits `\textwidth` → `table*` filling `\textwidth`; (ii) still exceeds
   `\textwidth` → rotate (`sidewaystable`/`\rotatebox`), split by column groups, or transpose;
   (iii) only then apply `\small`/`\footnotesize`/`\resizebox` as a last touch for short-cell numeric
   tables. A numeric table with ≳6 columns or long header labels (e.g. full model names) defaults to
   `table*`; ≳10 columns usually needs rotation or splitting even at full width.
4. Use `single-column` `table` only when the full table fits within `\linewidth` / `\columnwidth`.
5. **Column types must match cell content.** Use `r` (or `c`, or `siunitx` `S` for decimal
   alignment) for numeric columns — never stretch numbers with `tabularx` `Y`/`Z`, which left-rags
   and unevenly spaces them. Reserve `tabularx` `Y`/`Z` columns for long labels, example text,
   taxonomy descriptions, qualitative cases, and prose-heavy cells only. A numeric results table
   normally needs no `tabularx` at all: `\begin{tabular}{l rrrrr}` with booktabs is correct.
6. Mark metric direction in headers (`ASR ↑`, `LPIPS ↓`) and **bold** the best (or target) value per
   column. For "baselines vs. ours" tables, put your method in the last row below a `\midrule`. Color
   is optional and must stay redundant with bolding: at most a single light `\rowcolor`/`\cellcolor`
   (pale gray/blue) on the "ours" row or best cell, readable in grayscale; never saturated or
   multi-hue. When unsure of venue norms, use bolding alone.
7. Use fixed `p{...}` columns only when the widths are expressed as fractions of `\linewidth` or
   `\textwidth`; avoid absolute widths that can exceed a venue column.
8. Use `\resizebox{\linewidth}{!}{...}` only for compact numeric tables with short labels and only
   after checking that the rendered text remains readable; never as the primary fix for a too-wide
   table — promote it to `table*` first.
9. Split the table or move the complete version to supplementary material when neither single-column
   nor double-column layout is readable.
10. After compiling, inspect **every** PDF page containing a figure or table — **body, appendix, and
    supplementary alike**. If any item crosses a margin, overlaps another column, has clipped
    labels/columns, uses `\hline`, or becomes unreadable, treat it as a **blocking** defect: apply the
    overflow ladder in rule 3d (table* → rotate/split → resize), revise, and recompile before
    returning the draft. A compile-log overfull `\hbox` whose source is a `tabular` is this defect —
    do not dismiss it as cosmetic.
11. **Design the appendix against the opposite defect — sparseness, not overflow.** Once the page
    budget is gone, the failure mode flips: short floats scatter across half-empty pages and each
    appendix section becomes a one-line pointer (`Table~N provides ...`) plus a bare float ("太空").
    On the same inspection pass, treat a half-empty / table-dump appendix page as a defect to fix.
    (a) **Do not reflexively widen** — appendix definition / config / boundary / example tables that
    fit one column stay single-column `table` and pack tight; apply the same single-vs-cross-column
    test as the body. (b) **Anchor every appendix (sub)section with a real lead paragraph** (2–4
    sentences: what it is, how to read it, the pattern worth noticing, which main claim it backs), not
    a pointer. (c) **Pin float placement** with `[h]`/`[ht]` (or `[H]` via the `float` package) and a
    `\FloatBarrier` (`placeins`) or deliberate `\clearpage` between appendix sections so floats sit
    under their heading instead of drifting and leaving white bands; never pad with blank `\vspace`.
    (d) **Carry the full version, never a stub** — no `see supplementary material` placeholder in
    place of content that exists, and no sketch-only appendix. See `references/sections/figures-and-tables.md`
    ("The appendix has the opposite failure") for the substantive-material menu and float discipline.

### Section Drafting

Load section references when drafting each section:

| Draft target | Load |
|---|---|
| Abstract | `references/sections/abstract.md`, `references/sections/paragraph-flow.md` |
| Introduction | `references/sections/introduction.md`, `references/sections/paragraph-flow.md` |
| Related Work | `references/sections/related-work.md`, `references/sections/paragraph-flow.md`; load `references/checks/citation-integrity.md` when citation support matters |
| Method / System | `references/sections/method.md`, `references/sections/paragraph-flow.md`; load `references/sections/figures-and-tables.md` when figures or tables are used |
| Experiments / Evaluation | `references/sections/experiments.md`, `references/sections/paragraph-flow.md`; load `references/checks/metric-design.md` and `references/sections/figures-and-tables.md` when figures or tables are used |
| Demo / Application | `references/sections/demo-application.md`, `references/sections/paragraph-flow.md` |
| Conclusion / Limitations | `references/sections/conclusion.md`, `references/sections/paragraph-flow.md` |
| Draft completion review | `references/sections/paper-review.md`; automatic immediately after the first complete `paper/` draft exists |
| Final submission-readiness check | `references/checks/submission-readiness.md` after the complete `paper/` draft exists; also `references/checks/journal-submission-elements.md` when `venue_kind=journal` |

**Journal section overlays (only when `venue_kind=journal`).** After loading each base section guide
above, also load the matching overlay and apply it on top of the base (it states only the journal
deltas; see `references/sections/journal/index.md`):

| Draft target | Base guide | Journal overlay to layer on top |
|---|---|---|
| Abstract | `references/sections/abstract.md` | `references/sections/journal/abstract.md` |
| Introduction | `references/sections/introduction.md` | `references/sections/journal/introduction.md` |
| Method / System | `references/sections/method.md` | `references/sections/journal/method.md` |
| Conclusion / Discussion | `references/sections/conclusion.md` | `references/sections/journal/discussion.md` |

Sections without an overlay (Related Work, Experiments, Demo/Application) use the base guide alone.
When `venue_kind=conference`, do **not** load any file under `references/sections/journal/`.

Load a local example only when the section guide explicitly points to one, the section structure is
uncertain, or the user asks to learn from examples. Learn structure, not phrasing.

For each section, follow this drafting loop:

1. Read the confirmed Writing Policy, confirmed Paper Framework entry, and relevant source evidence.
2. Load only the current section guide and conditional references.
3. Build an internal Section Plan and Paragraph Plan.
4. Write English LaTeX prose, preserving one paragraph per message. Apply
   `references/style/copyediting-standard.md`: formal register, no contractions, no
   possessive `'s` on method/model/system names, simple and clear vocabulary, common
   abbreviations kept unexpanded, LaTeX commands preserved, and no list-ification of prose.
   **Bold the work's own name (`\textbf{Name}`) at its first mention in the Abstract and in the
   Introduction; thereafter plain text with stable capitalization. Do not wrap names in `\textsc{}`.**
   **Apply Salience And Compression (`references/sections/paragraph-flow.md`): lead each paragraph
   and subsection with its point (never bury it); allocate length by importance; and do not
   enumerate taxonomies/inventories/per-category counts in the body — mention them in one stroke
   (dimension, total, salient/novel members) and move the full list to a table or appendix.**
5. Run reverse outlining and claim-evidence mapping internally; revise before moving to next section.
6. **Section-Method Adherence check (mandatory, internal).** Before moving on, verify the section
   against the *required moves* of its section guide and mark each `present` / `missing`. A `missing`
   move means the section is not done — revise until resolved or record it as an explicit risk.
   Minimum required moves per section:
   - **Method** (`references/sections/method.md`): every module subsection has motivation, design,
     and technical advantage; an overview/section-map opens the section; terms defined before use.
   - **Experiments** (`references/sections/experiments.md`): setup (datasets/metrics/baselines/
     protocol) stated; each contribution claim has a matching experiment; metric direction and scope
     explicit.
   - **Introduction / Abstract**: problem → gap → contribution chain present; central claims map to
     available evidence; contributions preview maps to later sections.
   - **Related Work**: organized by topic group with a stated distinction per group, not a citation
     list.
   - **All sections**: one paragraph one message; first sentence states the paragraph role and
     leads with the point (not buried); stable terminology; **no taxonomy/inventory/per-category
     enumeration in the body** — such lists are mentioned in one stroke and the full list lives in a
     table or appendix; every prose number supports a claim rather than transcribing a table.

   Keep this check internal. Round 2 of the Post-Draft Review Gate (the independent subagent) must
   independently re-verify these same required moves against the section guides — it is the external
   check that the self-assessment was honest.

**Non-negotiables while drafting (these hold here, not only in the rules file):** no `\footnote{}`;
no `\texttt{*.json/*.py/*.csv}` or code identifiers or local paths in prose; subsection budget (0 for
short sections, ≤4 per main section); do not add sections/subsections beyond the confirmed Framework;
**no body-text enumeration of a taxonomy/inventory/per-category counts (each `V1…Vn` / `H1…Hn` /
per-app count on its own line) — compress to one stroke in the body and move the full list to a
table or appendix; lead every paragraph with its point.**

**During drafting, do not use `\footnote{...}` anywhere.** Move footnote content into the main
body, convert it to inline parenthetical text, or delete it. **Do not write file names, script
names, or code identifiers (`\texttt{*.json}`, `\texttt{*.py}`, `\texttt{*.csv}`) in prose.**
Replace with descriptive natural language. **Do not include local paths or directory names.**

**Apply the Disclosure And Naming registries (Writing Policy section 7) to every section, caption,
table, and figure.** For every entity in the Naming Map, write only the public display name; the
internal identifier (checkpoint / training-run / sweep / wandb / tool / unreleased-model name, e.g.
a `..._step380` tag) MUST NOT appear anywhere — not in prose, captions, table cells, figure labels,
or comments meant to ship. For every entity on the Do-Not-Disclose list, write nothing that names or
points at it: not a positive mention, not a passing reference, and **not a negation or exclusion**
(do not write "the protocol that excludes X", "unlike X", or "we do not compare against X"). When a
comparison or protocol sentence would otherwise have named a withheld entity, describe the scope on
its own terms ("against the strongest publicly comparable baselines"), without implying a complete
comparison and without fabricating a result. If suppressing a withheld competing method would make a
comparison claim misleading, do not write the flattering claim — surface it as an `idea-level risk`
per contract point 7.

Do not show internal section plans, paragraph plans, or claim-evidence maps unless the user asks or
a blocking risk must be surfaced.

### Citation Search Trigger

Do not run a broad literature search by default. Trigger targeted citation search only when the
draft needs external support that is not already available in workspace evidence or verified `.bib`
entries:

- Related Work drafting requires prior methods, benchmarks, datasets, or comparison lines.
- Introduction background or gap claims depend on external literature.
- A confirmed Paper Framework names prior work that is missing from local sources.
- A necessary sentence would otherwise require `% CITATION_NEEDED`.
- The user explicitly asks to find, add, or verify references.

When triggered, load `references/checks/citation-integrity.md`. Search before writing a final
citation; run targeted live lookup. If live search adds or changes a citation, record the
source and support judgment in `paper/citation-evidence.md`. If reliable support is not found,
weaken/remove the claim or leave `% CITATION_NEEDED: <short reason>` rather than inventing a source.

### Citation And Bibliography Rules

**Every cited source must be verified, complete, and traceable.** A draft with placeholder
authors, missing identifiers, or unverified entries is not complete. The citation audit
(`scripts/audit_citations.py`) enforces these rules mechanically — it must pass before the
draft leaves the agent's hands.

- Prefer existing workspace `.bib` files when available.
- Do not generate BibTeX from memory. Every entry must come from a trusted source (DBLP,
  CrossRef, Semantic Scholar, arXiv, publisher page) or from the user's verified `.bib`.
- **Complete author lists required.** Every BibTeX entry must list all authors by name.
  Never use `and others`, `et al.`, or similar placeholders in the `author` field. If
  the full author list is unavailable, mark the entry `% [VERIFY]` and do not cite it
  as verified.
- **Stable identifier required** for every entry published after 2000. At minimum: DOI,
  URL, or arXiv `eprint`. Conference papers without at least an arXiv link are not
  verified. An entry labeled `arXiv preprint arXiv:2025` (year substituted for ID) is
  malformed — fix or replace it.
- **Year consistency.** The citation key year (e.g., `smith2024`) must match the `year`
  field. Mismatched keys mean the entry was fabricated or botched — fix or replace.
- If no verified `.bib` entry is available, use `% CITATION_NEEDED: <short reason>`.
- If citation lookup is performed, record the source, DOI/URL, and verification status
  in `paper/citation-evidence.md`.
- Mark unverified citations as `not verified`.
- Use `\citep{}` / `\citet{}` for natbib venues; use numeric `\cite{}` for IEEE templates.
- Keep `paper/references.bib` limited to entries actually cited. Remove uncited entries.

**If any entry in `references.bib` violates these rules, the citation audit will fail.
Fix every error before returning the draft — the audit is a BLOCKING gate, not a
diagnostic.**

### Draft Completion Review Gate

This gate starts as soon as the first complete `paper/` draft exists: `main.tex`, all planned
`sections/*.tex`, intended figures/tables, `references.bib`, and post-main material are assembled.
Load `references/sections/paper-review.md` immediately at this point. Do not wait for the user to ask for review.
Do not ask whether to run review, and do not return the just-written draft before this
gate completes. The first draft returned to the user is the reviewed-and-revised draft.

Run the two-round Post-Draft Review Loop from `references/sections/paper-review.md` automatically:

- **Round 1 (self-review):** read the LaTeX source and compiled PDF when available, run a skeptical
  defect-finding pass over the eight dimensions (including internal consistency — front-to-back data
  and claim agreement), and fix every `blocking` finding and every feasible
  `high` finding within writing-only scope. Recompile after review-driven edits when compile tools
  are available.
- **Round 2 (independent subagent review):** after Round 1 fixes and recompile, launch a reviewer
  subagent in a fresh, isolated context per the Reviewer Independence rules in `paper-review.md`.
  Pass only the reviewer role, venue/format constraints, review dimensions, relevant section guides
  as neutral required-move rubrics, and paths to the current `paper/` LaTeX source and compiled PDF.
  Do not pass section plans, paragraph plans, Round 1 findings, fix summaries, or author framing.
  The reviewer returns findings only; the writing agent fixes every `blocking` finding and every
  feasible `high` finding within writing-only scope, then recompiles when tools are available.

Skip Round 2 only if the user explicitly opts out. If the runtime cannot launch a subagent, run Round
2 as the fresh self second-pass fallback described in `paper-review.md`.

After this gate, continue to the Final Static Audits and Final Submission Readiness Gate. If review
edits create citation, format, page-budget, layout, or compile changes, the later audits judge the
reviewed-and-revised draft, not the pre-review draft.

Return only a concise Paper Review Report summary in the terminal or conversation when the user asks
for a review, when review is the primary task, or when material risks remain. Do not print the full
review table or full defect list in the terminal unless the user explicitly asks for it. Write
`paper/review-report.md` only in those same cases; do not create it for a routine clean internal
review.

### Final Static Audits — BLOCKING GATE

**This gate is not optional. Skipping it, running it and ignoring failures, or returning
a draft before the audits pass is a workflow violation. The agent MUST run both scripts and
the output of both MUST be `PASS`.**

Before returning a complete `paper/` draft, run both audits. Resolve the skill checkout
path from this file's location (the script directory is alongside `static/workflow/`):

```bash
SKILL_DIR="$(dirname "$(dirname "$(dirname "$(readlink -f "$0" 2>/dev/null || echo "$0")")")")"
python3 "$SKILL_DIR/scripts/audit_citations.py" paper
python3 "$SKILL_DIR/scripts/audit_draft.py" paper
```

If drafting in another project (paper is not in CWD), pass the absolute path to that
project's `paper/` directory.

For any venue with a content page limit, also check the compiled-PDF page budget:

```bash
python3 "$SKILL_DIR/scripts/audit_draft.py" paper --max-content-pages <limit>
```

**How to handle audit failures:**

- `audit_citations.py` reports errors → **fix every error in `references.bib`** (missing
  authors, placeholder `and others`, missing DOI/URL/arXiv, year-key mismatch, malformed
  entries, uncited entries). Then **re-run the audit**. Repeat until `PASS`.
- `audit_draft.py` reports errors → **fix every error in the LaTeX source** (footnotes,
  file/code artifacts, leftover `% *_NEEDED` markers, duplicate labels, overfull pages, and
  disclosure leaks — internal identifiers that should use a display name, or do-not-disclose
  entities that appear in prose). For a disclosure leak, apply the Naming Map (rename to the public
  display name) or remove the do-not-disclose mention (including any negation/exclusion phrasing);
  do not edit `paper/.disclosure.yaml` to silence a true leak. Then **re-run the audit**. Repeat
  until `PASS`.
- **Do not return the draft while any audit reports errors.** A draft with audit failures
  is incomplete. Fix, re-run, pass, then return.
- Paste the audit result lines into the internal check log so the user can verify.

**What each script checks:**
- `audit_citations.py`: bibliography integrity — placeholder authors, missing required
  BibTeX fields, missing DOI/URL/arXiv on modern entries, vague source labels, year-key
  mismatch, uncited entries, unresolved `% CITATION_NEEDED` markers.
- `audit_draft.py`: mechanical writing rules — footnotes, file/code artifacts, local
  paths, subsection budget, duplicate labels, input consistency, leftover markers,
  content-page budget, and the disclosure check (internal identifiers and do-not-disclose
  entities listed in `paper/.disclosure.yaml`, plus a heuristic warning for internal-looking
  identifier tokens even when no list is present).

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
- **No footnotes.** Do not use `\footnote{...}` anywhere. Move the content into the main body as
  inline parenthetical text, or delete it if it does not matter. CS/ML conference papers should
  not rely on footnotes.
- **No file names or code artifacts in prose.** Do not write `\texttt{filename.ext}` or raw
  code identifiers in the paper text. Replace with descriptive natural language: "the benchmark
  manifest" not `\texttt{BENCHMARK_MANIFEST.json}`, "the released evaluation script" not
  `\texttt{compute_asr.py}`. File names and code artifacts are implementation details that
  break the reader's attention and should not appear in published prose.
- **No local paths or directories in prose.** Remove any local filesystem paths, directory
  names, or repository-relative paths from the paper text.

### Before Returning

Internally check: paragraph flow, section alignment, figure/table placement, Abstract/Introduction
consistency, Introduction claim support in Experiments, Method and Experiments correspondence,
Related Work positioning, terminology, missing citations, conclusion overclaiming, venue page
counting, post-main section order, required statements/checklists, appendix/supplement handling,
anonymity-sensitive locations, **front-to-back data consistency (the same metric reads the same in
abstract/text/table/caption; deltas and "average over N" match the reported numbers; every headline
number is backed in the body),** and skeptical reviewer risk.

If `latexmk` or `pdflatex` is available, compile the draft and run the applicable content-page audit
before returning. For page-limited venues, a draft whose main text exceeds the limit is not complete,
even if the Paper Framework's planned budget was within the limit. Do not call the draft clean or
submission-ready unless template, citation, evidence, page-budget, and compilation risks are
resolved.

**Compliance Self-Check (Before Returning) — complete before declaring the draft done.** Answer each
item yes/no and paste the evidence. **Any "no" means the draft is not done — fix it first.**
This check is MANDATORY and cannot be skipped.

**⛔ BLOCKING GATE — Static Audits (must pass before anything else):**
1. Did I run `audit_citations.py` and does it report `PASS`?  (Paste result. **If any error,
   fix every one in `references.bib` and re-run. Do not proceed past this item while errors
   remain. A draft with citation audit failures is not complete.**)
2. Did I run `audit_draft.py` (with `--max-content-pages <limit>` when a page limit exists)
   and does it report `PASS`?  (Paste result. **If any error, fix and re-run. Do not proceed
   while errors remain.**)

**Mandatory Gates:**
3. Did I load `references/sections/paper-review.md` immediately after the first complete `paper/`
   draft existed and run **both** review rounds (Round 1 self + Round 2 independent subagent), per
   the Draft Completion Review Gate, before any draft was returned to the user?
4. Did I load `references/checks/submission-readiness.md` and produce the Submission Readiness Report?
5. For every drafted section, did I run the Section-Method Adherence check, with no `missing` move
   left unresolved?
6. Does the structure still match the confirmed Paper Framework (section list, subsection budget),
   with no silently introduced sections or subsections?
7. Did I load and apply `references/figures/figure-planning.md` (Display Review Gate) for every
   generated figure?
8. If the draft has an appendix, did I inspect its compiled pages and confirm it is **substantive,
   not sparse** — every appendix section has a real lead paragraph (not a `Table~N provides ...`
   pointer), floats sit under their heading rather than scattering into half-empty pages, and no
   `see supplementary material` stub stands in for content that exists? (Apply Table Handling rule 11
   / `figures-and-tables.md` "The appendix has the opposite failure".)

**Load receipt:** list which mandatory references were loaded. A mandatory gate whose reference
was never loaded counts as a failed check, not a pass.

**Load receipt:** in the internal check, list which mandatory references were loaded
(`paper-review.md`, `figure-planning.md`, `submission-readiness.md`, plus the section guides used).
A mandatory gate whose reference was never loaded counts as a failed check, not a pass.

### Final Submission Readiness Gate

For a complete `paper/` draft, load `references/checks/submission-readiness.md` before returning
any submission-ready claim. Produce a compact Submission Readiness Report with verdict
`PASS / BLOCKED / OPEN_DECISION`, compile/PDF status, citation audit status, venue/format status,
evidence/claim status, blocking risks, open decisions, and next fixes. Do not call a draft
submission-ready when the gate is `BLOCKED` or `OPEN_DECISION`.

When `venue_kind=journal`, also run `references/checks/journal-submission-elements.md` as part of
this gate (mandatory statements, display-item caps/tiers, methods placement, and word/length
budget) and fold its verdicts into the report.

Return a concise interaction-language summary listing generated files and any blocking risks.
