---
name: academic-writing-skills
description: Use when planning, drafting, revising, or reviewing a research paper with venue, paper type, metric, claim-evidence, citation, reviewer-risk, or style constraints. Also trigger on general paper-writing requests even without these terms, such as writing a paper from scratch, drafting or restructuring a section, building a paper outline/framework, polishing or compressing prose, making a paper figure or table, finding or auditing citations, or a pre-submission review — and Chinese phrasings like 学术写作、科研写作、论文写作、写论文、写paper、帮我写论文、搭论文框架、起草论文、润色论文、改论文、写引言/摘要/方法/实验/相关工作/结论、论文配图、画图、表格排版、查引文、补引用、审稿、投稿前自检. This collection writes and revises the paper only; it does not run experiments or conduct research.
---

# Academic-Writing-Skills — Entry Router

This is the **entry point** of the Academic-Writing-Skills collection. It does no writing
work itself. Its only job is to read the user's request and hand off to exactly one of the
four sub-skills under `skills/`, then **read and follow that sub-skill's `SKILL.md`**.

The collection is a hub plus three specialized siblings, sharing one repository-level layer:

| Sub-skill | Path | Owns |
|---|---|---|
| **`academic-writing` (hub)** | `skills/academic-writing/SKILL.md` | The writing pipeline (Writing Policy → Paper Framework → LaTeX project → section drafting) and the two confirmation gates. Delegates figures/citations/review to the siblings. |
| `academic-figure` | `skills/academic-figure/SKILL.md` | Every figure and table (planning, plot style, table design, QA gate). |
| `academic-citation` | `skills/academic-citation/SKILL.md` | Every searched/written/verified citation and the BibTeX audit. |
| `academic-review` | `skills/academic-review/SKILL.md` | Closing review, static audits, submission-readiness, before-returning checklist. |

The cross-skill shared layer lives at the collection root under `_shared/` (core stance, gates,
contract; bundled venue templates; paper-type and venue cards; shared rubrics). It is **not** a
skill — the sub-skills load it by relative path (`../../_shared/...`).

## Routing — pick exactly one sub-skill, then follow its SKILL.md

Do not apply any writing, figure, citation, or review logic from memory or from this router.
Resolve the request to one sub-skill and open its `SKILL.md`:

1. **Write or revise a paper, or any section** — full first draft from a workspace; Writing Policy
   or Paper Framework only; rewrite/polish/diagnose/compress/weaken-claims/improve-flow on existing
   prose → **read and follow `skills/academic-writing/SKILL.md`** (the hub). This is also the
   default when the request spans multiple subsystems or is ambiguous, because the hub already
   delegates to the other three at the right time.
2. **Only a figure or table** — "make this plot", "fix this table's layout", 画个图/做表 →
   **read and follow `skills/academic-figure/SKILL.md`** directly.
3. **Only citations / bibliography** — "find sources for X", "audit my .bib", 补引用/查引文 →
   **read and follow `skills/academic-citation/SKILL.md`** directly.
4. **Only a review / pre-submission check** — "review my paper", 审稿/投稿前自检 →
   **read and follow `skills/academic-review/SKILL.md`** directly.

When in doubt, route to the hub (`skills/academic-writing/SKILL.md`); it owns the orchestration
and will pull in the siblings as each stage needs them.

## Scope (applies to every sub-skill)

This collection produces and revises the paper artifact; it does **not** do the research. It must
not change the research idea, design or run experiments, or invent/alter results or citations. The
full scope, the STOP-never-guess decision rule, the interaction-language rule, and the integrity
rules live in `_shared/core/` and are loaded by each sub-skill — they are not restated here to keep
this router thin.
