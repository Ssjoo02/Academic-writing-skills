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
| Writing Policy | `writing-policies/<paper-slug>-writing-policy.md` |
| Paper Framework | `writing-policies/<paper-slug>-paper-framework.md` and `writing-policies/<paper-slug>-paper-framework.confirmation.md` |
| Full Draft | complete `paper/` LaTeX project with `main.tex`, `sections/*.tex`, `references.bib`, and `math_commands.tex` |

## Execution Contract

Follow this contract before reading more references or writing downstream files.

| Stage | Required output | Hard stop |
|---|---|---|
| Writing Policy | `writing-policies/<paper-slug>-writing-policy.md` | **STOP HERE and wait for user response.** Do not generate Paper Framework until confirmed. |
| Paper Framework | `writing-policies/<paper-slug>-paper-framework.md` and `.confirmation.md` | **STOP HERE and wait for user response.** Do not create `paper/` until confirmed. |
| Full Draft | complete `paper/` LaTeX project | Return generated files, unresolved markers, and citation/template/compile risks. |

Mandatory gate behavior:

- A user request for a complete paper draft authorizes the workflow, not automatic passage through
  the gates.
- Do not "compress", "batch", "assume", or "silently satisfy" the Writing Policy or Paper
  Framework confirmation gates.
- After writing the Writing Policy, return only the concise policy summary, stage ledger, and the
  required user action. **STOP HERE and wait for user response.** Do not load archetype, venue,
  domain, section, figure, template, example, or check references until the user confirms the
  Writing Policy. Ask exactly for confirmation or corrections to the Writing Policy before moving
  to Paper Framework.
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

Use the interaction language from `../SKILL.md` for user-facing summaries, checkpoint text,
clarification questions, and confirmation files. Keep paper prose, LaTeX content, BibTeX entries,
file paths, and machine-readable fields in English unless the user explicitly requests a Chinese
paper artifact.

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

- paper archetype,
- research domain, or `generic` / `no matching profile`,
- core contribution and central claim,
- evidence boundary: available results, source evidence, and unsupported claims,
- key terms and naming conflicts,
- source conflicts affecting claims, evidence, terminology, or paper identity.

Optional context, record only when visible:

- target venue, otherwise `generic / venue TBD`,
- existing draft files and progress,
- figures, tables, bibliography, code/data artifacts,
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

Do not load venue, archetype, domain, section, figure, style, or check references during workspace
discovery. Discovery reads project materials only.

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
`generic_article.tex (non-submission draft template)` unless the user later supplies a venue.

Ask at most 1-3 questions per round. A round is one clarification message sent before the agent
continues to the next stage. Normal Writing Policy generation should need at most one round.

Use the concise user-facing question format from `../SKILL.md`. Keep target, inference, basis, why
decisive, and safe default internal unless the user asks for reasoning or the conflict is high-risk.

Prefer confirm/correct questions over open-ended questions:

```text
Before Writing Policy, I need one decision: should this be treated as a method paper?
I infer method paper from the README and ablation-heavy results. Please confirm or correct.
Default if unanswered: write `paper archetype = method paper`.
```

For target venue, do not ask before Writing Policy when it is merely unspecified. Record
`target venue = generic / venue TBD; use generic framework unless the user requests venue-specific
planning`. Before Paper Framework, ask only if the user explicitly wants a venue-specific framework
or if venue ambiguity blocks a user-requested venue-specific template. Otherwise use a generic
framework and `generic_article.tex` without asking again.

## 3. Writing Policy

Load only `../references/principles/research-strategy.md`.

Do not load venue, archetype, domain, template, section, figure, style, or check references by
default during Writing Policy generation. Writing Policy should identify candidate venue, archetype,
and domain from the workspace and user prompt, but detailed venue constraints and section templates
are resolved in Paper Framework.

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
2. **Paper Identity**: target venue, paper archetype, archetype profile filename when available,
   domain, domain profile filename or `generic` / `no matching profile`, intended reader, core
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

If the interaction language is Chinese, add a final **Chinese Confirmation Summary** with only:
paper type, target venue, one-sentence contribution, core claim boundary, main evidence status,
top risks, and decisions the user must confirm. If the interaction language is English, do not add a
Chinese summary unless requested.

Record venue status in the Writing Policy as one of:

- `confirmed: <venue>` when the user or workspace clearly specifies it,
- `generic / venue TBD` when unspecified,
- `conflict: <options>` only when workspace/user sources disagree on a venue and venue-specific
  planning is required.

