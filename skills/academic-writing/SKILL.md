---
name: academic-writing
description: Use when planning, drafting, revising, or reviewing a research paper with venue, paper type, metric, claim-evidence, citation, reviewer-risk, or style constraints. Also trigger on general paper-writing requests even without these terms, such as writing a paper from scratch, drafting or restructuring a section, building a paper outline/framework, polishing or compressing prose, and Chinese phrasings like 学术写作、科研写作、论文写作、写论文、写paper、写一篇论文、帮我写论文、搭论文框架、起草论文、润色论文、改论文、写引言/摘要/方法/实验/相关工作/结论、投稿前自检. This skill writes and revises the paper only; it does not run experiments or conduct research. It is the hub of the academic-writing collection and delegates figures/tables to academic-figure, citations to academic-citation, and review/audits to academic-review.
---

# Academic Writing — Hub Router

This is the **hub** skill of the academic-writing collection. It owns the writing pipeline
(Writing Policy → Paper Framework → LaTeX project → section drafting) and the two confirmation
gates. It **delegates** three self-contained subsystems to sibling skills:

- **`academic-figure`** — every figure and table (planning, plot style, table design, QA).
- **`academic-citation`** — every searched/written/verified citation and the bibliography audit.
- **`academic-review`** — the closing review, static audits, submission-readiness, and the
  before-returning checklist.

The hub states *when* to invoke each sibling; the sibling owns *how*. Rules are not duplicated across
skills. The cross-skill shared layer lives at the repository root under `_shared/` (core stance,
gates, contract; bundled venue templates; paper-type and venue cards; shared
claim-evidence / metric-design rubrics).

## ⚠️ Scope: Writing Only, Never Research

**This skill produces and revises the paper artifact. It does not do the research.**
It improves expression, structure, section logic, claim-evidence alignment, reviewer-facing
framing, figures/tables presentation, and venue fit. It MUST NOT, by default:

- change the research idea, problem scope, method mechanism, or contribution type,
- design, run, or modify experiments, environments, or pipelines,
- invent, alter, or "improve" results, numbers, baselines, ablations, or datasets,
- fabricate citations, evidence, or experimental detail.

If correct writing appears to require changing any of the above, **stop and ask the user**.
If the user asks to "optimize the idea" or change results while using this skill, get explicit
confirmation first; otherwise mark the issue as an `idea-level risk` or `needs evidence` (the
status vocabulary is defined in `../../_shared/core/contract.md`), keep the wording bounded, and
continue with writing-only revisions. Unsupported claims are weakened, marked `needs evidence`, or
removed — never strengthened to look better.

This skill is split into two layers:

- A **static layer** under `static/` that holds versioned, reusable content fragments (the workflow
  orchestrators and per-stage execution rules). Cross-skill core fragments live in `../../_shared/`.
- A **dynamic layer** (this file plus `manifest.yaml`) that detects the request's axes and loads
  only the fragments needed for the current job. Section guides, check references,
  and style references stay in on-demand `references/` (this skill) or `../../_shared/`.

Do not apply the writing logic from memory or from this router. Always load fragments from disk
as described below.

## ⚠️ Critical Decision Rule: STOP, NEVER GUESS

**This is the highest-priority rule. It overrides all other instructions, defaults, and
autonomy settings. No exception.**

When the agent encounters a decision that materially affects the paper — paper identity,
core claims, evidence boundary, key terminology, evidence conflicts, venue/template,
section structure, or figure/table plan — **it MUST stop and ask the user. It MUST NOT
guess, assume, default silently, or proceed past the decision.**

Read `../../_shared/core/gates.md` for the full rule. The short version: if guessing wrong would
cause a false claim, wrong paper identity, wrong terminology, or a large downstream rewrite,
**stop. Ask. Wait for the user's explicit response. Do not proceed without it.**

## ⚠️ Interaction Language Rule

**The agent MUST mirror the user's interaction language in all conversation output.**
This includes clarification questions, checkpoint summaries, status updates, policy
rationale, self-review notes, and warnings. If the user writes in Chinese (with or
without English technical terms), the agent MUST respond in Chinese. File paths,
LaTeX commands, BibTeX keys, and code remain in their original language. Paper prose
remains English by default. This rule is not overridden by any other policy.

## ⚠️ Bundled Venue Templates — Local First, Do Not Web-Fetch

**This collection ships the official LaTeX templates for the major venues, preloaded in
`../../_shared/templates/`** (ICLR, NeurIPS, ICML, ACL/EMNLP/NAACL, CVPR, AAAI, IJCAI,
ACM/KDD/WWW/SIGIR/CHI/UIST, IEEE conference/journal, JMLR, plus a generic draft template). When a
target venue maps to a preloaded template (see `../../_shared/templates/index.md`), the agent
**MUST use the local file directly and MUST NOT search the web or download a template** to obtain
venue formatting. Web/official-source fetch is a **last resort only** for a venue with no preloaded
mapping and no user-provided template. The official-source URLs in venue cards and in
`maintenance/venue-template-sources.md` are **provenance records for maintenance, not draft-time
fetch instructions**. Do not infer venue formatting from memory either — use the bundled template.

