# Draft Revision Workflow

Use this workflow when the user provides existing prose and asks to revise, rewrite, polish,
diagnose, review, compress, weaken claims, or improve flow.

Default behavior: load the fewest references needed for the requested grain. Do not generate a
Writing Policy, Paper Framework, or output file unless the user explicitly asks.

## State Machine

```text
Existing draft / section / paragraph / sentence / caption
  -> identify grain and task
  -> load minimal references
  -> section drafting protocol when revising a section
  -> rewrite / polish / diagnose / review
  -> output revised text + necessary notes
```

## State 1: Identify Grain And Task

Identify the object:

- full draft,
- section,
- paragraph,
- sentence,
- caption,
- title,
- abstract,
- figure/table description.

Identify the task:

- grammar polish,
- academic tone,
- clarity improvement,
- flow diagnosis,
- claim weakening,
- caption rewrite,
- compression,
- reviewer-friendly rewrite,
- structural rewrite,
- whole-paper review.

Use the global Clarification Protocol in `../SKILL.md` for missing context. If missing context can
be handled conservatively, proceed and state assumptions briefly. Ask only when the missing
information changes the revision strategy.

## State 2: Load Minimal References

Choose references by grain:

| Grain / task | Required references | Conditional references |
|---|---|---|
| Sentence polish | none beyond this workflow | `../references/style/user-style-profile.md`, `../references/style/reference-paper-learning.md`, `../references/checks/claim-evidence.md` |
| Paragraph polish / flow | `../references/sections/paragraph-flow.md` | style references, `../references/checks/claim-evidence.md` |
| Caption rewrite | `../references/sections/figures-and-tables.md` | `../references/checks/claim-evidence.md`, `../references/checks/metric-design.md` |
| Abstract rewrite | `../references/sections/abstract.md`, `../references/sections/paragraph-flow.md` | `../references/sections/examples/abstract.md`, `../references/checks/claim-evidence.md`, `../references/checks/reviewer-risk.md` |
| Introduction rewrite | `../references/sections/introduction.md`, `../references/sections/paragraph-flow.md` | `../references/sections/examples/introduction.md`, `../references/checks/claim-evidence.md`, `../references/checks/reviewer-risk.md` |
| Related Work rewrite | `../references/sections/related-work.md`, `../references/sections/paragraph-flow.md` | `../references/sections/examples/related-work.md`, `../references/checks/citation-integrity.md` |
| Method rewrite | `../references/sections/method.md`, `../references/sections/paragraph-flow.md` | `../references/sections/examples/method.md`, `../references/sections/figures-and-tables.md`, `../references/checks/reviewer-risk.md` |
| Experiments rewrite | `../references/sections/experiments.md`, `../references/sections/paragraph-flow.md` | `../references/sections/examples/experiments.md`, `../references/checks/metric-design.md`, `../references/sections/figures-and-tables.md`, `../references/checks/reviewer-risk.md` |
| Conclusion rewrite | `../references/sections/conclusion.md`, `../references/sections/paragraph-flow.md` | `../references/checks/claim-evidence.md` |
| Whole-paper review | `../references/sections/paper-review.md`, `../references/sections/paragraph-flow.md` | `../references/checks/reviewer-risk.md`, `../references/checks/claim-evidence.md`, `../references/checks/metric-design.md`, `../references/checks/citation-integrity.md` |

For section rewrites, load matching example files only when the section guide points to a specific
example, the section structure is uncertain, or the user asks for examples. Learn structure, not
phrasing.

Do not load full-draft-only references by default:

- `workflows/full-draft.md`
- venue profiles
- archetype profiles
- domain profiles

Load those only when the user asks to revise using project evidence, the confirmed Writing Policy,
the confirmed Paper Framework, venue-specific expectations, paper type, or domain-specific
evidence pressure.

## State 3: Section Drafting Protocol

