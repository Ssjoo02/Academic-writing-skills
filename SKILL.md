---
name: academic-writing
description: Generate and use a policy-driven research paper writing strategy before drafting or revising academic papers. Use when planning, drafting, revising, or reviewing a research paper with venue, paper type, domain evidence adapter, metric, claim-evidence, citation, reviewer-risk, or style constraints.
---

# Academic Writing — Router

This skill is split into two layers:

- A **static layer** under `static/` that holds versioned, reusable content fragments (core stance,
  gates, contract, and per-workflow execution rules).
- A **dynamic layer** (this file plus `manifest.yaml`) that detects the request's axes and loads
  only the fragments needed for the current job. Section guides, check references, figure
  references, domain adapters, and style references stay in on-demand `references/`.

Do not apply the writing logic from memory or from this router. Always load fragments from disk
as described below.

## ⚠️ Critical Decision Rule: STOP, NEVER GUESS

**This is the highest-priority rule. It overrides all other instructions, defaults, and
autonomy settings. No exception.**

When the agent encounters a decision that materially affects the paper — paper identity,
core claims, evidence boundary, key terminology, evidence conflicts, venue/template,
section structure, or figure/table plan — **it MUST stop and ask the user. It MUST NOT
guess, assume, default silently, or proceed past the decision.**

Read `static/core/gates.md` for the full rule. The short version: if guessing wrong would
cause a false claim, wrong paper identity, wrong terminology, or a large downstream rewrite,
**stop. Ask. Wait for the user's explicit response. Do not proceed without it.**

## Routing Protocol

Follow these steps every time the skill is invoked.

### 1. Load the manifest and the core layer

Read [manifest.yaml](manifest.yaml). It declares the axes (`workflow`, `paper_type`, `venue`),
the allowed values, and the file paths each value maps to.

Also read every file listed under `always_load` (`static/core/stance.md`, `static/core/gates.md`,
`static/core/contract.md`). These hold the language policy, integrity rules, output contract,
checkpoint semantics, clarification protocol, and writing contract that apply to every writing job.

### 2. Route into exactly one workflow — a blocking gate

Decide the `workflow` value from the user request. Every request must be routed before work begins:

- **Full Draft Workflow** (`full-draft`): user provides a workspace or asks for a complete first
  paper draft from project materials.
- **Draft Revision Workflow** (`draft-revision`): user provides existing prose and asks to rewrite,
  polish, diagnose, review, compress, weaken claims, or improve flow.

If ambiguous, ask one concise question and stop. After routing, load the matching workflow fragment
(`static/fragments/workflow/full-draft.md` or `static/fragments/workflow/draft-revision.md`).

### 3. Detect the remaining axis values

For each remaining axis in the manifest (`paper_type`, `venue`), decide the value using the
manifest's `detect:` hint and the user's input. State the detected values briefly so the user can
correct them cheaply.

- `paper_type`: infer from workspace evidence; default to `generic`.
- `venue`: from user input or workspace; default to `generic`. Ask about venue at most once.

### 4. Build the paper using the loaded material

Apply the loaded material in this order:

1. Core contract (`static/core/contract.md`) — establish paper identity, core story, claims and
   evidence boundary, key terminology, and venue/format contract.
2. Core gates (`static/core/gates.md`) — apply clarification protocol, mandatory checkpoint
   semantics, and workflow planning protocol.
3. Core stance (`static/core/stance.md`) — apply language policy, output contract, and integrity
   rules.
4. Workflow fragment — the exclusive full-draft or draft-revision execution rules.

The Full Draft Workflow follows this state machine:
`workspace → Writing Policy → user confirmation → Paper Framework → user confirmation → paper/`

### 5. Reach for references only when needed

The files under `references/` are deep references, not defaults. Open them on demand per the
`references.on_demand` table in the manifest. Typical triggers:

- Section drafting → `references/sections/<section>.md`
- Figure/table planning → `references/figures/figure-planning.md`
- Claim-evidence audit → `references/checks/claim-evidence.md`
- Citation integrity → `references/checks/citation-integrity.md`
- Domain-specific evidence pressure → `references/domains/<domain>.md`
- Template selection → `templates/index.md`
- Reference paper style learning → `references/style/reference-paper-learning.md`

## Why This Split

- The static layer is versioned and reviewable. Adding a new paper type or venue is one new file
  plus one manifest line.
- The dynamic layer keeps each invocation cheap: only the fragments relevant to this draft enter
  context, instead of 1000+ lines of workflow and reference text.
- The router itself is short on purpose. Update fragments and references, not this file, when
  adding scope.
- This structure mirrors `nature-writing` and `nature-figure` so the pattern is consistent across
  the skill ecosystem.
