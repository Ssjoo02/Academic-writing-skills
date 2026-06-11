# Stage: Section Drafting

Load this fragment for the per-section drafting loop of the Full Draft Workflow. It pairs with
`stages/latex-project.md` (project setup), the **`academic-figure`** skill (every figure/table), the
**`academic-citation`** skill (every searched/written/verified citation and the bibliography), and
the **`academic-review`** skill (the closing gates).

Load section references when drafting each section:

| Draft target | Load |
|---|---|
| Abstract | `references/sections/abstract.md`, `references/sections/paragraph-flow.md` |
| Introduction | `references/sections/introduction.md`, `references/sections/paragraph-flow.md` |
| Related Work | `references/sections/related-work.md`, `references/sections/paragraph-flow.md`; invoke the `academic-citation` skill when citation support matters |
| Method / System | `references/sections/method.md`, `references/sections/paragraph-flow.md`; invoke the `academic-figure` skill when figures or tables are used |
| Experiments / Evaluation | `references/sections/experiments.md`, `references/sections/paragraph-flow.md`; load `_shared/checks/metric-design.md` and invoke the `academic-figure` skill when figures or tables are used |
| Demo / Application | `references/sections/demo-application.md`, `references/sections/paragraph-flow.md` |
| Conclusion / Limitations | `references/sections/conclusion.md`, `references/sections/paragraph-flow.md` |

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
   A taxonomy subsection must not become a glossary-style definition list (`V1 -- ...`, `H1 -- ...`);
   its prose must explain the design rationale, category boundaries, and the few salient/novel
   members, while complete definitions/counts live in a table or appendix.
5. Run reverse outlining and claim-evidence mapping internally; revise before moving to next section.
6. **Section-Method Adherence check (mandatory, internal).** Before moving on, verify the section
   against the *required moves* of its section guide and mark each `present` / `missing`. A `missing`
   move means the section is not done — revise until resolved or record it as an explicit risk.
   Minimum required moves per section:
   - **Method** (`references/sections/method.md`): every module subsection has motivation, design,
     and technical advantage; an overview/section-map opens the section; terms defined before use.
   - **Experiments** (`references/sections/experiments.md`): setup (datasets/metrics/baselines/
     protocol) stated; each contribution claim has a matching experiment; metric direction and scope
     explicit. **No Limitations block lives here** — limitations do not belong in a numbered body
     section; route them to the dedicated Limitations section below.
   - **Introduction / Abstract**: problem -> challenge/gap -> insight/contribution -> advantage -> evidence
     chain present; contribution sentences state purpose or advantage, not only a component list;
     central claims map to available evidence; contributions preview maps to later sections.
   - **Related Work**: organized by topic group with a stated distinction per group, not a citation
     list. **Every named prior method, benchmark, dataset, model, or framework carries a `\cite`**;
     proactively run the targeted citation search (see Citation Search Trigger) rather than leaving
     groups thin.
   - **Conclusion** (`references/sections/conclusion.md`): short close (contribution → strongest
     evidence → scoped implication); **no full limitations paragraph** (it has its own section) and
     **no future-impact / "we hope …" promotional closer**; no new claims or citations. Over-long or
     four-paragraph conclusions with a vision closer are a `missing`/over-length defect — compress.
   - **Limitations** (when the venue expects one, e.g. ACL family): a single dedicated
     `\section{Limitations}` after Conclusion holds all limitations, ~120–180 words, 3–4 material
     points; it is the only home for limitations in the paper (do not also enumerate them in
     Experiments or Conclusion).
   - **All sections**: one paragraph one message; first sentence states the paragraph role and
     leads with the point (not buried); stable terminology; **no taxonomy/inventory/per-category
     enumeration in the body** — such lists are mentioned in one stroke and the full list lives in a
     table or appendix; no glossary-style taxonomy subsection whose main content is one item per
     category; every prose number supports a claim rather than transcribing a table.

   Keep this check internal. Round 2 of the Post-Draft Review Gate (the independent subagent, owned by
   the `academic-review` skill) must independently re-verify these same required moves against the
   section guides — it is the external check that the self-assessment was honest.

