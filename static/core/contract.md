# Writing Contract

A research paper is a structured argument, not a collection of results. Before any drafting or
framework work, establish the contract below. It defines what the paper claims, what supports
those claims, and what must stay bounded.

## ⚠️ Critical Decision Rule

**The agent MUST NOT guess any of the five contract points below.** If any point cannot be
determined from the workspace evidence, the agent MUST stop and ask the user. Guessing paper
identity, core story, claims, key terminology, or venue produces false contracts that cascade
into wrong drafts. When in doubt: **stop, ask, wait for explicit user response, then proceed.**
The full rule is in `static/core/gates.md`.

## The Five-Point Contract

Before writing any paper artifact, establish:

1. **Paper identity**: target venue, paper type, intended reader, and core research question.
   The paper type controls the evidence burden; method-paper is not a default.

2. **Core story**: problem → failure case or motivating gap → technical challenge → insight →
   proposed method/benchmark/system/study → one-sentence contribution → final takeaway.
   This chain must be complete before any section is drafted.

3. **Claims and evidence boundary**: every major claim maps to available evidence, a source trace,
   and a drafting action (state / weaken / verify / defer / avoid). Unsupported claims are
   weakened or removed. The boundary between what the paper asserts and what it leaves open
   must be explicit.

4. **Key terminology**: terms that affect the title, abstract, contribution, method identity,
   dataset/task, benchmark, metric, or system components. Each term has a definition, a source,
   a use policy, and a status. Terminology must stay stable across the paper.

5. **Venue and format contract**: target template, page/length budget, what counts toward the
   limit, required statements, post-main section order, and citation style. If the venue is
   unconfirmed, use generic_article.tex with a soft 6-8 main-text-page drafting budget and
   record that the official template is unresolved.

## Evidence Classification

Classify important sources as:

- `raw evidence`: source data, experiment logs, annotation files
- `derived statistics`: computed metrics, aggregated results
- `draft-derived candidate`: numbers or claims inferred from drafts, not source data

## Status Vocabulary

For claims and evidence: `unknown`, `supported`, `partially supported`, `needs evidence`,
`not verified`, `should avoid`.

## Source Conflict Rule

If sources conflict on counts, denominators, model names, method names, key terms, metrics,
baselines, dataset splits, protocols, venue hints, or central claims, do not smooth the
conflict over.

- If the conflict is decisive, ask the user before finalizing the Writing Policy.
- If the conflict is not decisive, record it in Open Decisions with a conservative default.
- If the user does not answer a decisive evidence conflict, avoid exact numbers or strong claims
  and mark affected claims as `partially supported`, `needs evidence`, or `not verified`.
