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

Follow this contract before reading more references or writing downstream files.

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

Workflow plan behavior:

- At workflow start, create or show a concise plan derived from the state machine.
- During Writing Policy, the active plan should focus on evidence discovery, Writing Policy
  generation, lightweight artifact/policy consistency checks, and the checkpoint stop.
- Do not put package installation, `.venv` creation, registry smoke tests, full experiment execution,
  or source-directory writeability checks into the workflow plan unless the user asked for execution
  validation or those checks directly block writing the requested output artifact.
- Update the plan at the Writing Policy and Paper Framework confirmation gates and leave the next
  gated stage pending until the user confirms.

At every stage, keep a brief stage ledger in the user-facing summary:

- output artifact,
- decisions needing user confirmation,
- unresolved blockers,
- next required user action.

Use the interaction language from `../SKILL.md` for user-facing summaries, checkpoint text, and
clarification questions. Keep paper prose, LaTeX content, BibTeX entries, file paths, and
machine-readable fields in English unless the user explicitly requests a Chinese paper artifact.
Writing Policy and Paper Framework artifacts are English by default. If the user requests another
language version before a stage is generated, create a complete translated sibling artifact with the
same content and structure, changing only the natural language.

Do not make a checkpoint summary primarily about process mechanics, file existence, line counts, or
which folders were avoided. Those details can appear inside the written policy/framework when they
matter for traceability. The visible checkpoint must expose the substantive paper state the user is
being asked to confirm.

For `Unresolved blockers`, include only issues that block the next writing stage or would make the
paper contract false: unresolved paper identity, claim boundary, evidence availability, metric
definition, taxonomy, result denominator, citation source, template/venue requirement, or required
user decision. Do not include workspace write permissions, package setup, `.venv` creation, smoke
tests, or runtime environment notes unless they prevent writing the output artifact under the user
requested output directory or directly invalidate a result/evidence claim.

`<paper-slug>` is a stable lowercase kebab-case filename stem. Infer it from the project, method,
benchmark, or dataset name. If no specific name is visible, use the workspace directory name. If a
file would collide, append the date as `-YYYYMMDD`. Do not ask the user only to choose a slug.

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

Use the global Clarification Protocol in `../SKILL.md` after scanning enough workspace evidence. Do
not run a front-loaded questionnaire before reading project materials.

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

Stop discovery once the paper contract can be supported with source traces. Do not exhaustively
read large source trees or logs unless a decisive conflict remains.

Do not run environment setup, dependency installation, registry smoke checks, benchmark execution,
or `.venv` creation during Writing Policy generation. Writing Policy may read scripts, configs,
metadata, and existing result files as evidence, but it should not execute experiments or test the
runtime unless the user explicitly asks for execution verification.

Extract compactly into the Writing Policy:

- project facts and source traces needed for the paper contract,
- paper identity, core contribution, central claim, and evidence boundary,
- key terms, naming conflicts, and source conflicts,
- available evidence/results and unsupported claims,
- optional visible assets or weakness/review notes only when they affect drafting.

Classify important sources as `raw evidence`, `derived statistics`, or `draft-derived candidate`.
If sources conflict on counts, denominators, model names, method names, key terms, metrics,
baselines, dataset splits, protocols, venue hints, or central claims, do not smooth the conflict
over.

- If the conflict is decisive, ask the user before finalizing the Writing Policy.
- If the conflict is not decisive, record it in `Open Decisions` or `Assets And Constraints` with a
  conservative default.
- If the user does not answer a decisive evidence conflict, avoid exact numbers or strong claims and
  mark affected claims as `partially supported`, `needs evidence`, or `not verified`.

Do not load venue, paper type, domain evidence adapter, section, figure, style, or check references
during workspace discovery. Discovery reads project materials only.

## 2. Full Draft Clarification Boundaries

Use these boundaries together with the global Clarification Protocol in `../SKILL.md`. The global
protocol decides whether to ask; this section decides which Full Draft stage owns the question.

Build an internal question queue after workspace discovery, but show only questions that meet the
Ask Now Criteria:

