# Paragraph Flow Principles

Use this file with any section-specific guide when drafting or revising prose.

## One Paragraph, One Message

Each paragraph should have one clear message: one paragraph, one message. The first sentence should usually state the paragraph
role or claim.

## Salience And Compression

Good prose is not "everything that is true about the work"; it is the **load-bearing** subset,
ordered and weighted by importance. Most messy, unfocused drafts fail here, not at grammar.

**Lead with the point.** A paragraph's skeleton is: first sentence = the point (claim/result/decision),
middle = support, last = reinforcement or transition. **Never bury the key sentence in the middle.**
If the first sentence could be deleted without the reader losing the paragraph's purpose, rewrite it.

**Allocate length by importance, not by availability.** Spend words in proportion to how much a piece
of content supports the paper's claims. Novel, surprising, or claim-supporting content earns its own
paragraph; routine setup earns a clause; content that supports no claim is cut. Do not give an
unimportant fact a full sentence just because it is true.

**Do not enumerate in the body.** Inventories, taxonomies, per-category counts, exhaustive option
lists, and "one item per line" content do **not** belong in running text. In the body, *mention them
in one stroke* — name the dimension, give the total, and call out only the **few salient or novel
members** — then send the **full list to a table or the appendix**. Reasons to put a list in the
body must be argumentative, never completeness:

- ❌ Listing every category `V1…Vn` / `H1…Hn` with its definition and task count in the body.
- ✅ "We define `n` attack vectors spanning `<short span>`; two are novel (`Vk`, `Vj`, motivated
  below). The full taxonomy with per-vector counts is in Table/Appendix X."

**Every number must carry a point.** A statistic in prose must support a claim (a total, a dominant
or surprising share, a headline coverage figure). Numbers that merely report "how much of each kind"
go in a table; never transcribe a table into sentences.

**The "so what?" test.** For each paragraph, sentence, or list, ask: if I delete this, does any claim
weaken? If not, compress it to a clause or cut it. Compress by removing repeated background,
collapsing redundant statements, and keeping only the one or two most decision-relevant points —
never by deleting the actual claim or its key evidence.

### Before / After (enumeration)

Before (body text, unfocused — full inventory inline):

```text
We define 8 attack vectors. V1 -- Email: ... 20 tasks. V2 -- SMS: ... 16 tasks.
V3 -- Web: ... 21 tasks. [... five more bullets ...]
```

After (body text, one stroke + pointer; full list moved to a table/appendix):

```text
The benchmark spans 8 attack vectors, from common text channels (email, SMS, web, social,
work chat, files) to two we introduce: compromised tool return values (V7) and visual-payload
injection (V8). Table~\ref{tab:vectors} lists all vectors with per-vector task counts.
```

## Before Drafting

Create a `Paragraph Plan` before writing prose. First list the key points as bullet points, then
order them by dependency (what must the reader understand first?). Convert the ordered bullets into
paragraphs, one per message.

| Paragraph | Role | Message | Evidence / Source | Risk |
|---|---|---|---|---|

The plan should make the section thesis visible and prevent mixed-message paragraphs.

## Sentence-Level Rules

- **Keep sentences short.** If a sentence spans more than three clauses, split it.
- **Concrete before abstract.** State the specific finding or design first, then generalize.
  Avoid opening with abstract claims the reader hasn't been prepared for.
- **Avoid jargon when plain words work.** Use technical terms only when they carry precise
  meaning needed for the argument.
- **Prefer active voice for your own work.** "We propose / We evaluate / We find." Passive
  voice is acceptable for describing existing work or objective experimental outcomes.
- **Avoid ambiguous relative pronouns.** Replace bare "this / these / that / which" with
  explicit noun phrases: "this method / this result / this limitation / these baselines."
  The reader must never guess what a pronoun refers to.

## Continuation Markers

At the start of each section and subsection, tell the reader what follows and how it connects
to the contribution or previous section. These markers act as re-entry points for skim readers
and reviewers. Example: "Having established the benchmark design, we now evaluate each baseline
against the three criteria defined in §2."

## Sentence-To-Sentence Flow

Every sentence should connect to the previous sentence through one of these relations:

- cause,
- contrast,
- consequence,
- refinement,
- example,
- evidence.

If the relation is unclear, revise the transition or split the paragraph.

## Reverse Outline Check

After drafting a section, write:

1. section thesis,
2. each paragraph topic sentence,
3. evidence or explanation under each paragraph,
4. evidence mapping from paragraph to source or experiment,
5. mapping from paragraph to section thesis.

Remove or revise paragraphs that do not map cleanly.

## During Revision

Revise paragraph-by-paragraph. For each paragraph, preserve supported claims, weaken unsupported
claims, and keep one role per paragraph. If one paragraph contains multiple roles, split it.

Required revision note:

| Paragraph | Original role | Revised role | Main change | Reason |
|---|---|---|---|---|

## Term Consistency

Define important terms before reuse. Keep names stable across the paper unless the Writing Policy
explicitly changes terminology.

## Self-Check

- Does this paragraph have one message?
- Is the first sentence doing the right job (the point, not buried)?
- Is length allocated by importance — no full sentence wasted on a non-load-bearing fact?
- Are inventories/taxonomies/per-category counts mentioned in one stroke with the full list in a
  table or appendix, rather than enumerated in the body?
- Does every number in prose support a claim, instead of transcribing a table?
- Are nouns self-contained for an external reader?
- Does each sentence have a visible relation to the previous one?
