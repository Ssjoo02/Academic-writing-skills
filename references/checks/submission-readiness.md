# Final Submission Readiness Check

Use this check after the full draft exists and before calling a paper
submission-ready. This is a gate, not a writing guide.

## Verdicts

| Verdict | Meaning | Allowed claim |
|---|---|---|
| PASS | Required checks ran and no blocker remains | may call the draft submission-ready for the checked venue |
| BLOCKED | A required check failed or a required artifact is missing | do not declare submission-ready |
| OPEN_DECISION | A venue rule, source verification, or compile environment cannot be confirmed | do not declare submission-ready |

## Compile And PDF Checks

- Compile from the generated `paper/` directory when `latexmk` or `pdflatex` is available.
- Treat LaTeX errors, missing PDF output, undefined references or citations, and unresolved
  `% EVIDENCE_NEEDED`, `% CITATION_NEEDED`, `% FIGURE_NEEDED`, or `% TABLE_NEEDED` markers as
  `BLOCKED`.
- Check page count, file size when the venue has a limit, and font embedding when PDF tools such as
  `pdfinfo` or `pdffonts` are available.
- If compilation or PDF tools are unavailable, report `OPEN_DECISION`; do not declare
  submission-ready.

## Executable Format Checks

When the compiled `paper/` and a build log exist, run these objective checks instead of judging
layout by eye. Recompile once with file/line errors first so warnings can be located:

```bash
cd paper && latexmk -pdf -file-line-error -interaction=nonstopmode -halt-on-error main.tex
```

### Main-content page count vs venue limit

```bash
python3 scripts/audit_draft.py paper --max-content-pages <limit>
```

Use the confirmed venue content-page limit (or the generic 6-8 main-text page drafting budget, with
8 as the upper bound). The audit uses the compiled PDF and is venue-aware: it stops counting at the
first post-matter heading — `References` or a venue-excluded section such as `Limitations`,
`Acknowledgments`, or `Ethics` — so a correctly placed dedicated Limitations/Ethics section does not
consume the budget, but main text (or a limitations block left inside a body section) that reaches a
page makes that page count. Over the limit is `BLOCKED`; if the venue rule is unconfirmed, report
`OPEN_DECISION`. Do not rely on the Paper Framework's planned page arithmetic alone; compiled PDF
page count is authoritative.

### Required-section and limitations placement

```bash
python3 scripts/audit_draft.py paper --max-content-pages <limit>
```

`audit_draft.py` also flags Limitations placement. Treat as `BLOCKED`: a Limitations-titled
`\subsection`, `\paragraph`, or `\textbf{Limitations …}` run-in sitting inside a body section
(e.g. Experiments) instead of the dedicated section, and more than one dedicated `\section{Limitations}`.
For venues that require a Limitations section (ACL family), a missing `\section{Limitations}` is
`BLOCKED`; confirm it exists after Conclusion and before References.

### Duplicate labels (hard block)

```bash
grep -Rho "\\\\label{[^}]*}" paper/main.tex paper/sections 2>/dev/null | sort | uniq -d
```

Any duplicate label is `BLOCKED` (it silently breaks `\ref`/`\eqref`).

### Overfull boxes, classified by location

```bash
grep -n "Overfull \\\\hbox" paper/main.log 2>/dev/null
```

Classify each warning by the source file in the `-file-line-error` log:

- Main body (files before `\appendix`): any overfull is `BLOCKED`.
- Appendix: `BLOCKED` only if it exceeds ~10pt or visibly clips.
- Bibliography (`*.bbl`, `references.bib`): `BLOCKED` only if it exceeds ~20pt or visibly clips.
- Underfull boxes stay warnings unless they create visible layout damage.

If a warning cannot be classified, treat it as main body and fix it. Fix main-body overfulls by
rephrasing prose, splitting equations (`aligned`/`split`/`multline`), or resizing tables — do not
hide them with a global `\sloppy`.

### Undefined references and citations