```markdown
| Candidate question | Stage | Impact | Confidence | Safe default | Ask now? |
|---|---|---|---|---|---|
```

Ask immediately only when all are true:

1. the answer affects the current stage output,
2. no conservative default can preserve correctness,
3. a wrong guess would cause a false claim, wrong paper identity, wrong terminology, or large
   downstream rewrite,
4. the answer cannot be recovered from workspace evidence.

If an item does not satisfy these criteria, record the inference, default, or deferred decision in
the relevant output file.

Stage boundaries:

| Stage | Ask now only for | Defer or default |
|---|---|---|
| Writing Policy | paper identity, core story, claim/evidence boundary, key terminology, decisive source conflict | venue if unspecified, page budget, section order, figure placement, caption wording, optional ablations |
| Paper Framework | user-required venue-specific planning with missing/contradictory venue, missing official/preloaded template, blocking Writing Policy decision that changes section structure | template choice, page budget, section order, and figure/table plan when the agent can choose conservatively |
| Section Drafting | facts needed to write the section correctly without false claims | weaken the claim, defer the decision, or insert a precise LaTeX marker |

Ask about venue at most once. If unspecified, use `generic / venue TBD` and
`generic_article.tex (non-submission single-column draft template)` unless the user later supplies a
venue. The fallback length is a soft drafting budget of 6-8 main-text pages, excluding references
and appendix; it is not a venue page limit.

Ask at most 1-3 questions per round. A round is one clarification message sent before the agent
continues to the next stage. Normal Writing Policy generation should need at most one round.

Use the concise user-facing question format from `../SKILL.md`. Keep target, inference, basis, why
decisive, and safe default internal unless the user asks for reasoning or the conflict is high-risk.

Prefer confirm/correct questions over open-ended questions:

```text
Before Writing Policy, I need one decision: should this be treated as a method paper?
I infer method paper from the README and ablation-heavy results. Please confirm or correct.
Default if unanswered: use `method-paper.md` because the evidence strongly supports it; correct this
before Paper Framework if the paper identity is different.
```

For target venue, do not ask before Writing Policy when it is merely unspecified. Record
`target venue = generic / venue TBD; use generic framework unless the user requests venue-specific
planning`. Before Paper Framework, ask only if the user explicitly wants a venue-specific framework
or if venue ambiguity blocks a user-requested venue-specific template. Otherwise use a generic
framework, `generic_article.tex`, and the 6-8 main-text-page drafting budget without asking again.

## 3. Writing Policy

Load only `../references/principles/research-strategy.md`.

Do not load venue, paper type, domain evidence adapter, template, section, figure, style, or check
references by default during Writing Policy generation. Writing Policy should identify candidate
venue, paper type, and any clear domain evidence adapter from the workspace and user prompt, but
detailed venue constraints and section templates are resolved in Paper Framework.

Only load `../references/checks/claim-evidence.md` during Writing Policy if the user explicitly asks
for a claim audit or if a central claim is high-risk and cannot be safely classified using the
available evidence. Defer metric, citation, formal review, reviewer-risk, section, and figure
references to later stages.

The Writing Policy is a compact writing contract. It records what is known, what can be claimed,
what must be weakened, which terms must stay stable, and which decisive choices still need the user.
It is not a section outline and not a paragraph plan.

Save it to:

```text
writing-policies/<paper-slug>-writing-policy.md
```

Writing Policy file format:

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
6. **Assets And Constraints**: only visible assets or constraints that affect drafting, such as
   result files, key figures/tables, bibliography status, known missing evidence, source conflicts,
   or template status already visible from project files.
7. **Open Decisions**: only unresolved decisions that can change the paper identity, central claim,
   evidence boundary, key terminology, figure/table plan, or venue/template choice.

Do not add a short translated confirmation summary inside the Writing Policy. If the user requested
another language version before this stage was generated, create a complete same-content translated
sibling artifact such as `writing-policies/<paper-slug>-writing-policy.zh-CN.md`; preserve the same
sections, tables, claims, evidence statuses, and open decisions.