Do not include a section strategy in the Writing Policy. Section choices belong in the Paper
Framework after the Writing Policy is confirmed.

The paper archetype must be resolved before confirming the Writing Policy. If it cannot be inferred
or safely defaulted, ask the user before finalizing the Writing Policy. The domain should also be
resolved before Paper Framework as either a known domain profile, `generic`, or `no matching profile`.
Do not defer unresolved paper archetype or domain selection to Paper Framework.

Status vocabulary: `unknown`, `supported`, `partially supported`, `needs evidence`, `not verified`,
`should avoid`.

Show only a concise summary: paper type, target venue, one-sentence contribution, core story, main
claim/evidence statuses, key terminology decisions, available experiments/figures/tables, top
claim or drafting risks, and decisive questions requiring confirmation.

Writing Policy checkpoint content snapshot must include:

- paper identity: working name, paper archetype, domain, and target venue status,
- research content: core research question, one-sentence contribution, and central claim boundary,
- evidence snapshot: key source-evidence types and what they support,
- experiment/result snapshot: current datasets/tasks/models/metrics/result ranges found, or
  `not found in inspected sources` if missing; include concrete counts, denominators, metric names,
  and result ranges when available,
- top risks: 2-3 claim, evidence, terminology, result, or citation risks that affect drafting,
- decisions to confirm: split into `Required` identity/framing/claim-boundary decisions and
  `Optional` venue/template/style defaults.

Do not replace this content snapshot with a line-count, existence check, or generic statement that
the policy was written. If experiments or results are not available, say that explicitly in the
snapshot instead of omitting the category.

Inputs:

- user request and workspace path,
- compact workspace evidence and source traces,
- any direct answers to decisive clarification questions,
- `../references/principles/research-strategy.md`.

Output file:

```text
writing-policies/<paper-slug>-writing-policy.md
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
- venue format and submission constraints: `../references/venues/<venue>.md` when a target venue is
  confirmed,
- paper archetype section structure: `../references/archetypes/<archetype>.md` from the confirmed
  Writing Policy,
- domain-specific evidence pressure and section content: `../references/domains/<domain>.md` only
  when the confirmed domain has a matching profile,
- figure/table planning: `../references/figures/figure-planning.md`.

Use `../references/venues/index.md` only when a venue hint exists but the profile mapping is
unclear, or when the user explicitly asks for venue options. Do not use archetype/domain indexes at
this stage to decide paper identity; archetype and domain come from the confirmed Writing Policy.
If the confirmed Writing Policy records only a human-readable archetype or domain label, use
`../references/archetypes/index.md` or `../references/domains/index.md` only to resolve the profile
filename, not to re-decide the paper identity.
If the confirmed domain has no matching profile, skip the domain profile and rely on the Writing
Policy plus archetype profile.

Do not load section-level guide files, section examples, `paragraph-flow.md`, style references, or
check references at this stage. Those files are used only when drafting, revising, or reviewing
specific text.

Build the framework in this order:

1. **Venue first**: if a target venue is confirmed, use the venue profile for physical format and
   submission constraints, including official template source, single-column/two-column layout, page
   budget, anonymity, citation style, required statements, and whether references count toward the
   limit. If no target venue is confirmed, use a generic framework and record the selected template
   as `generic_article.tex (non-submission draft template)`.
2. **Archetype second**: load the confirmed paper archetype profile and use its `Framework Effects`
   as the primary source for section structure. The lightweight section roles below are fallback
   guidance only, not a replacement for the archetype profile.
3. **Domain third**: use the domain profile to add required content, evidence pressure, metrics,
   figures/tables, and claim/evaluation risks inside those sections.
4. **Writing Policy last**: keep only sections and claims supported by available evidence; move
   unresolved structure, evidence, template, or venue decisions to Open Decisions.

Use `../templates/index.md` to select the preloaded official-style venue template when a target
venue is confirmed. If no target venue is confirmed, select `generic_article.tex` as a
non-submission draft template and record that the official target-venue template must be resolved
before submission. If the needed venue template is not present, use a user-provided official
template or the official template source recorded for that venue. If a selected template requires a
companion `.sty`, `.cls`, or `.bst` file that is not available in `../templates/` or the workspace,
record `template companion missing` in Open Decisions and do not claim the draft is compilable. Do
not invent venue formatting from memory.

Current preloaded templates:

- `../templates/index.md`
- `../templates/generic_article.tex`
- `../templates/iclr2026.tex`
- `../templates/neurips2025.tex`
- `../templates/icml2025.tex`
- `../templates/ieee_conference.tex`
- `../templates/ieee_journal.tex`
- `../templates/IEEEtran.cls`
- `../templates/IEEEtran.bst`
- `../templates/math_commands.tex`

Load `../references/figures/figure-planning.md` during Paper Framework generation. Deciding whether
the main paper needs figures or tables, where they belong, what message they carry, and how they
will be generated is part of the framework. Do not generate figures during framework writing.

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
writing-policies/<paper-slug>-paper-framework.confirmation.md
```