Use this protocol for any section-level draft or rewrite, including Abstract, Introduction, Related
Work, Method, Experiments, Conclusion, and section-scale figure/table narration. Do not use it for
sentence, paragraph, caption, light compression, local claim weakening, or local flow diagnosis.

For section-level work, build these internal artifacts before writing prose:

1. `Section Plan`: 3-7 bullets that state the section's argument in order.
2. `Paragraph Plan`: each paragraph has one role, one message, evidence or source, and risk.
3. `Claim-Evidence Check`: every major claim maps to supplied evidence, citation support, or a
   weakened/removed claim.
4. `Risk Notes`: unresolved evidence, citation, metric, terminology, or reviewer-facing risks.

Apply these section-writing rules:

- One paragraph has one message; the first sentence should state the paragraph role or claim.
- Key terms must be self-contained and stable across the revised text.
- Sentence-to-sentence flow must show cause, contrast, consequence, refinement, example, or evidence.
- For Method subsections, include motivation, design, and technical advantage when applicable.
- For Abstract and Introduction, map central claims to available evidence before strengthening them.
- For Experiments, make metric direction, denominator, comparison setting, and result scope explicit.
- For figures/tables, treat the visual as evidence: one visual has one message and a caption that
  states the supported claim.

After drafting the section, run reverse outlining internally:

1. section thesis,
2. each paragraph topic sentence,
3. evidence or explanation under each paragraph,
4. mapping from paragraph to section thesis,
5. unsupported or mixed-message paragraphs to revise, split, weaken, or remove.

Do not show the internal Section Plan, Paragraph Plan, reverse outline, or claim-evidence map by default.
Show them only when the user asks, when the task is explicitly diagnostic/review-oriented, or when a
blocking evidence/citation risk must be surfaced.

## State 4: Decide Whether To Show A Plan

No visible formal plan for:

- sentence polish,
- paragraph polish,
- caption rewrite,
- light compression,
- local claim weakening,
- local flow diagnosis.

Generate a compact local plan before rewriting when the task is broad enough that the user may need
to see the intended change before reading the revision:

- rewriting a whole section,
- changing section structure,
- revising a full draft,
- reorganizing figures/tables,
- changing contribution or claim framing,
- responding to reviewer-style risks.

The local plan should be brief:

```markdown
## Revision Plan
- Object:
- Goal:
- Main issue:
- Structure change:
- Claims to preserve:
- Claims to weaken:
- Evidence / citation risk:
```

Do not save this plan to a file by default.

For section-level revisions, the visible plan may summarize the internal `Section Plan`, main
structure change, claims to preserve, claims to weaken, and evidence/citation risk. Keep paragraph
plans and claim-evidence maps internal unless the user asks.

## State 5: Revise Or Diagnose

For sentence-level tasks, output:

- revised sentence,
- one short note only if the change affects claim strength or meaning.

For paragraph-level tasks, output:

- revised paragraph,
- interaction-language explanation when useful,
- parallel-language version only when requested or needed to verify intent,
- main change notes only if needed.

For caption tasks, output:

- improved caption,
- figure message,
- reviewer concern only if relevant.

For section-level tasks, output:

- revised section,
- concise interaction-language revision notes,
- parallel-language version only when requested or needed to verify intent,
- remaining evidence/citation risks.

Do not output the Section Plan, Paragraph Plan, reverse outline, or full claim-evidence map
by default. Include them only when requested, when the user asked for diagnosis/review, or when a
blocking risk affects the revision.

For whole-paper review, output:

- concise findings ordered by severity,
- required revision,
- evidence/citation risks.

## Revision Rules

- Preserve the user's intended meaning unless explicitly asked to change it.
- Improve logic, not just wording, when the task asks for rewrite or flow.
- Keep one paragraph to one message.
- Make topic sentences clear.
- Keep paragraph roles explicit internally during section-level work.
- Keep terminology consistent.
- Do not strengthen unsupported claims.
- Mark unverified citations as `not verified`.
- Do not fabricate citations, results, or experimental details.
- Do not output Writing Policy, Paper Framework, or full review tables unless requested.