Record venue status in the Writing Policy as one of:

- `confirmed: <venue>` when the user or workspace clearly specifies it,
- `generic / venue TBD` when unspecified,
- `conflict: <options>` only when workspace/user sources disagree on a venue and venue-specific
  planning is required.

Do not include a section strategy in the Writing Policy. Section choices belong in the Paper
Framework after the Writing Policy is confirmed.

The paper type must be resolved before confirming the Writing Policy. Check
`../references/paper-types/index.md` before defaulting. If one specific profile clearly controls the
main evidence burden, use it and mark the inference in the Writing Policy. If the type is unknown,
mixed, or too sparse to classify without distorting the paper, use `generic-paper.md` as a
provisional section-planning fallback and record why. Do not use `method-paper.md` as a global
default. Ask the user before finalizing the Writing Policy only when even the generic fallback would
make the paper identity false or hide a decisive conflict. Domain evidence adapters are optional
evidence adapters, not required paper identity. Do not force a domain adapter match. If there is no
clear match, record `domain evidence adapter = none / no matching profile` and continue. Do not defer
unresolved paper type selection to Paper Framework.

Status vocabulary: `unknown`, `supported`, `partially supported`, `needs evidence`, `not verified`,
`should avoid`.

Show only a concise checkpoint summary: paper type, target venue, one-sentence contribution, core
story, main claim/evidence statuses, key terminology decisions, available
experiments/figures/tables, top claim or drafting risks, and decisive questions requiring
confirmation.

Writing Policy checkpoint summary must include:

- paper identity: working name, paper type, optional domain evidence adapter, and target venue status,
- research content: core research question, one-sentence contribution, and central claim boundary,
- evidence snapshot: key source-evidence types and what they support,
- experiment/result snapshot: current datasets/tasks/models/metrics/result ranges found, or
  `not found in inspected sources` if missing; include concrete counts, denominators, metric names,
  and result ranges when available,
- top risks: 2-3 claim, evidence, terminology, result, or citation risks that affect drafting,
- decisions to confirm: split into `Required` identity/framing/claim-boundary decisions and
  `Optional` venue/template/style defaults.

Do not replace this summary with a line-count, existence check, or generic statement that the policy
was written. If experiments or results are not available, say that explicitly instead of omitting the
category.

Inputs:

- user request and workspace path,
- compact workspace evidence and source traces,
- any direct answers to decisive clarification questions,
- `../references/principles/research-strategy.md`.

Output file:

```text
writing-policies/<paper-slug>-writing-policy.md
```

Optional translated output files, only when requested before generation:

```text
writing-policies/<paper-slug>-writing-policy.<language-code>.md
```

Output format: Markdown using the seven sections above.

Gate: the user must confirm the Writing Policy before Paper Framework generation.

## 4. Paper Framework

The Paper Framework is a concise section-level plan for the paper. It decides which sections the
paper will have and what each section mainly writes. It is not a paragraph plan and not prose.

Inputs:

- confirmed `writing-policies/<paper-slug>-writing-policy.md`,
- user confirmations and changes from the Writing Policy gate,
- workspace evidence snapshot and asset inventory from the Writing Policy.

Load only the references needed to resolve paper structure and physical format:

- template selection: `../templates/index.md`,
- venue framework constraints: `../references/venues/<venue>.md` when a target venue is confirmed,
- paper type section/page-budget reference: `../references/paper-types/<paper-type>.md` from the confirmed
  Writing Policy,
- optional domain evidence adapter: `../references/domains/<domain>.md` only when the Writing
  Policy names a clear matching adapter,
- figure/table planning: `../references/figures/figure-planning.md`.

Use `../references/venues/index.md` only when a venue hint exists but the profile mapping is
unclear, or when the user explicitly asks for venue options. Do not use paper type or domain-adapter
indexes at this stage to decide paper identity; paper type comes from the confirmed Writing Policy.
If the confirmed Writing Policy records only a human-readable paper type label, use
`../references/paper-types/index.md` only to resolve the profile filename, not to re-decide the paper
identity. Use `../references/domains/index.md` only when the Writing Policy already points to a
clear domain-adapter candidate and the filename needs resolution. If there is no clear match, skip
the domain evidence adapter and rely on the Writing Policy plus paper type profile.

