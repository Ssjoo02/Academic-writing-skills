# Academic Writing

**Academic Writing** is a skill focused on academic paper writing. It is designed to generate complete manuscript drafts that follow the format requirements of specific conferences or journals, and can be used in local skill environments such as Claude Code and Codex.

中文: [README.md](README.md)

## Use Cases

Academic Writing is designed for the **paper construction stage** of the research workflow: turning experimental results, research notes, figures, evidence, and claims into a complete, well-structured, and logically coherent paper draft.

By default, it only handles writing-related tasks and does not change the research itself. In other words, it can help improve paper structure, argumentation flow, section logic, claim-evidence alignment, venue fit, citation hygiene, figure/table presentation, and reviewer-facing clarity. However, it will not silently modify the research idea, run experiments, fabricate results, invent citations, or overstate claims that lack sufficient evidence.

This skill is suitable for the following scenarios:

- **You have partial experimental results and want to write a paper draft**: The experiments are complete or partially complete, and you already have results and research notes that need to be organized into a complete and coherent manuscript draft.
- **You already have a draft and want to polish or rewrite it**: Revise, restructure, or rewrite sections such as the Introduction, Method, or Experiments, or polish the paper according to the style of a specific venue.
- **You need a manuscript for a specific venue**: You have a target conference or journal, such as EMNLP, NeurIPS, or JMLR, and need to organize the paper according to its template, page budget, and submission requirements.
- **You want a step-by-step writing workflow**: Generate only the Writing Policy or Paper Framework first, then continue to full drafting after confirming the paper identity, evidence boundaries, and section structure.
- **You want a pre-submission check**: Review an existing manuscript before submission and identify potential risks related to evidence, citations, formatting, and venue limits.
- **You need to switch between conference and journal modes**: Organize the paper under either conference or journal mode, including journal-specific section overlays and submission requirement checks.

The core premise of this skill is:

```text
Problem -> Gap -> Challenge -> Insight -> Method / Study / Benchmark -> Evidence -> Claim
```

A paper is not a pile of results, but a defensible chain of argument. Every major claim must have a clear evidence boundary.

## Writing Philosophy and References

The writing approach of this skill is distilled from widely recognized research writing practices. The most direct source of inspiration is the research and paper-writing experience summarized in *learning_research* by Peng Sida, combined with several classic pieces of scientific writing advice:

- *learning_research* — Peng Sida’s research experience:  
  <https://github.com/pengsida/learning_research/tree/master>
- *Ten Tips for Writing CS Papers* — Sebastian Nowozin:  
  <https://www.nowozin.net/sebastian/blog/ten-tips-for-writing-cs-papers-part-1.html>
- *Writing a Good Introduction* — Henning Schulzrinne, adapted from Jim Kurose:  
  <https://www.cs.columbia.edu/~hgs/etc/intro-style.html>

Our goal is to help AI learn practical and realistic paper-writing experience, so that the generated papers better match the writing habits and expression style of real researchers.

## Core Workflow

The full manuscript drafting workflow consists of three stages and two mandatory checkpoints:

```text
Workspace Discovery
  -> Writing Policy
  -> Checkpoint 1: Confirm or revise the policy
  -> Paper Framework
  -> Checkpoint 2: Confirm or revise the framework
  -> Manuscript Draft
```

To avoid the common problem that “one-click generated” drafts do not match real paper-writing habits, Academic Writing introduces two checkpoints before generating a complete manuscript draft. The agent must stop at the Writing Policy and Paper Framework stages, respectively, and expose decisions that might otherwise be made silently, including paper identity, evidence boundaries, target venue, section structure, and figure/table plans.

Therefore, when a user asks to “write a full paper,” the request only starts the workflow; it does not skip these two checkpoints. The final output should be a manuscript draft built around the author’s own research logic, rather than a templated automatic product.

### 1. Writing Policy

The Writing Policy is the writing contract for the paper. It records the source snapshot, paper identity, core story, claim-evidence map, key terminology, visible assets, and open decisions.

It is recommended to specify the target conference or journal at the beginning. If no venue is specified, the skill defaults to a generic conference-mode template.

### 2. Paper Framework

The skill includes multiple paper-type profiles for common paper structures and writing strategies. These profiles cover section organization, section goals, and content planning, helping prevent the AI’s writing from becoming too scattered.

The Paper Framework turns the Writing Policy into a section-level plan. It defines the section list, the core content of each section, venue/template assembly, body-text budget, and the display-item budget for figures and tables. Users can adjust and confirm the Paper Framework before moving on to full drafting.

### 3. Manuscript Draft

After the user confirms the Paper Framework, the skill creates a complete LaTeX paper project, including the confirmed structure, template, citations, sections, and figure/table plan.

Official venue templates are used only as formatting shells: sample text and instructional content are removed before the paper content is written in.

Before delivery, the draft goes through an internal review and readiness pass.

## Conference and Journal Support

Academic Writing includes templates and paper-type profiles for both conferences and journals. It is not limited to conference papers.

Conference templates cover ICLR, NeurIPS, ICML, CVPR, ACL, EMNLP, NAACL, AAAI, IJCAI, and more. Journal support includes IEEE Transactions, JMLR, and a generic journal profile for journals that are not separately modeled.

