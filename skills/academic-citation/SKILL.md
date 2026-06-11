---
name: academic-citation
description: Use when searching for, writing, verifying, or auditing citations and the BibTeX bibliography of a research paper — finding sources for named methods/datasets/benchmarks, completing author lists and stable identifiers (DOI/URL/arXiv), checking citation coverage, and running the blocking bibliography audit. Triggers with or without a full draft, including Chinese phrasings like 查引文、补引用、引用核对、参考文献、文献检索、bib 核查、引文审计. Part of the academic-writing collection; the academic-writing hub delegates all citation work here.
---

# Academic Citation — Router

This skill searches, writes, verifies, and audits every **citation and bibliography entry** for a
paper. It is independently invokable ("find sources for this related-work paragraph", "audit my
references.bib") and is the subsystem the **`academic-writing`** hub delegates to whenever a draft
needs citation support.

It is split into two layers:

- A **static layer** at `static/citation-workflow.md` — when to search, the citation/bibliography
  integrity rules, and how to run the blocking audit.
- A **dynamic layer** (this file + `manifest.yaml`) plus the deep reference
  `references/checks/citation-integrity.md` and the mechanical gate `scripts/audit_citations.py`.

Cross-skill stance and integrity rules live in `../../_shared/core/`. Never fabricate a citation —
weaken or mark the claim instead.

## ⚠️ Integrity

**Do not generate BibTeX from memory.** Every entry must come from a trusted source (DBLP, CrossRef,
Semantic Scholar, arXiv, publisher page) or the user's verified `.bib`. Complete author lists and a
stable identifier (DOI/URL/arXiv) are required. If reliable support is not found, weaken or remove
the claim, or leave `% CITATION_NEEDED: <reason>` — never invent a source. Mirror the user's
interaction language (`../../_shared/core/stance.md`).

## Routing protocol

1. **Load the core layer.** Read `manifest.yaml`, the `always_load` file
   (`../../_shared/core/stance.md`), and `static/citation-workflow.md`.
2. **Decide the task:** targeted search for missing support, verification of existing entries, or a
   full bibliography audit.
3. **For search/verify**, open `references/checks/citation-integrity.md` and run a targeted live
   lookup before writing any final citation; log added/changed citations and their support judgment to
   `paper/citation-evidence.md`.
4. **For the audit (blocking gate)**, run `scripts/audit_citations.py` against the paper directory and
   fix every error in `references.bib` until it reports `PASS`. The script is path-agnostic:

   ```bash
   python3 "<path-to-this-skill>/scripts/audit_citations.py" paper
   python3 "<path-to-this-skill>/scripts/audit_citations.py" paper --min-citations <floor>
   ```

## Why this split

- Citation search and bibliography integrity are a self-contained, frequently standalone task, so
  they live in their own skill with the audit script alongside.
- The hub and the `academic-review` closing gates invoke this skill rather than duplicating its rules.
