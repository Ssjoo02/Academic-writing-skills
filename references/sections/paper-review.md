# Paper Review Principles

## Section Role

Use this file for whole-paper self-review, review reports, or final revision after a draft exists.
The goal is adversarial writing: read as a skeptical reviewer, identify rejection risks, and revise
before submission. In the Full Draft Workflow, this file is triggered automatically by the Full Draft Workflow
immediately after the first complete `paper/` draft exists; the user does not need to ask for review.
Do not load this file during Writing Policy generation unless the user explicitly asks for a formal
review.

## Acceptance Drivers

The paper should have:

1. sufficient contribution,
2. strong enough empirical effect or insight,
3. sufficient comparison experiments and ablation studies for its paper type,
4. clear writing and reproducible details,
5. reasonable method or benchmark design.

## Eight Review Dimensions (Six Core Plus Visual and Format Checks)

### Contribution

Check whether the paper gives readers new knowledge:

- novel task,
- novel pipeline,
- novel module,
- novel design choice,
- new experimental finding,
- new insight.

Failure signals: common failure case, well-explored technique, predictable improvement, or
straightforward design.

### Writing clarity

Check whether readers can understand and reproduce the work:

- clear story,
- motivated modules,
- stable terminology,
- enough technical detail,
- one paragraph, one message,
- **salience**: each paragraph/subsection leads with its point; length is allocated by importance,
  not by what is available,
- **no body enumeration**: taxonomies/inventories/per-category counts are mentioned in one stroke
  with the full list in a table or appendix, not enumerated `V1…Vn` / `H1…Hn` / per-app in the body;
  every prose number supports a claim instead of transcribing a table,
- no footnotes, file names, code artifacts, or local paths in prose,
- **no disclosure leaks**: no internal identifiers (checkpoint / training-run / sweep / wandb / tool
  / unreleased-model names) where a public display name belongs, and no do-not-disclose entity
  anywhere (not even by negation or exclusion phrasing).

Failure signals: a subsection that opens with background or a list instead of its point; an
itemize/enumerate of taxonomy members or per-category counts living in a body section; sentences that
restate numbers already in a table; a raw checkpoint/run name (e.g. a `..._step380` tag) or a
withheld baseline named in the text or in an "excludes X" clause.

### Experimental strength

Check whether the effect is meaningful:

- improvement is not marginal,
- absolute performance is credible,
- evidence supports main claims,
- failure modes are discussed.

### Evaluation completeness

Check whether evaluation covers what reviewers expect:

- important baselines,
- important metrics,
- ablation studies,
- controls,
- hard enough datasets or settings.

### Method design soundness

Check whether the design is reasonable:

- realistic setting,
- no hidden technical flaw,
- robust enough without per-case tuning,
- benefits outweigh added limitations,
- no negative net value.

### Internal consistency (front-to-back data and claim consistency)

Check that the paper agrees with itself end to end. This is a paper-vs-paper audit: the same fact
must read the same way wherever it appears, and every derived number must follow from the numbers
the paper itself reports. (The standalone paper-vs-raw-evidence audit lives at the Writing Policy
stage in `references/checks/workspace-logic-audit.md`; this dimension re-checks the assembled draft
for self-consistency.)

- **Cross-location number agreement**: a metric or result stated in the abstract, introduction, body
  text, a table, or a caption must carry the same value in every place it appears. Only standard
  rounding to the displayed precision is allowed; an abstract number that disagrees with its table
  is a defect.
- **Delta / improvement arithmetic**: every "+X%", "improves by", "Y× faster/smaller", or absolute
  gain must be arithmetically consistent with the underlying numbers reported elsewhere in the paper
  (e.g. a claimed 15% gain must match `(new - old) / old` computed from the table it draws on).
- **Aggregation and count consistency**: "average over N seeds/runs", "N datasets/tasks", sample
  sizes, denominators, and totals must match what the tables and figures actually contain; a claimed
  N must equal the reported N, and per-group counts must sum to the stated total.
- **Table/figure vs text agreement**: prose must not contradict its own table or figure (which row
  is best, the ranking of methods, which setting wins); the caption must describe what the table or
  figure actually shows, not a different result.