Paper Framework file format:

1. **Inputs Used**: Writing Policy path, target venue, selected template path or template source,
   venue format summary, page/length budget, paper archetype, domain, evidence snapshot.
2. **Section Framework**: ordered section list. For each section, include section name, main
   content, rough length budget, key evidence or figure/table if any, and one writing caution if
   needed.
3. **Figure Plan**: a short table with only figures/tables that are likely to appear in the main
   paper. Include `ID`, `type`, `section`, `message`, `source`, and `generation route`.
4. **Open Decisions**: only blocking missing evidence, uncertain section choices, terminology,
   figure/table choices, or user decisions.

When target venue is `generic / venue TBD`, Paper Framework should record:

- `target venue: generic / venue TBD`,
- `selected template: generic_article.tex (non-submission draft template)`,
- `venue format summary: generic research paper draft; not submission-ready`,
- `page/length budget: flexible; resolve after target venue is selected`.

Output files:

```text
writing-policies/<paper-slug>-paper-framework.md
writing-policies/<paper-slug>-paper-framework.confirmation.md
```

Output format: Markdown using the four sections above. The primary framework is English and
technical. The confirmation file is concise, user-facing, and written in the interaction language.

Keep the framework short. Do not include paragraph-level plans, detailed claim-evidence tables,
full formal-review risk maps, or long figure/table inventories.

Create both the English framework and the concise confirmation framework. Show the confirmation
framework, plus any blocking Open Decisions, to the user for confirmation.

Paper Framework checkpoint content snapshot must include:

- confirmed paper identity and any user changes from the Writing Policy gate,
- proposed section order with each section's role in the argument,
- main figure/table plan and which evidence supports each planned visual,
- expected experiment/result placement by section,
- unresolved structure, evidence, citation, template, or figure blockers,
- decisions to confirm before creating `paper/`.

Gate: the user must confirm the Paper Framework before full-draft writing. If the user changes
section order, figure/table arrangement, experiment emphasis, or contribution wording, update the
Paper Framework and ask for confirmation again.

## 5. Full Draft LaTeX Project

Use the confirmed Writing Policy, confirmed Paper Framework, relevant section guides,
`../references/sections/paragraph-flow.md`, relevant experiment/figure/table materials, and
`../references/figures/figure-planning.md` only when figures or tables will be generated, revised,
or inserted.

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
4. Create `paper/sections/` files matching the confirmed Paper Framework section list.
5. Update `paper/main.tex` so its `\input{sections/...}` calls match the confirmed section files.
6. Remove stale section files not referenced by the updated `paper/main.tex`.

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
2. For data-driven plots and tables, create reproducible scripts or table files under
   `paper/figures/` and read data from workspace result files; do not hardcode results from memory.
3. For architecture, pipeline, workflow, or system diagrams, prefer the configured paper-figure MCP
   or a deterministic FigureSpec-style JSON-to-SVG/PDF route when available. Keep the source spec in
   `paper/figures/specs/`.
4. For screenshots or qualitative examples, use existing workspace assets and record their source.
5. Insert each figure/table only in the section specified by the confirmed Paper Framework unless
   drafting reveals a clear conflict; if conflict changes the paper structure, ask the user.
6. Captions must state the figure's message and supported claim, not merely describe visual content.

Load section references when drafting each section. Follow the `Research-Paper-Writing-Skills`
pattern: load only the current section guide by default; load a local example only when the section
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
overclaiming, and skeptical reviewer risk across Contribution, Writing clarity, Experimental
strength, Evaluation completeness, and Method design soundness.

If `latexmk` or `pdflatex` is available, compile the draft once from `paper/main.tex` and report the
result. If compilation is skipped because tooling or template companions are missing, report the
exact reason. Do not call the draft submission-ready unless template, citation, evidence, and
compilation risks are resolved.

Do not show paragraph, section, or full-paper review tables by default. Show review details only
when the user asks or when a blocking issue remains unresolved.
