# Citation And Bibliography Workflow

Execution rules for searching, writing, and verifying every citation in a paper draft, and for the
blocking bibliography audit. The deep reference lives at `references/checks/citation-integrity.md`;
the mechanical gate is `scripts/audit_citations.py`.

## When To Search

Run targeted citation search whenever the draft needs external support not already covered by
workspace evidence or verified `.bib` entries. Do not run an unbounded survey, but do not under-cite
either. Proactive triggers (search rather than waiting for a `% CITATION_NEEDED`):

- Related Work and Introduction background are proactive by default — search for the prior methods,
  benchmarks, datasets, environments, and comparison lines they discuss.
- Every named entity (model, dataset, benchmark, environment, baseline, taxonomy/standard framework)
  needs a `\cite` to its source.
- A confirmed Paper Framework names prior work missing from local sources.
- A necessary sentence would otherwise require `% CITATION_NEEDED`.
- The user explicitly asks to find, add, or verify references.

Citation coverage is paper-type-scaled. Benchmark, survey, and method papers cite broadly; a 10-entry
bibliography for such a paper is a smell. The final audit is run with a paper-type `--min-citations`
floor (see below).

When searching, load `references/checks/citation-integrity.md` and run a targeted live lookup before
writing a final citation. If live search adds or changes a citation, record the source, DOI/URL, and
support judgment in `paper/citation-evidence.md`. If reliable support is not found, weaken/remove the
claim or leave `% CITATION_NEEDED: <short reason>` rather than inventing a source. References do not
count toward the page limit, so breadth is cheap — never fabricate to hit a count.

## Citation And Bibliography Rules

**Every cited source must be verified, complete, and traceable.** A draft with placeholder
authors, missing identifiers, or unverified entries is not complete. The citation audit
(`scripts/audit_citations.py`) enforces these rules mechanically — it must pass before the
draft leaves the agent's hands.

- Prefer existing workspace `.bib` files when available.
- Do not generate BibTeX from memory. Every entry must come from a trusted source (DBLP,
  CrossRef, Semantic Scholar, arXiv, publisher page) or from the user's verified `.bib`.
- **Complete author lists required.** Every BibTeX entry must list all authors by name.
  Never use `and others`, `et al.`, or similar placeholders in the `author` field. If
  the full author list is unavailable, mark the entry `% [VERIFY]` and do not cite it
  as verified.
- **Stable identifier required** for every entry published after 2000. At minimum: DOI,
  URL, or arXiv `eprint`. Conference papers without at least an arXiv link are not
  verified. An entry labeled `arXiv preprint arXiv:2025` (year substituted for ID) is
  malformed — fix or replace it.
- **Year consistency.** The citation key year (e.g., `smith2024`) must match the `year`
  field. Mismatched keys mean the entry was fabricated or botched — fix or replace.
- If no verified `.bib` entry is available, use `% CITATION_NEEDED: <short reason>`.
- If citation lookup is performed, record the source, DOI/URL, and verification status
  in `paper/citation-evidence.md`.
- Mark unverified citations as `not verified`.
- Use `\citep{}` / `\citet{}` for natbib venues; use numeric `\cite{}` for IEEE templates.
- Keep `paper/references.bib` limited to entries actually cited. Remove uncited entries.

**If any entry in `references.bib` violates these rules, the citation audit will fail.
Fix every error before returning the draft — the audit is a BLOCKING gate, not a
diagnostic.**

## Citation Audit (blocking)

Run from the paper project directory (the script is path-agnostic; pass the `paper/` directory):

```bash
python3 "<path-to-academic-citation>/scripts/audit_citations.py" paper
# with the paper-type citation floor:
python3 "<path-to-academic-citation>/scripts/audit_citations.py" paper --min-citations <floor>
```

`<floor>` is a paper-type expectation (benchmark / survey / method papers cite broadly — use ~25–30;
otherwise ~12–15); the floor raises a warning, not a hard block, because references do not consume
page budget.

**What `audit_citations.py` checks:** bibliography integrity — placeholder authors, missing required
BibTeX fields, missing DOI/URL/arXiv on modern entries, vague source labels, year-key mismatch,
uncited entries, unresolved `% CITATION_NEEDED` markers, and (with `--min-citations`) a
low-citation-coverage warning when the bibliography is thinner than the paper type expects.

**On failure:** fix every error in `references.bib` (missing authors, placeholder `and others`,
missing DOI/URL/arXiv, year-key mismatch, malformed entries, uncited entries), then **re-run the
audit**. Repeat until `PASS`. Do not return the draft while any error remains.
