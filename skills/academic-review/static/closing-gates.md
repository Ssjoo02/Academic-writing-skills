# Closing Gates

The mandatory closing sequence that runs after the first complete `paper/` draft exists and before
any draft is returned to the user. It applies regardless of how the Full Draft stage was entered
(linear flow or re-entry). These gates are owned by this `academic-review` skill; the
`academic-writing` hub hands off to them.

Order: **Draft Completion Review Gate → Final Static Audits → Final Submission Readiness Gate →
Before-Returning Compliance Self-Check.**

## Draft Completion Review Gate

This gate starts as soon as the first complete `paper/` draft exists: `main.tex`, all planned
`sections/*.tex`, intended figures/tables, `references.bib`, and post-main material are assembled.
Load `references/sections/paper-review.md` immediately at this point. Do not wait for the user to ask for review.
Do not ask whether to run review, and do not return the just-written draft before this
gate completes. The first draft returned to the user is the reviewed-and-revised draft.

Run the two-round Post-Draft Review Loop from `references/sections/paper-review.md` automatically:

- **Round 1 (self-review):** read the LaTeX source and compiled PDF when available, run a skeptical
  defect-finding pass over the eight dimensions (including internal consistency — front-to-back data
  and claim agreement). **Before prose-level praise or cleanup, verify the compiled content-page
  count against the active limit; any over-limit draft is a `blocking` review finding.** Fix every `blocking` finding and every feasible
  `high` finding within writing-only scope. Recompile after review-driven edits when compile tools
  are available.
- **Round 2 (independent subagent review):** after Round 1 fixes and recompile, launch a reviewer
  subagent in a fresh, isolated context per the Reviewer Independence rules in `paper-review.md`.
  Pass only the reviewer role, venue/format constraints **including the numeric content-page limit
  and Limitations placement rule**, review dimensions, relevant section guides as neutral
  required-move rubrics, and paths to the current `paper/` LaTeX source and compiled PDF.
  Do not pass section plans, paragraph plans, Round 1 findings, fix summaries, or author framing.
  The reviewer returns findings only; the writing agent fixes every `blocking` finding and every
  feasible `high` finding within writing-only scope, then recompiles when tools are available.

Skip Round 2 only if the user explicitly opts out. If the runtime cannot launch a subagent, run Round
2 as the fresh self second-pass fallback described in `paper-review.md`.

After this gate, continue to the Final Static Audits and Final Submission Readiness Gate. If review
edits create citation, format, page-budget, layout, or compile changes, the later audits judge the
reviewed-and-revised draft, not the pre-review draft.

Return only a concise Paper Review Report summary in the terminal or conversation when the user asks
for a review, when review is the primary task, or when material risks remain. Do not print the full
review table or full defect list in the terminal unless the user explicitly asks for it. Write
`paper/review-report.md` only in those same cases; do not create it for a routine clean internal
review.

## Final Static Audits — BLOCKING GATE

**This gate is not optional. Skipping it, running it and ignoring failures, or returning
a draft before the audits pass is a workflow violation. The agent MUST run both scripts and
the output of both MUST be `PASS`.**

Both audit scripts are path-agnostic — they take the `paper/` directory as an argument and do not
depend on where they are installed. `audit_draft.py` ships with this `academic-review` skill;
`audit_citations.py` ships with the `academic-citation` skill. Resolve each script's absolute path
from its skill checkout, then run both:

```bash
python3 "<path-to-academic-citation>/scripts/audit_citations.py" paper
python3 "<path-to-academic-review>/scripts/audit_draft.py" paper --framework writing-policies/<paper-slug>-paper-framework.md
```

If drafting in another project (paper is not in CWD), pass the absolute path to that
project's `paper/` directory.

**The content page budget is a blocking gate, not an optional extra.** Whenever the venue has a
content page limit (every modeled venue does; the conference fallback is a soft 8-page upper bound),
run the page-budget audit with the limit bound in the confirmed Paper Framework, and run the citation
audit with the paper-type citation floor:

```bash
python3 "<path-to-academic-review>/scripts/audit_draft.py" paper --framework writing-policies/<paper-slug>-paper-framework.md --max-content-pages <limit>
python3 "<path-to-academic-citation>/scripts/audit_citations.py" paper --min-citations <floor>
```

`<limit>` is the confirmed venue content-page limit (ACL long 8 / short 4; generic fallback 8). The
audit is venue-aware: it stops counting at the first post-matter heading (References, or a
venue-excluded section such as Limitations / Acknowledgments / Ethics), so a correctly placed
`\section{Limitations}` is not counted against the limit. `<floor>` is a paper-type expectation
(benchmark / survey / method papers cite broadly — use ~25–30; otherwise ~12–15); the floor raises a
warning, not a hard block, because references do not consume page budget.