Do not load section-level guide files, section examples, `paragraph-flow.md`, style references, or
check references at this stage. Those files are used only when drafting, revising, or reviewing
specific text.

Build the framework in this order:

1. **Venue first**: if a target venue is confirmed, use the venue profile as a Paper Framework
   constraint card. Apply only facts recorded there or in a current official/user-provided venue
   guideline: official template source, single-column/two-column layout, page budget, anonymity,
   citation style, required statements, post-main section order, and whether references, appendices,
   checklists, ethics, limitations, acknowledgments, or supplementary material count toward the
   limit. The venue schema is strict but facts may be incomplete: if a required venue fact is missing,
   stale, or only generically described, record the exact field as `not verified` or an Open Decision
   and do not invent it from memory. If no target venue is confirmed, use a generic framework and
   record the selected template as `generic_article.tex (non-submission single-column draft
   template)` with a soft 6-8 main-text-page drafting budget, excluding references and appendix.
2. **Paper type second**: load the confirmed paper type profile and use it only as a flexible
   section/page-budget reference. It helps decide candidate sections and approximate section budgets;
   it is not a fixed template and must be adapted to the actual paper, venue, evidence, and user
   request. The lightweight section roles below are fallback guidance only, not a replacement for
   the paper type profile.
3. **Domain evidence adapter third, optional**: when a clear adapter matches, use it to add evidence
   pressure, metrics, baselines, figures/tables, and claim/evaluation risks inside those sections.
   If there is no clear match, skip this step; do not force a domain adapter match.
4. **Writing Policy last**: keep only sections and claims supported by available evidence; move
   unresolved structure, evidence, template, or venue decisions to Open Decisions.

Use `../templates/index.md` to select the preloaded official-style venue template when a target
venue is confirmed. If no target venue is confirmed, select `generic_article.tex` as a
non-submission single-column draft template and record that the official target-venue template must
be resolved before submission. In this fallback, set the page/length budget to `soft drafting
budget: 6-8 main-text pages, excluding references and appendix; not a submission limit`. If the
needed venue template is not present, use a user-provided official template or the official template
source recorded for that venue. If a selected template requires a companion `.sty`, `.cls`, or `.bst`
file that is not available in `../templates/` or the workspace, record `template companion missing`
in Open Decisions and do not claim the draft is compilable. Do not invent venue formatting from
memory.

Page-budget arithmetic:

- If the target venue has a page limit, compute the total main-text budget first, including whether
  references, appendix, checklist, acknowledgments, ethics/limitations statements, or supplementary
  material count toward the limit according to verified facts in the venue profile or a current
  official/user-provided venue guideline. The Section Framework must include `Page budget` for every
  section, and the total planned pages must not exceed the venue limit. If the venue limit is
  verified, the total planned pages must not exceed the verified venue limit. If the venue limit is
  not verified, record the current page budget as an Open Decision and use a conservative planning
  budget without calling it a submission limit.
- If the target venue is `generic / venue TBD`, use a soft drafting budget of 6-8 main-text pages,
  excluding references and appendix; this is not a submission limit.
- Allocate section pages after loading the confirmed paper type profile. Treat
  `../references/paper-types/<paper-type>.md` as a flexible section and page-budget reference, and
  verified venue facts as the hard physical constraint.
- Adapt the profile instead of copying it mechanically: merge, rename, split, shrink, or omit
  sections when the actual contribution, available evidence, user request, or venue budget requires
  it. Still record numeric section budgets and ensure their total fits the venue or generic budget.
- If the required content cannot fit the page budget, merge sections, move secondary analyses to
  appendix candidates, or mark the overflow as an Open Decision. Do not silently exceed the target
  budget.

Current preloaded templates:

