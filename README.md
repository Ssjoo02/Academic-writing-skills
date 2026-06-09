# Academic Writing

Academic Writing is an agent-readable skill for building research papers from real project
materials. It works in local skill environments such as Claude Code and Codex, and can also be used
manually by any agent or researcher that can read `SKILL.md` and the referenced Markdown files.

简体中文：[README.zh-CN.md](README.zh-CN.md)

## Project Orientation

Academic Writing focuses on the manuscript-building part of research: turning experiments, notes,
figures, tables, and claims into a coherent first manuscript.

It is deliberately writing-only by default. It can improve structure, argument flow, section logic,
claim-evidence alignment, venue fit, citation hygiene, figure/table presentation, and reviewer-facing
clarity. It does not silently change the research idea, run experiments, invent results, fabricate
citations, or strengthen claims beyond the available evidence.

The skill is built around one principle:

```text
problem -> gap -> challenge -> insight -> method / study / benchmark -> evidence -> claim
```

A paper is not a collection of results. It is a defensible argument, and every major claim needs a
visible evidence boundary.

## Writing Philosophy And Influences

The writing methodology is not an in-house invention. It distills widely shared research-writing
experience, most directly the research and paper-writing guidance compiled by Sida Peng (彭思达) in
*learning_research*, together with established community advice on clear scientific writing:

- *learning_research* — Sida Peng's research notes:
  <https://github.com/pengsida/learning_research/tree/master>
- *Ten Tips for Writing CS Papers* — Sebastian Nowozin:
  <https://www.nowozin.net/sebastian/blog/ten-tips-for-writing-cs-papers-part-1.html>
- *Writing a Good Introduction* — Henning Schulzrinne (after Jim Kurose):
  <https://www.cs.columbia.edu/~hgs/etc/intro-style.html>

From these sources the skill internalizes a few load-bearing habits: state the contribution early
and classify it as *insight*, *performance*, or *capability*; treat every section as a facet of that
single contribution; prefer simple, direct language over ornate prose; and give the introduction a
clear motivation → specific problem → contribution → distinction-from-prior-work → roadmap arc. The
principle above is the spine that holds these habits together.

## Workflow

The full-manuscript workflow has three stages and two required checkpoints.

```text
Workspace Discovery
  -> Writing Policy
  -> Checkpoint 1: confirm or correct the policy
  -> Paper Framework
  -> Checkpoint 2: confirm or correct the framework
  -> First Manuscript
```

The two checkpoints are deliberate. A language model can emit a full paper in a single pass, but a
one-click draft tends to collapse toward a generic, averaged writing style that rarely matches how
the work should actually be told. The gates break that pattern: the agent must pause at the Writing
Policy and again at the Paper Framework, surface the decisions it would otherwise make silently —
paper identity, evidence boundary, venue, section structure, figure plan — and let the author confirm
or redirect them. Asking for a complete paper starts the workflow; it does not skip the gates. The
result is a manuscript that follows the author's intent rather than a templated auto-generation.

### 1. Writing Policy

The Writing Policy is the paper contract. It records the source snapshot, paper identity, core story,
claim-evidence map, key terminology, visible assets, and open decisions.

It also resolves routing in this order:

```text
venue_kind -> venue -> paper_type
```

Journal mode is used only when the user explicitly says the target is a journal article or names a
journal venue. Otherwise the skill defaults to conference mode.

### 2. Paper Framework

The Paper Framework turns the policy into a section-level plan. It defines the section list, each
section's role, paper-type profile alignment, venue/template assembly, prose budget, and display-item
budget for figures and tables.

This matters for real submissions: a double-column figure or large table consumes page space, so the
framework budgets display items before manuscript generation begins.

### 3. First Manuscript

After the framework is confirmed, the skill creates a complete LaTeX manuscript project with the
confirmed structure, template, bibliography, sections, and figure/table plan. Official venue
templates are treated as format shells: sample text and instructions are removed before manuscript
content is written.

Before the first manuscript is delivered, the skill performs its internal review and readiness pass.
Blocking writing, evidence, citation, layout, or venue-limit problems are fixed when they are within
writing scope; otherwise they are reported as unresolved risks instead of being hidden.

## Conference And Journal Support

Academic Writing ships templates and paper-type profiles for **both conference and journal**
manuscripts — it is not limited to conference papers. Conference templates include ICLR, NeurIPS,
ICML, CVPR, ACL/EMNLP/NAACL, AAAI, and IJCAI; journal targets include IEEE Transactions and JMLR,
with a generic journal profile for any journal not modeled individually. Journal mode also layers
journal-specific section overlays and submission-element checks (mandatory statements, display-item
caps, methods placement, length budgets) on top of the base writing rules.

| Case | Behavior |
| --- | --- |
| User names a conference | Load the matching venue profile when available. |
| User gives no venue | Use conference mode with a generic venue-TBD manuscript. |
| User explicitly names a journal | Use journal mode and journal paper-type profiles. |
| User gives an unmodeled journal | Use a generic journal profile and keep journal-specific fields open until verified. |

This conservative routing avoids accidentally writing a journal article when the user only asked for
a paper.

## Optional Figure Generation

Data charts are generated from project data by the current agent. For non-data paper pictures such
as teasers, conceptual illustrations, and overview images, the skill can optionally use Gemini or
GPT-image through normal API keys or relay/base-URL configuration.

If no image API is configured, the current agent can still create or assemble figures directly when
the requested figure is within scope.

## Installation

Copy the complete `academic-writing` directory. Do not copy only `SKILL.md`; the skill depends on
`manifest.yaml`, `static/`, `references/`, `templates/`, and supporting scripts.

### Claude Code

User-level install:

```bash
mkdir -p ~/.claude/skills
cp -R /path/to/academic-writing ~/.claude/skills/
```

Project-local install:

```bash
mkdir -p your-paper-repo/.claude/skills
cp -R /path/to/academic-writing your-paper-repo/.claude/skills/
```

Restart Claude Code after installing or updating the skill.

### Codex

User-level install:

```bash
mkdir -p ~/.codex/skills
cp -R /path/to/academic-writing ~/.codex/skills/
```

If you use a custom `$CODEX_HOME`, place the directory under `$CODEX_HOME/skills/` instead.

### Other Agents Or Manual Use

Keep the directory structure intact and read `SKILL.md` first. When it points to `static/`,
`references/`, or `templates/`, resolve those paths inside the same `academic-writing` directory.
Load only the files needed for the current task.

## Example Requests

```text
Use academic-writing to build a first manuscript from this workspace for EMNLP.
Use academic-writing to write only the Writing Policy first.
Use academic-writing to build the Paper Framework after I confirm the policy.
Use academic-writing to revise this Introduction for ACL-style clarity.
Use academic-writing to prepare a journal manuscript targeting JMLR.
Use academic-writing to review this manuscript before submission.
```

## Scope

Academic Writing helps produce a cleaner, more defensible manuscript, but it does not guarantee
acceptance. It will not fabricate evidence, hide unsupported claims, or turn missing experiments into
confident prose. When the evidence is incomplete, the manuscript should say less, not pretend more.