**If the page budget is exceeded, do not return the draft — compress, then recompile and re-audit.**
Apply the compression ladder in order, cheapest first:

1. **Fix Limitations placement first.** Move every limitations paragraph/run-in into the single
   dedicated `\section{Limitations}` when the venue excludes that section from content pages (ACL
   family). This reclaims counted pages and fixes placement. For venues that do not require
   pre-reference Limitations and allow appendices, a compressed Limitations appendix section is an
   allowed overflow tradeoff. For ACL-family venues, do **not** move required Limitations to the
   appendix unless the current official instructions explicitly allow it.
2. Cut the Conclusion to a short close (drop any limitations paragraph and any future-impact closer).
3. Merge over-budget subsections (≤4 per section) and demote single-paragraph steps to
   `\paragraph{}` run-ins.
4. Move per-vector / per-harm / per-category enumerations into a table and keep only load-bearing
   numbers in prose.
5. Compress support and compress-first sections named in the confirmed Core Section Budget before
   touching primary-core or evidence-core sections.
6. Move non-essential detail, full taxonomies, full protocol listings, extended examples, and
   secondary result matrices to the appendix or supplement only when the active venue permits that
   movement and those pages do not count against the content limit.
7. If the paper still exceeds the limit and the only remaining cut would push a core section below
   its Minimum floor, stop and return to the Paper Framework checkpoint for an explicit scope,
   venue, or floor tradeoff.

Overflow is a blocking defect even when the Paper Framework's planned arithmetic was within the
limit — the compiled PDF is authoritative.

**How to handle audit failures:**

- `audit_citations.py` reports errors → **fix every error in `references.bib`** (missing
  authors, placeholder `and others`, missing DOI/URL/arXiv, year-key mismatch, malformed
  entries, uncited entries). Then **re-run the audit**. Repeat until `PASS`. (See the
  `academic-citation` skill for the full rule set.)
- `audit_draft.py` reports errors → **fix every error in the LaTeX source** (footnotes,
  file/code artifacts, leftover `% *_NEEDED` markers, duplicate labels, overfull pages,
  unresolved rendered references such as `Table ??` / `Figure ??`, invalid LaTeX section
  environments such as `\end{section}`, misplaced/duplicated or over-long Limitations units,
  Framework Figure Plan alignment failures (planned figures/tables missing from `paper/`, picture
  figures missing a Picture Brief or rendered artifact, `latex_includes.tex` entries that say
  `not yet generated`), content-page overflow, and disclosure leaks — internal identifiers that should use a display name,
  or do-not-disclose entities that appear in prose). For
  a misplaced Limitations unit, move it into the venue-correct Limitations home: the dedicated
  pre-reference section for ACL-family venues, or a compressed appendix section only when the active
  venue permits it; for content-page overflow, apply the compression ladder above (limitations
  placement → conclusion trim → subsection merge → enumerations to tables → appendix/supplement when
  permitted). For a disclosure leak,
  apply the Naming Map (rename to the public display name) or remove the do-not-disclose mention
  (including any negation/exclusion phrasing); do not edit `paper/.disclosure.yaml` to silence a true
  leak. Then **re-run the audit**. Repeat until `PASS`.
- **Do not return the draft while any audit reports errors.** A draft with audit failures
  is incomplete. Fix, re-run, pass, then return.
- Paste the audit result lines into the internal check log so the user can verify.

**What `audit_draft.py` checks:** mechanical writing rules — footnotes, file/code artifacts, local
paths, subsection budget, duplicate labels, input consistency, unresolved rendered references,
undefined references/citations, invalid LaTeX section environments, leftover markers,
Limitations placement (no Limitations-titled subsection/paragraph/`\textbf` run-in inside a body
section; at most one dedicated `\section{Limitations}`), Limitations length, venue-aware
content-page budget (counting stops at the first post-matter heading, so a dedicated
Limitations/Ethics section is excluded), and
Framework alignment when `--framework` is provided (planned display items from the confirmed Paper
Framework must materialize as artifacts and section insertions; picture figures must have prompt
briefs plus rendered output; incomplete registry comments are errors), and
the disclosure check (internal identifiers and do-not-disclose entities listed in
`paper/.disclosure.yaml`, plus a heuristic warning for internal-looking identifier tokens even when
no list is present).

## Before Returning