- `../templates/index.md`
- `../templates/generic_article.tex`
- `../templates/iclr2026.tex`
- `../templates/iclr2026_conference.sty`
- `../templates/iclr2026_conference.bst`
- `../templates/neurips2026.tex`
- `../templates/neurips_2026.sty`
- `../templates/checklist.tex`
- `../templates/icml2026.tex`
- `../templates/icml2026.sty`
- `../templates/icml2026.bst`
- `../templates/algorithm.sty`
- `../templates/algorithmic.sty`
- `../templates/acl2026.tex`
- `../templates/acl.sty`
- `../templates/acl_natbib.bst`
- `../templates/cvpr2026.tex`
- `../templates/preamble.tex`
- `../templates/cvpr.sty`
- `../templates/ieeenat_fullname.bst`
- `../templates/aaai2026.tex`
- `../templates/aaai2026.sty`
- `../templates/aaai2026.bst`
- `../templates/aaai2026.bib`
- `../templates/ijcai26.tex`
- `../templates/ijcai26.sty`
- `../templates/named.bst`
- `../templates/ijcai26.bib`
- `../templates/acm_mm2026.tex`
- `../templates/acmart.cls`
- `../templates/acm.bst`
- `../templates/ieee_conference.tex`
- `../templates/ieee_journal.tex`
- `../templates/IEEEtran.cls`
- `../templates/IEEEtran.bst`
- `../templates/math_commands.tex`

Load `../references/figures/figure-planning.md` during Paper Framework generation. Deciding whether
the main paper needs figures or tables, where they belong, what message they carry, and how they
will be generated is part of the framework. Do not generate figures during framework writing.

Generic fallback compression rules:

- When target venue is `generic / venue TBD`, keep the main-paper framework compact: 4-6 numbered
  main sections between Introduction and Conclusion, excluding Abstract and Conclusion.
- Prefer merged section names when evidence does not require separation, such as `Benchmark and
  Evaluation Protocol`, `Results and Diagnostic Analysis`, or `Discussion, Limitations, and
  Reproducibility`.
- Split a standalone section only when the Writing Policy shows that the topic is a core
  contribution, a major evidence block, or a likely reviewer blocker that would become unclear if
  merged.
- Keep the main Figure Plan to 3-5 figures/tables for the generic draft. Put extra diagnostics,
  release tables, ablations, or qualitative cases in Open Decisions or appendix candidates instead
  of the main plan.

Lightweight section roles:

| Section | Framework role |
|---|---|
| Abstract | Summarize problem, contribution, evidence, and boundary at a high level. |
| Introduction | Establish problem, gap/challenge, contribution, and evidence promise. |
| Related Work | Position the contribution against the closest prior work and clarify the gap. |
| Method / System | Explain the main design or system components and why they address the challenge. |
| Experiments / Evaluation | Map research questions to evidence, metrics, baselines, ablations, and figures/tables. |
| Discussion / Limitations | State scope boundaries, risks, failure cases, and interpretation. |
| Conclusion | Close the argument without adding unsupported new claims. |

Save the framework to:

```text
writing-policies/<paper-slug>-paper-framework.md
```

Paper Framework file format:

1. **Inputs Used**: Writing Policy path, target venue, selected template path or template source,
   venue format summary, venue source status, page/length budget, paper type, optional domain
   evidence adapter, evidence snapshot.
2. **Page Budget Summary**: total venue or generic page budget, what counts toward the limit, planned
   main-text total, whether references, appendix, checklist, acknowledgments, ethics/limitations, and
   supplementary material count, and any overflow or compression decision.
3. **Section Framework**: ordered section list. For each section, include section name, main
   content, `Page budget`, key evidence or figure/table if any, and one writing caution if needed.
   The sum of section page budgets must fit the Page Budget Summary.
4. **Figure Plan**: a short table with only figures/tables that are likely to appear in the main
   paper. Include `ID`, `type`, `section`, `message`, `source`, and `generation route`.
5. **Venue Assembly Plan**: post-main order, required statements or checklists, optional appendices
   or supplementary material, and `not verified` venue fields that must be checked before
   submission-ready status.