- **Claim-to-body support**: every headline claim in the abstract and introduction must be backed by
  a number or finding that actually appears later in the paper. A headline figure with no table or
  experiment behind it is a defect, not a rounding issue.
- **Terminology, notation, and units**: method/model/dataset/metric names, symbols, abbreviations,
  units, and metric direction (↑/↓) stay identical throughout. The same quantity must not be
  reported in different units or under two names in different sections.

When raw result files are available and cited by the draft, spot-check the load-bearing numbers
against them, but stay within writing-only scope: flag a mismatch as a finding; do not re-run or
modify experiments to "fix" it.

Failure signals: an abstract number no table backs; "15% improvement" that the table makes 12.8%;
"average of 5 seeds" beside a 3-row table; a caption that names the wrong method as best; a metric
defined as a percentage in one place and a raw count in another; a symbol used with two meanings.

### Visual and layout quality

Check the compiled PDF when it exists:

- figures are readable and close to their first text reference,
- captions state the figure or table message,
- tables have aligned columns and consistent precision,
- no orphaned section headers or awkward page breaks,
- labels, legends, colors, and panel markers remain legible.

### Format and submission hygiene

Check format risks before any submission-ready claim:

- page count follows the active venue rule,
- references, appendix, supplement, checklist material, and required statements are in the confirmed
  order,
- anonymous submissions do not expose author identity,
- duplicate labels, undefined references, undefined citations, and overfull main-body content are
  resolved or reported,
- every intended section file is referenced by `main.tex`,
- footnotes are removed or converted to inline text; file names and code artifacts
  (`\texttt{*.json}`, `\texttt{*.py}`) are replaced with descriptive natural language,
- disclosure is clean: `scripts/audit_draft.py` reports no internal-identifier or do-not-disclose
  errors against `paper/.disclosure.yaml`, and heuristic internal-token warnings are resolved or
  justified.

## Claim Support Rule

Every major claim, especially in Abstract and Introduction, needs claim support from experiments,
verified source text, or confirmed evidence. Unsupported claims must be weakened, removed, or moved
to future work.

## Post-Draft Review Loop (Two Rounds, Both Default On)

Run two review rounds after the full draft exists and before the final submission-readiness gate.
**Both rounds are on by default.** Round 1 is the writing agent's own review; Round 2 is an
independent review by a separate reviewer subagent. Do not skip Round 2 unless the user explicitly
opts out or the runtime has no subagent capability (use the Fallback below).

For a Full Draft request, this loop is part of producing the draft itself: the first draft returned to
the user is the reviewed-and-revised draft, not the pre-review draft.

### Round 1 — Self-review

1. Read both the LaTeX source and the compiled PDF when the PDF exists.
2. Review the eight dimensions above as a defect-finding pass, not a confirmation pass.
3. Grade findings as `blocking / high / medium / low`.
4. Fix every `blocking` finding and every `high` finding that can be fixed without inventing
   evidence, citations, results, or venue rules.
5. Recompile after review-driven edits when compile tools are available.
6. Carry only the current LaTeX source and compiled PDF into Round 2. Keep unresolved findings for
   the final summary, but do not feed them to the Round 2 reviewer (see Reviewer Independence).

### Round 2 — Independent subagent review

After Round 1 fixes and recompile, launch a **reviewer subagent in a fresh, isolated context** using
the runtime's subagent/Task facility. The subagent reads the artifacts itself and judges them as a
skeptical reviewer; it does not see how the draft was written or what Round 1 changed.

1. Spawn the reviewer subagent with the Reviewer Independence inputs below. Give it the reviewer
   role, the venue/format constraints, the paths to the LaTeX source directory and the compiled PDF,
   and the eight review dimensions plus the `blocking / high / medium / low` scale. Also give it the
   **Section-Method Adherence** task: pass the relevant section guides
   (`references/sections/<section>.md`) as a neutral rubric and ask it to verify per section whether
   the required moves are present (e.g., Method: motivation/design/advantage per module; Experiments:
   setup + each claim mapped to an experiment; Related Work: grouped with a distinction per group;
   all sections: one paragraph one message, topic-sentence first). A section guide is a rubric, not
   author framing, so passing it does not break independence.