Internally check: paragraph flow, section alignment, figure/table placement, Abstract/Introduction
consistency, Introduction claim support in Experiments, Method and Experiments correspondence,
Related Work positioning, terminology, missing citations, conclusion overclaiming, venue page
counting, post-main section order, required statements/checklists, appendix/supplement handling,
anonymity-sensitive locations, **front-to-back data consistency (the same metric reads the same in
abstract/text/table/caption; deltas and "average over N" match the reported numbers; every headline
number is backed in the body),** and skeptical reviewer risk.

Run `scripts/check_compile_env.py` (it ships in this `academic-review` skill) to decide the compile
path — do not guess whether compilation is possible:

- **Compile available (exit 0):** compile the draft with the reported command (`latexmk -pdf main.tex`
  when available) and run the applicable content-page audit on the compiled PDF before returning. For
  page-limited venues, a draft whose main text exceeds the limit is not complete, even if the Paper
  Framework's planned budget was within the limit.
- **Compile unavailable (exit 1):** you MUST tell the user explicitly that the PDF could not be
  compiled in this environment, list the missing tools the script reported, and state that the
  page-budget, overfull, and float-layout gates ran static-only. Record this in the Submission
  Readiness Report's compile/PDF status as a blocking-or-open risk — never a silent pass.

Do not call the draft clean or submission-ready unless template, citation, evidence, page-budget, and
compilation risks are resolved or explicitly surfaced to the user.

**Compliance Self-Check (Before Returning) — complete before declaring the draft done.** Answer each
item yes/no and paste the evidence. **Any "no" means the draft is not done — fix it first.**
This check is MANDATORY and cannot be skipped.

**⛔ BLOCKING GATE — Static Audits (must pass before anything else):**
1. Did I run `audit_citations.py` and does it report `PASS`?  (Paste result. **If any error,
   fix every one in `references.bib` and re-run. Do not proceed past this item while errors
   remain. A draft with citation audit failures is not complete.**)
2. Did I run `audit_draft.py --framework <confirmed-framework>` (with `--max-content-pages <limit>` when a page limit exists)
   and does it report `PASS`?  (Paste result. **If any error, fix and re-run. Do not proceed
   while errors remain.**)

**Mandatory Gates:**
3. Did I load `references/sections/paper-review.md` immediately after the first complete `paper/`
   draft existed and run **both** review rounds (Round 1 self + Round 2 independent subagent), per
   the Draft Completion Review Gate, before any draft was returned to the user?
4. Did I load `references/checks/submission-readiness.md` and produce the Submission Readiness Report?
5. For every drafted section, did the `academic-writing` hub run the Section-Method Adherence check,
   with no `missing` move left unresolved (re-verified independently in Round 2 here)?
6. Does the structure still match the confirmed Paper Framework (section list, subsection budget),
   with no silently introduced sections or subsections?
7. Did the `academic-figure` skill apply its Display Review Gate for every generated figure?
7b. Does `paper/framework-execution-report.md` show every main-paper Figure Plan item from the
   confirmed Framework as generated, inserted in the planned section, and QA-passed, with no
   `not yet generated` registry entries?
8. If the draft has an appendix, did I inspect its compiled pages and confirm it is **substantive,
   not sparse, and in order** — every appendix section has a real lead paragraph (not a `Table~N
   provides ...` pointer); floats appear **in section order** under their heading (no bare `[h]`
   placement that defers and reorders across the separate figure/table queues); no wide single-column
   float overflows into the next column; and no `see supplementary material` stub stands in for
   content that exists? (Apply the `academic-figure` skill's Table Handling rule 11 /
   `figures-and-tables.md` "The appendix has the opposite failure".)

**Load receipt:** in the internal check, list which mandatory references were loaded
(`paper-review.md`, the `academic-figure` figure-planning reference, `submission-readiness.md`,
figure-sizing (conference or journal), plus every section guide used). A mandatory gate whose
reference was never loaded counts as a failed check, not a pass.

## Final Submission Readiness Gate

For a complete `paper/` draft, load `references/checks/submission-readiness.md` before returning
any submission-ready claim. Produce a compact Submission Readiness Report with verdict
`PASS / BLOCKED / OPEN_DECISION`, compile/PDF status, citation audit status, venue/format status,
evidence/claim status, blocking risks, open decisions, and next fixes. Do not call a draft
submission-ready when the gate is `BLOCKED` or `OPEN_DECISION`.

When `venue_kind=journal`, also run `references/checks/journal-submission-elements.md` as part of
this gate (mandatory statements, display-item caps/tiers, methods placement, and word/length
budget) and fold its verdicts into the report.

Return a concise interaction-language summary listing generated files and any blocking risks.
