# Academic Writing

Academic Writing is a Codex skill for turning research materials into a disciplined paper draft. It
is writing-only by default: it improves paper structure, argument flow, claim-evidence alignment,
venue fit, citation hygiene, figures/tables presentation, and final review readiness, but it does
not change the research idea, run experiments, invent results, or fabricate citations.

Chinese version: [README.zh-CN.md](README.zh-CN.md)

## What This Skill Is For

Use this skill when you want to:

- create a complete first paper draft from a project workspace;
- build a paper-level writing policy before drafting;
- turn the policy into a section-level paper framework;
- generate a LaTeX `paper/` project from the confirmed framework;
- revise, polish, compress, or review an existing paper draft;
- adapt a draft to a conference or journal venue while preserving evidence boundaries.

The skill treats a research paper as a structured argument:

```text
problem -> gap -> challenge -> insight -> method / study / benchmark -> evidence -> claim
```

Every major claim must map to visible evidence or be weakened, deferred, or marked unresolved.

## Core Workflow

The full-draft workflow has three stages and two mandatory user checkpoints.

```text
Workspace Discovery
  -> Writing Policy
  -> Checkpoint 1: user confirms or corrects the policy
  -> Paper Framework
  -> Checkpoint 2: user confirms or corrects the framework
  -> Full Draft LaTeX Project
  -> Automatic Post-Draft Review
  -> Final Audits / Submission Readiness Summary
```

The two checkpoints are deliberate. A request for a complete draft authorizes the workflow, but it
does not allow the agent to skip the Writing Policy or Paper Framework gates.

### Stage 1: Writing Policy

The Writing Policy is the compact contract for the paper. It is saved as:

```text
writing-policies/<paper-slug>-writing-policy.md
```

It records:

- source snapshot and files inspected;
- paper identity: venue kind, venue, paper type, intended reader, core research question;
- core story and one-sentence contribution;
- claims and evidence boundaries;
- key terminology and naming decisions;
- visible assets and constraints;
- open decisions that could change the paper.

The skill must decide `venue_kind` before `venue`, and `venue` before `paper_type`.

```text
venue_kind -> venue -> paper_type
```

Journal mode is selected only when the user explicitly says this is a journal article or names a
journal venue. If the user does not explicitly specify journal, the default is conference.

### Stage 2: Paper Framework

The Paper Framework is a section-level plan, not prose and not a paragraph-by-paragraph outline. It
is saved as:

```text
writing-policies/<paper-slug>-paper-framework.md
```

It defines:

- title direction and section list;
- each section's main content;
- paper-type profile adherence and any justified deviations;
- prose page budget;
- display-item page budget for figures and tables;
- template and venue assembly plan;
- unresolved blockers before drafting.

For strict conference venues, figures and tables are budgeted explicitly. A wide figure or double-
column table consumes real page space; planned prose pages alone are not enough.

### Stage 3: Full Draft

After the Paper Framework is confirmed, the skill creates a complete LaTeX project:

```text
paper/
  main.tex
  math_commands.tex
  references.bib
  sections/
  figures/
```

The draft uses the confirmed template and section plan. Official venue templates are treated as
format shells: their sample prose and instruction text are removed before drafting.

## Automatic Review And Audits

The first draft returned to the user is not the raw first pass. As soon as a complete `paper/` draft
exists, the skill automatically loads `references/sections/paper-review.md` and runs the post-draft
review gate.

The review has two rounds:

1. Self-review over contribution, clarity, evidence, evaluation completeness, method soundness,
   visuals/layout, and format hygiene.
2. Independent reviewer pass when subagent capability is available; otherwise a fresh second self-
   pass fallback.

The agent fixes every blocking issue and every feasible high-priority issue within writing-only
scope before final delivery.

Final audits are blocking gates:

```bash
python3 scripts/audit_citations.py paper
python3 scripts/audit_draft.py paper
python3 scripts/audit_draft.py paper --max-content-pages <limit>
```

The page-limit audit uses the compiled PDF. For EMNLP/ACL-style long papers, use 8 content pages;
for short papers, use 4. A draft that exceeds the confirmed venue limit is incomplete even if the
framework's planned budget looked valid.

## Conference And Journal Routing

The skill supports both conferences and journals, but the default is conservative:

- If the user explicitly names a journal or says "journal paper", use `venue_kind=journal`.
- Otherwise use `venue_kind=conference`.
- Conference paper types use `references/paper-types/*.md`.
- Journal paper types use `references/paper-types/journal/*.md`.
- Journal-only section overlays and submission-element checks are loaded only in journal mode.

This prevents a generic or unspecified request from accidentally becoming a journal article.

## Optional Picture API

For non-data paper pictures such as teasers, conceptual illustrations, or overview images, the skill
can optionally use an image-generation API. Data charts are generated directly by the current agent
with Python.

Gemini:

```bash
export GEMINI_API_KEY="..."
export GEMINI_IMAGE_MODEL="gemini-2.5-flash-image"   # optional
export GEMINI_BASE_URL="..."                          # optional, for relay
```

GPT-image:

```bash
export OPENAI_API_KEY="..."
export OPENAI_IMAGE_MODEL="gpt-image-2"              # optional
export OPENAI_BASE_URL="..."                          # optional, for relay
```

If no picture API is configured, the current agent draws or assembles the figure directly.

## Installation

Copy the complete `academic-writing` directory, not only `SKILL.md`. The skill depends on its
`manifest.yaml`, `static/`, `references/`, `templates/`, `scripts/`, and `tests/` paths.

For Codex:

```bash
mkdir -p ~/.codex/skills
cp -R /path/to/academic-writing ~/.codex/skills/
```

Start a new session after installing or updating the skill.

## Example Requests

```text
Use academic-writing to create a full draft from this workspace for EMNLP.
Use academic-writing to write the Writing Policy first; do not draft yet.
Use academic-writing to build the Paper Framework from the confirmed policy.
Use academic-writing to revise this introduction for ACL-style clarity.
Use academic-writing to review this full paper before submission.
Use academic-writing for a journal paper targeting JMLR.
```

## Scope Limits

This skill does not:

- run new experiments or modify experimental pipelines by default;
- invent numbers, citations, baselines, datasets, or claims;
- silently change the research idea, method mechanism, or evidence boundary;
- declare a draft submission-ready when compilation, citation, page-limit, or review gates fail.

When writing needs evidence that is missing, the skill weakens the claim, marks the gap, asks the
user, or reports the issue as unresolved.