6. **Open Decisions**: only blocking missing evidence, uncertain section choices, terminology,
   figure/table choices, or user decisions.

When target venue is `generic / venue TBD`, Paper Framework should record:

- `target venue: generic / venue TBD`,
- `selected template: generic_article.tex (non-submission single-column draft template)`,
- `venue format summary: generic research paper draft; not submission-ready; replace with the
  official target-venue template before submission`,
- `page/length budget: soft drafting budget of 6-8 main-text pages, excluding references and
  appendix; not a venue page limit`.

Output files:

```text
writing-policies/<paper-slug>-paper-framework.md
```

Optional translated output files, only when requested before generation:

```text
writing-policies/<paper-slug>-paper-framework.<language-code>.md
```

Output format: Markdown using the six sections above. The primary framework is English and
technical. A translated sibling artifact, when requested, must contain the same sections, page
budgets, figure plan, and open decisions; only the natural language changes.

Keep the framework short. Do not include paragraph-level plans, detailed claim-evidence tables,
full formal-review risk maps, or long figure/table inventories.

Show the framework to the user for confirmation in the conversation. Do not create a separate
confirmation file. For Chinese interaction, use this terminal-style checkpoint summary shape:

```markdown
Checkpoint: Paper Framework
Stage result: <one sentence>
Output: <framework artifact path, plus translated artifacts if any>

论文结构：

| 顺序 | Section | 主要内容 |
|---:|---|---|
| 1 | Abstract | <main content> |
| 2 | Introduction | <main content> |

图表计划：

| ID | 放置位置 | 内容 |
|---|---|---|
| Fig. 1 | Introduction | <message> |

Decisions to confirm:
- Required: <section order / page budget / venue assembly / figure plan decisions before creating paper/>
- Optional: <venue/template/additional language artifact defaults>
Unresolved blockers: <none or concise list>
User action required: 请确认是否继续创建 `paper/`，或说明要改的章节、页数预算、图表或 venue。
```

For English interaction, use the same content and table structure with English labels. Do not output
a separate `Content snapshot` bullet list.

Gate: the user must confirm the Paper Framework before full-draft writing. If the user changes
section order, figure/table arrangement, experiment emphasis, or contribution wording, update the
Paper Framework and ask for confirmation again.

## 5. Full Draft LaTeX Project

Use the confirmed Writing Policy, confirmed Paper Framework, the confirmed venue profile when a
venue is selected, relevant section guides, `../references/sections/paragraph-flow.md`, relevant
experiment/figure/table materials, and `../references/figures/figure-planning.md` only when figures
or tables will be generated, revised, or inserted.

The default full-draft deliverable is a complete English LaTeX paper project under `paper/`, not a
Markdown prose draft and not a Chinese-English parallel draft. If the user explicitly requests a
Chinese paper or Chinese-English parallel paper, create a separate auxiliary artifact outside the
submission `paper/` project and keep the English LaTeX project clean.

Before creating or overwriting LaTeX files:

1. If `paper/` already exists, back it up to `paper-backup-<timestamp>/`.
2. Copy the selected template from `../templates/` into `paper/main.tex`. If the Paper Framework
   uses `generic_article.tex`, mark the final summary with `non-submission template; replace with
   official venue template before submission`.
3. Copy required companion files, such as `math_commands.tex`, `IEEEtran.cls`, `IEEEtran.bst`, or
   venue `.sty` files, when the selected template needs them. If a required companion file is
   missing, keep drafting only if the Paper Framework allows a non-compilable draft; otherwise use
   `generic_article.tex` or ask the user for the official template source.
4. Replace official sample or instruction body text in `paper/main.tex` with the confirmed Paper
   Framework section inputs. Preserve the document class and venue options, required package/style
   setup, title/author anonymity policy, bibliography commands, and verified post-main hooks. Do not
   treat official sample prose as draft content.