2. The subagent runs a fresh skeptical defect-finding pass over the current LaTeX source and PDF,
   grades each finding, **independently re-verifies the section-method moves against the guides**, and
   **returns the findings only — it does not edit the paper.**
3. The writing agent receives the findings and fixes every `blocking` finding and every feasible
   `high` finding within writing-only scope. Recompile after edits when compile tools are available.
4. Stop after this round. Do not open a third review round by default. If a `blocking` or `high`
   finding cannot be fixed without inventing evidence, citations, results, or venue rules, record it
   as an unresolved finding instead of looping — a finding that needs more rounds depends on missing
   evidence, not on more reviewing.

#### Reviewer Independence (what the subagent gets)

The reviewer must form its own assessment from the primary artifacts, so its context stays clean.

- **Pass to the subagent:** the reviewer role/persona, the review objective and the eight
  dimensions, the `blocking / high / medium / low` scale, venue/format constraints (venue, page
  limit, anonymity, required statements), file paths (the `paper/` LaTeX source directory and the
  compiled PDF), and the relevant section guides (`references/sections/<section>.md`) as a neutral
  required-moves rubric. Tell it to read the files itself.
- **Do NOT pass:** the writing agent's Section Plan / Paragraph Plan / claim-evidence map, the Round 1
  finding list or fix summary, any "what changed since the draft" notes, or any framing that asserts
  the paper's strengths. A reviewer told what was fixed tends to confirm the fix instead of
  re-testing it, and a reviewer fed the author's framing inherits the author's blind spots.

#### Subagent scope guard

The subagent is a **writing reviewer**, bound by the same writing-only scope as this skill. It may
read code, results, and data files only to check that the writing matches them. It MUST NOT run or
modify experiments, invent or alter evidence/results/citations, or change the research idea. It
reports findings; the writing agent applies only writing-scoped fixes (prose, structure,
claim-evidence alignment, figures/tables presentation, format).

#### Fallback (no subagent capability)

If the runtime cannot launch a subagent, run Round 2 as a fresh self second-pass instead: judge the
revised draft only from its current LaTeX source and compiled PDF, and do not re-read or carry
forward Round 1's finding list, fix summary, or "what changed" notes. Treat it as a fresh skeptical
read with the same scale and the same fix rules.

### Risk scale

Use `blocking` for false claims, unsupported headline claims, broken compilation, misleading
figures/tables, major format violations, citation failures, venue-readiness claims that cannot be
verified, or internal data inconsistencies (a number that disagrees across abstract/text/table, a
delta that the reported numbers do not support, or a headline number with no backing in the body). Use `high` for likely rejection risks that can be fixed in prose, structure, evidence
alignment, or layout. Use `medium` for clarity and presentation issues that reduce trust. Use `low`
for cosmetic issues.

## Output Requirement

Use this output only when the user explicitly asks for a review report or when a blocking issue
must be shown. During the full workflow, run both review rounds as part of the workflow before
returning the final draft; the rounds are internal process, not a user-facing deliverable by default.

By default, report review results as a concise terminal or conversation summary only. Do not print
the full review table or full defect list in the terminal unless the user explicitly asks for it.
Write `paper/review-report.md` only when the user explicitly asks for a review report, when review
is the primary task, or when `blocking` or unresolved `high` findings remain after revision. Do not
create `paper/review-report.md` for a routine internal review when no user-facing review is needed.

When showing full-paper review, produce:

| Dimension | Reviewer question | Current answer | Risk level | Required revision |
|---|---|---|---|---|

Use these eight dimensions:

1. Contribution,
2. Writing clarity,
3. Experimental strength,
4. Evaluation completeness,
5. Method design soundness,
6. Internal consistency,
7. Visual and layout quality,
8. Format and submission hygiene.

Risk level vocabulary: `blocking`, `high`, `medium`, `low`.

For a Paper Review Report, use:

- Verdict: `pass / revise / blocked`
- Blocking findings
- High-priority revisions
- Format/PDF findings
- Actions taken
- Remaining risks

When a risk comes from missing evidence, state whether the fix is prose revision, claim weakening,
citation verification, additional analysis, or a new experiment.