**Non-negotiables while drafting (these hold here, not only in the rules file):** no `\footnote{}`;
no `\texttt{*.json/*.py/*.csv}` or code identifiers or local paths in prose; subsection budget (0 for
short sections, ≤4 per main section); do not add sections/subsections beyond the confirmed Framework;
**no body-text enumeration of a taxonomy/inventory/per-category counts (each `V1…Vn` / `H1…Hn` /
per-app count on its own line) — compress to one stroke in the body and move the full list to a
table or appendix; no `itemize` / `enumerate` taxonomy glossary in a body section; lead every
paragraph with its point.** This ban includes the **disguised form**: a run of `\textbf{V1 (...)}.` /
`\textbf{H1 (...)}.` bold lead-in paragraphs that define each coded member one by one is a glossary
list with the `\item` markers removed — it is forbidden in the body. **When a taxonomy table already
lists the members, do not also re-define every member in prose.** Instead: give the table a short
`Description` column (use a `tabularx` wrapping column), and in the body explain only the design
rationale, the category boundaries, and the two or three most salient/novel members in one
argumentative stroke. Put the full per-member definitions in a dedicated **appendix** subsection
(with a real lead paragraph), not in the body.

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

## Citation Search Trigger

Do not run an unbounded survey, but do not under-cite either. Run targeted citation search whenever
the draft needs external support not already covered by workspace evidence or verified `.bib`
entries. For a full draft, the following are **proactive** triggers — search for them rather than
waiting for a `% CITATION_NEEDED` to appear:

- **Related Work and Introduction background are proactive by default.** Drafting either one
  triggers targeted search for the prior methods, benchmarks, datasets, environments, and comparison
  lines they discuss; a Related Work group with one or zero citations is under-cited, not done.
- **Every named entity must be cited.** Each model, dataset, benchmark, environment, baseline, or
  taxonomy/standard framework named in the text (e.g. each evaluated model, each prior benchmark,
  any security/standard framework the taxonomy is "grounded in") needs a `\cite` to its source.
- **Citation coverage is paper-type-scaled.** Benchmark, survey, and method papers are expected to
  cite broadly; a 10-entry bibliography for such a paper is a smell. The final citation audit is run
  with a paper-type `--min-citations` floor (see the `academic-citation` skill).
- A confirmed Paper Framework names prior work that is missing from local sources.
- A necessary sentence would otherwise require `% CITATION_NEEDED`.
- The user explicitly asks to find, add, or verify references.

When any trigger fires, invoke the **`academic-citation`** skill: it owns the citation-integrity
search, verification, BibTeX completeness rules, `paper/citation-evidence.md` logging, and the
`audit_citations.py` blocking gate. References do not count toward the page limit, so breadth is
cheap; never fabricate to hit a count, and prefer weakening or removing an unsupported claim over a
guessed citation.

## Missing-Support Markers

A marker records a slot whose **underlying evidence genuinely does not exist** in the workspace and
cannot be produced by writing alone. It is a last resort, never a way to defer work the chain can do
now:

```tex
% EVIDENCE_NEEDED: <short reason>
% CITATION_NEEDED: <short reason>
% FIGURE_NEEDED: <short reason>
% TABLE_NEEDED: <short reason>
```

**A `% FIGURE_NEEDED` / `% TABLE_NEEDED` for a display item the confirmed Paper Framework Figure Plan
calls for, or a `% CITATION_NEEDED` for a claim whose source is findable, is NOT an acceptable end
state.** When the user asks for a draft, the Full Draft chain must *resolve* these in the same
session: invoke the **`academic-figure`** skill to generate every planned figure and table, and the
**`academic-citation`** skill to search and write every needed citation. Leaving them as comments and
telling the user to "complete them later" via the sibling skills is a workflow violation — the closing
`audit_draft.py` gate fails on any leftover `% *_NEEDED` marker, so such a draft cannot pass the Final
Static Audits and is not done.

A marker may survive into the returned draft **only** when the evidence is truly missing (an
experiment was never run, a result does not exist, no citable source exists). Even then, prefer
weakening or removing the unsupported claim, and list every surviving marker as a blocking risk in the
final summary — never as routine follow-up. Do not use markers as placeholders for routine prose.

## Writing Rules

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

After all sections are drafted and figures/tables/citations are in place, hand off to the
**`academic-review`** skill for the Draft Completion Review Gate, the Final Static Audits, the Final
Submission Readiness Gate, and the Before-Returning Compliance Self-Check. Do not return `paper/`
before those gates pass.