## Routing Protocol

Follow these steps every time the skill is invoked.

### 1. Load the manifest and the core layer

Read [manifest.yaml](manifest.yaml). It declares the axes (`workflow`, `venue_kind`, `venue`,
`paper_type`), the allowed values, and the file paths each value maps to.

Also read every file listed under `always_load` (`../../_shared/core/stance.md`,
`../../_shared/core/gates.md`, `../../_shared/core/contract.md`). These hold the language policy,
integrity rules, output contract, checkpoint semantics, clarification protocol, and writing contract
that apply to every writing job.

### 2. Route into exactly one workflow — a blocking gate

Decide the `workflow` value from the user request. Every request must be routed before work begins:

- **Full Draft Workflow** (`full-draft`): user provides a workspace or asks for a complete first
  paper draft from project materials.
- **Draft Revision Workflow** (`draft-revision`): user provides existing prose and asks to rewrite,
  polish, diagnose, review, compress, weaken claims, or improve flow.

If ambiguous, ask one concise question and stop. After routing, load the matching workflow fragment
(`static/workflow/full-draft.md` or `static/workflow/draft-revision.md`). The full-draft orchestrator
loads its per-stage fragments under `static/workflow/stages/` as each stage is reached.

### 3. Detect the remaining axis values in order

For each remaining axis in the manifest (`venue_kind`, `venue`, `paper_type`), decide the value
using the manifest's `detect:` hint and the user's input. State the detected values briefly so the
user can correct them cheaply.

- `venue_kind`: decide first. Use `journal` only when the user explicitly says journal article /
  journal paper or names a journal venue/track. If the user does not explicitly specify journal,
  default to `conference`.
- `venue`: decide second. For unspecified conference targets, use `generic`; for explicit but
  unmodeled journal targets, use `journal`.
- `paper_type`: decide third from workspace evidence and the selected `venue_kind`; conference uses
  the top-level paper-type profiles, journal uses `journal-*` profiles. Default to `generic` for
  conference and `journal-generic` for journal.

### 4. Build the paper using the loaded material

Apply the loaded material in this order:

1. Core contract (`../../_shared/core/contract.md`) — establish paper identity, core story, claims
   and evidence boundary, key terminology, and venue/format contract.
2. Core gates (`../../_shared/core/gates.md`) — apply clarification protocol, mandatory checkpoint
   semantics, and workflow planning protocol.
3. Core stance (`../../_shared/core/stance.md`) — apply language policy, output contract, and
   integrity rules.
4. Workflow fragment — the full-draft orchestrator (+ its stage fragments) or the draft-revision
   execution rules.

The Full Draft Workflow follows this state machine:
`workspace → Writing Policy → user confirmation → Paper Framework → user confirmation → paper/`

### 5. Delegate the three subsystems

When a stage needs figures/tables, citations, or the closing review, load the sibling skill and
follow it. Do not reproduce its rules here:

- Any figure or table → **`academic-figure`** (`../academic-figure/SKILL.md`).
- Any searched/written/verified citation, or the bibliography audit → **`academic-citation`**
  (`../academic-citation/SKILL.md`).
- The first complete `paper/` draft exists → **`academic-review`** (`../academic-review/SKILL.md`):
  Draft Completion Review Gate, Final Static Audits, Submission Readiness, Before-Returning check.
  The draft returned to the user is always the reviewed-and-revised draft.

### 6. Reach for hub references only when needed

The files under `references/` are deep references, not defaults. Open them on demand per the
`references.on_demand` table in the manifest. Typical triggers:

- Section drafting → `references/sections/<section>.md` + `references/sections/paragraph-flow.md`
- **Journal section overlays (only when `Venue Kind` is `journal`):** the
  `references/sections/journal/` overlays layer on top of the base section guides; the journal
  paper-type profiles live at `../../_shared/paper-types/journal/`; the journal vs conference posture
  at `../../_shared/venues/journal-vs-conference.md`. When `Venue Kind` is `conference`, do not load
  any `references/sections/journal/` file.
- Writing Policy workspace logic/evidence audit → `references/checks/workspace-logic-audit.md`
- Claim strength / metric rubric → `../../_shared/checks/claim-evidence.md`,
  `../../_shared/checks/metric-design.md`
- Drafting or polishing English prose → `references/style/copyediting-standard.md`
- Template selection → `../../_shared/templates/index.md` (preloaded official templates are the
  **first and authoritative** source; do not web-search/download when the venue maps to a bundled
  template)

## Why This Split

- The hub owns orchestration and writing-body rules; the three sibling skills own self-contained,
  independently invokable subsystems (just make a figure, just review, just check citations).
- The static layer is versioned and reviewable. Adding a new paper type or venue is one new file in
  `../../_shared/` plus one manifest line.
- The dynamic layer keeps each invocation cheap: only the fragments relevant to this draft and the
  delegated subsystem enter context, instead of one 1000+ line monolith.
- The router itself is short on purpose. Update fragments, references, and sibling skills — not this
  file — when adding scope.