| Scenario | Behavior |
| --- | --- |
| The user explicitly names a conference | Load the corresponding venue profile if available. |
| The user does not specify a venue | Default to conference mode and mark the venue as generic / venue TBD. |
| The user explicitly names a journal | Use journal mode and journal paper-type profiles. |
| The user names an unsupported journal | Use the generic journal profile and keep journal-specific fields as open decisions. |

This conservative routing prevents the system from mistakenly organizing a paper as a journal manuscript when the user simply says “write a paper.”

## Installation

Please copy the entire directory instead of copying only `SKILL.md`, because this skill depends on `manifest.yaml`, `static/`, `references/`, `templates/`, and supporting scripts.

**Clone the repo**

```bash
git clone https://github.com/Ssjoo02/Academic-writing-skills
cd Academic-writing-skills
```

### 1. Codex

Copy the skill to `$CODEX_HOME/skills/`:

```bash
mkdir -p "$CODEX_HOME/skills"
cp -R Academic-writing-skills "$CODEX_HOME/skills/academic-writing"
```

Example usage:

```text
Use academic-writing to revise my paper's Introduction.
```

### 2. CC / Claude Code

Both global installation and project-level installation are supported.

Global installation:

```bash
mkdir -p "$HOME/.claude/skills"
cp -R Academic-writing-skills "$HOME/.claude/skills/academic-writing"
```

Project-level installation:

```bash
mkdir -p .claude/skills
cp -R Academic-writing-skills .claude/skills/academic-writing
```

After installation, restart Claude Code and explicitly mention this skill in your prompt, for example:

```text
Please use the academic-writing skill to revise my Introduction.
```

## Figure Generation

Data figures, such as bar charts, line charts, radar charts, heatmaps, scatter plots, and tables, are generated directly by the current agent from project data and do not require additional configuration.

For non-data paper visuals such as teasers, conceptual figures, and overview images, the skill can optionally connect to Gemini or GPT-image models.

If no image-generation API is configured, the current agent will draw the figure by default. If an image API is configured, the corresponding model will be used for rendering.

### Image Generation API Configuration

The skill automatically detects available image-generation APIs through environment variables:

- If `GEMINI_API_KEY` is set, Gemini will be used.
- If `OPENAI_API_KEY` is set, GPT-image will be used.
- If both are set, Gemini takes priority.

Standard official API keys can be used. Relay or self-hosted gateway base URLs are also supported.

**Gemini**

```bash
export GEMINI_API_KEY="your_key"

# Optional: override the base URL when using a relay or self-hosted gateway
# Default: https://generativelanguage.googleapis.com
export GEMINI_BASE_URL="https://your-relay.example.com"

# Optional: override the model
# Default: gemini-2.5-flash-image
export GEMINI_IMAGE_MODEL="gemini-2.5-flash-image"
```

**OpenAI / GPT-image**

```bash
export OPENAI_API_KEY="your_key"

# Optional: override the base URL when using a relay or self-hosted gateway
# Default: https://api.openai.com
export OPENAI_BASE_URL="https://your-relay.example.com"

# Optional: override the model
# Default: gpt-image-2
export OPENAI_IMAGE_MODEL="gpt-image-2"
```

Please configure these variables in the environment where the agent runs, such as in your shell’s `~/.bashrc` / `~/.zshrc`, or by running `export` before starting the agent. The skill will automatically read these variables when generating images, so no custom prefix variables are needed.

You can also directly tell the agent your API key and target model in the conversation, and let the agent call the corresponding API to complete figure generation.

## Compile to PDF

The skill produces a **complete, compilable LaTeX project**, located by default under the `paper/` directory. It usually contains:

```text
paper/
  main.tex
  sections/*.tex
  references.bib
  math_commands.tex
  venue template files
```

It is not just a loose `.tex` snippet, but a complete paper project. To compile it into a PDF and make layout checks effective, we recommend installing the following tools in the runtime environment:

- `latexmk` or `pdflatex`: from TeX Live / MacTeX, used to compile LaTeX;
- `pdfinfo` / `pdftotext`: from poppler-utils, used to read the compiled PDF and check page budgets.

As long as `latexmk` or `pdflatex` exists in the environment, the agent will **automatically compile the paper during the writing workflow and use the compiled PDF as the source of truth** for layout checks. These checks include, but are not limited to:

- Whether figures overflow the page;
- Whether `Overfull \hbox` appears;
- Whether tables overflow;
- Whether appendix formatting is abnormal;
- Whether the page count exceeds the target venue’s budget.

If these tools are not available in the environment, the agent will still generate the complete LaTeX source and run static audits, but it cannot verify the final PDF layout.

To compile locally:

```bash
cd paper
latexmk -pdf main.tex
```

We recommend installing the LaTeX and poppler toolchain before asking the agent to generate a complete draft. This allows layout-related gates to take effect properly.

## Example Requests

We recommend specifying the experiment directory and target conference at the beginning, for example:

```text
Use academic-writing to build a first manuscript from this workspace for EMNLP, my workspace is xxx/xxx.
Use academic-writing to revise this Introduction for ACL-style clarity, this is my paper xxx/xxx.
```

## Maintenance Note

This project is under continuous development. Everyone is welcome to try it, and any feedback, suggestions, or revision comments would be greatly appreciated.