5. Create `paper/sections/` files matching the confirmed Paper Framework section list.
6. Update `paper/main.tex` so its `\input{sections/...}` calls match the confirmed section files.
7. Assemble post-main material according to the Paper Framework's `Venue Assembly Plan`: required
   statements, references, checklists, appendices, acknowledgments, and supplementary pointers must
   appear only in locations supported by the confirmed venue profile or a current official/user
   guideline. If the order is `not verified`, keep the draft conservative, mark the field as an Open
   Decision, and do not call the output submission-ready.
8. Remove stale section files not referenced by the updated `paper/main.tex`.

Default LaTeX project layout:

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

Figure handling:

1. Read the confirmed Figure Plan from the Paper Framework.
2. Resolve the Image Renderer Preference recorded during intake or visible in the user request. If
   the user explicitly configured a picture API such as `GPT-image2` or `Gemini`, use that API for
   picture figures after the Picture Brief is written. If the user did not provide a picture API, the
   current executing agent draws the picture from the brief. This preference affects only non-data
   picture figures, not charts.
3. Load `../references/figures/plot-style.md` for data-driven plots and tables. For these outputs,
   data-driven plots default to Python and are drawn directly by the current agent. Write the final
   chart files as `paper/figures/<figure-id>.pdf` plus `paper/figures/<figure-id>.png` when a preview
   or raster fallback is useful, then include them in LaTeX. Do not create shared style modules,
   scripts directories, derived data folders, or audit files by default. Read data from workspace
   result files; do not hardcode results from memory.
4. For architecture, pipeline, workflow, or system diagrams, prefer the configured paper-figure MCP
   or a deterministic FigureSpec-style JSON-to-SVG/PDF route when available. Keep the source spec in
   `paper/figures/specs/`.
5. For non-data picture figures such as teasers, conceptual method illustrations, polished raster
   overview pictures, or qualitative visual summaries, load
   `../references/figures/picture-generation.md`. Always write the Picture Brief before attempting
   image generation. Save it to `paper/figures/prompts/<figure-id>.md`.
6. After the Picture Brief is written, generate `paper/figures/<figure-id>.png`. Use the user
   configured `GPT-image2`/`Gemini`/other picture API when explicitly provided; otherwise use the
   current executing agent's drawing or image-generation capability. Do not leave a planned picture
   blank. If a high-fidelity external renderer is unavailable, create a simpler paper-safe picture
   that follows the brief, then mark polish limitations in the final summary.
7. For screenshots or qualitative examples, use existing workspace assets and record their source.
8. Insert each figure/table only in the section specified by the confirmed Paper Framework unless
   drafting reveals a clear conflict; if conflict changes the paper structure, ask the user.
9. Captions must state the figure's message and supported claim, not merely describe visual content.
10. Save LaTeX snippets in `paper/figures/latex_includes.tex` when useful. Keep extra scripts,
   derived data files, or audits only when the user requests reproducibility packaging or when a
   complex result figure cannot be regenerated otherwise.

Load section references when drafting each section, load only the current section guide by default; load a local example only when the section
guide explicitly points to one, the section structure is uncertain, or the user asks to learn from
examples. Learn structure, not phrasing.

| Draft target | Load |
|---|---|
| Abstract | `../references/sections/abstract.md`, `../references/sections/paragraph-flow.md` |
| Introduction | `../references/sections/introduction.md`, `../references/sections/paragraph-flow.md` |
| Related Work | `../references/sections/related-work.md`, `../references/sections/paragraph-flow.md`; load `../references/checks/citation-integrity.md` when citation support matters |
| Method / System | `../references/sections/method.md`, `../references/sections/paragraph-flow.md`; load `../references/sections/figures-and-tables.md` when figures are used |
| Experiments / Evaluation | `../references/sections/experiments.md`, `../references/sections/paragraph-flow.md`; load `../references/checks/metric-design.md` and `../references/sections/figures-and-tables.md` when metrics, tables, or figures are used |
| Demo / Application | `../references/sections/demo-application.md`, `../references/sections/paragraph-flow.md`; load `../references/sections/figures-and-tables.md` when visuals are used |
| Conclusion / Limitations | `../references/sections/conclusion.md`, `../references/sections/paragraph-flow.md` |
| Final full-paper check | `../references/sections/paper-review.md`; load check files only for unresolved risks |