```bash
grep -nE "undefined (references|citations)|Citation .* undefined|Reference .* undefined" paper/main.log 2>/dev/null
```

Any undefined reference or citation is `BLOCKED`.

### Visual spot check

After the objective checks pass, open the PDF pages that contain figures and tables and confirm
nothing crosses a margin, overlaps a column, or has clipped labels. Revise and recompile before a
`PASS`.

## Citation And Bibliography Checks

- Run the static citation audit before a submission-ready claim, with a paper-type citation floor:

```bash
python3 scripts/audit_citations.py paper --min-citations <floor>
```

- Set `<floor>` by paper type (benchmark / survey / method papers cite broadly — ~25–30; otherwise
  ~12–15). The low-coverage result is a warning, not a `BLOCKED` (references do not count toward the
  page limit), but a warning here means Related Work / Introduction likely under-cite or a named
  model/dataset/baseline/framework is uncited — resolve before claiming submission-ready.
- If drafting in another project, use this skill's script path and pass that project's `paper/`
  directory.
- Treat any citation audit error (not the coverage warning) as `BLOCKED`.
- A citation added through search is verified only when metadata and claim support were checked and
  recorded in `paper/citation-evidence.md`.
- When a needed source is not in project materials, run targeted live lookup against stable sources
  such as DBLP, CrossRef, arXiv, DOI landing pages, publisher pages, Semantic Scholar, or OpenAlex.
  If targeted live lookup is unavailable or inconclusive, leave the citation unresolved and report
  `OPEN_DECISION`.

## Venue And Format Checks

- Use the active venue profile and any user-provided official instructions for page counting,
  anonymity, required statements, checklist material, file size, and post-main order.
- Do not invent venue rules. If the current venue rule is not confirmed, report `OPEN_DECISION`.
- Treat author identity leakage in anonymous submissions, page-budget overflow, missing required
  statements, and wrong appendix or supplement placement as `BLOCKED`.
- Appendix or supplement checks must follow the confirmed venue rule; do not hard-code one global
  LaTeX order.

## Journal Submission Elements (Venue Kind: journal)

When the confirmed venue is a journal, run the journal-specific element checks in
`references/checks/journal-submission-elements.md` in addition to the venue/format
checks above. Treat the following as `BLOCKED`:

- A required mandatory statement is missing (Data Availability, Code Availability,
  Author Contributions, Competing Interests, Funding/Acknowledgments, Ethics, or
  Reporting Summary) when it applies to the paper.
- Display items (figures + tables) exceed the venue cap, or supplementary/extended
  material is in the wrong tier for the venue.
- Methods placement contradicts the venue's post-main order (inline vs after
  references).
- Body length exceeds the venue word/page cap, including the case where the cap
  includes Methods; or the abstract exceeds its word/character cap.

Report `OPEN_DECISION` for any journal rule that cannot be confirmed because the
venue card marks it `not verified`. For conference venues, skip this section.

## Evidence And Claim Checks

- Treat unsupported central claims, numeric results without traceable evidence, and abstract or
  introduction claims not supported later in the paper as `BLOCKED`.
- If a claim can be made true by narrowing the wording, narrow it before returning the draft.
- If raw evidence is missing or inconsistent, mark `OPEN_DECISION` or `BLOCKED` according to
  whether user input can resolve the issue.

## Orphan Section Check

- Check that intended section `.tex` files are referenced from `main.tex`.
- Treat stale or orphan section files as `BLOCKED` when they contain paper content that could make
  the returned draft misleading.

## Submission Readiness Report

Return a compact report with:

- Verdict: `PASS / BLOCKED / OPEN_DECISION`
- Compile/PDF status
- Format check status (page count, duplicate labels, overfull boxes, undefined refs/cites)
- Citation audit status
- Venue/format status
- Evidence/claim status
- Blocking risks
- Open decisions
- Next fixes

Do not declare submission-ready unless the verdict is `PASS`.