For each section, follow this drafting loop:

1. Read the confirmed Writing Policy, confirmed Paper Framework entry for the section, and relevant
   source evidence.
2. Load only the current section guide and conditional references from the table above.
3. Build an internal `Section Plan` and `Paragraph Plan` with paragraph role, message, evidence or
   source, and risk.
4. Write English LaTeX prose into the matching section file, preserving one paragraph per message.
5. Run reverse outlining and claim-evidence mapping internally; revise the section before moving to
   the next section.

Do not show internal section plans, paragraph plans, or claim-evidence maps unless the user asks or
a blocking risk must be surfaced.

Draft section by section into LaTeX section files. The visible product is the `paper/` directory:

```text
paper/main.tex
paper/sections/*.tex
paper/references.bib
paper/math_commands.tex
```

Return a concise interaction-language summary listing generated files and any blocking evidence,
citation, template, or compilation risks. Do not produce a Chinese parallel draft unless the user
explicitly requested a Chinese paper artifact.

Citation and bibliography rules:

- Prefer existing workspace `.bib` files when available.
- Do not generate BibTeX from memory.
- If no verified `.bib` entry is available, use `% CITATION_NEEDED: <short reason>` instead of a
  fabricated citation.
- If citation lookup is allowed and performed, record the source, DOI or URL, and verification
  status before adding the BibTeX entry.
- Mark unverified citations as `not verified` in comments or notes until verified.
- Use `\citep{}` / `\citet{}` for ML-style natbib venues when the selected template supports
  natbib.
- Use numeric `\cite{}` for IEEE templates; do not mix natbib commands with IEEE `cite`.
- Keep `paper/references.bib` limited to entries actually cited in `paper/sections/*.tex` and
  `paper/main.tex`.
- If citation support is uncertain, load `../references/checks/citation-integrity.md`.

Lightweight missing-support markers:

- Use markers only when a claim, citation, figure, table, or result slot is necessary for the
  section but the supporting evidence is missing or unverified.
- Prefer weakening or removing unsupported claims when possible.
- If the missing item materially affects the draft and cannot be resolved, insert a searchable
  LaTeX comment at the exact location:

```tex
% EVIDENCE_NEEDED: <short reason>
% CITATION_NEEDED: <short reason>
% FIGURE_NEEDED: <short reason>
% TABLE_NEEDED: <short reason>
```

- Do not use markers as placeholders for routine prose. Do not invent numbers, citations, figure
  references, or results around a marker.
- Include all remaining markers in the final summary as blocking or non-blocking risks.

Writing rules:

- Each paragraph has one message.
- The first sentence states the paragraph's function or core information.
- Define terms before using them.
- Claims require evidence; unsupported claims are weakened or marked.
- Methods must not read as ad hoc patches.
- Captions state the message supported by the figure or table.
- Abstract and Introduction claims require extra caution.

Before returning the full draft, internally check paragraph flow, section alignment, figure/table
placement, Abstract/Introduction consistency, Introduction claim support in Experiments, Method and
Experiments correspondence, Related Work positioning, terminology, missing citations, conclusion
overclaiming, venue page counting, post-main section order, required statements/checklists,
appendix/supplement handling, anonymity-sensitive locations, and skeptical reviewer risk across
Contribution, Writing clarity, Experimental strength, Evaluation completeness, and Method design
soundness.

If `latexmk` or `pdflatex` is available, compile the draft once from `paper/main.tex` and report the
result. If compilation is skipped because tooling or template companions are missing, report the
exact reason. Do not call the draft submission-ready unless template, citation, evidence, and
compilation risks are resolved and all venue fields that affect page counting, post-main order,
required statements/checklists, anonymity, and supplementary material are verified against the
confirmed venue profile or a current official/user-provided guideline.

Do not show paragraph, section, or full-paper review tables by default. Show review details only
when the user asks or when a blocking issue remains unresolved.
