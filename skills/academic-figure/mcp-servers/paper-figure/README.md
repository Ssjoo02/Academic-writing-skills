# paper-figure MCP

Narrow MCP helper for the `academic-writing` skill.

It is intentionally limited to figure-specific work:

- classify a figure/table idea into a generation route,
- write a simple FigureSpec JSON skeleton for architecture, pipeline, workflow, and taxonomy
  diagrams,
- render a FigureSpec JSON (from the skeleton tool or hand-written) to an editable academic-style
  SVG diagram,
- write a Picture Brief Markdown file with a Direct Image Prompt for AI-generated paper pictures.

It does not write paper prose, invent claims, invent results, or manage the paper workflow.

## Register

```bash
codex mcp add paper-figure -- python3 /path/to/academic-writing/mcp-servers/paper-figure/server.py
```

Use the equivalent MCP registration command for non-Codex hosts.

## Tools

- `classify_figure`
- `write_figurespec_skeleton`
- `write_picture_brief`
- `render_figurespec` — render a FigureSpec JSON (nodes, edges, groups) to an editable SVG diagram suitable for paper inclusion. Accepts `spec_path` (path to a FigureSpec JSON) or `spec` (inline spec object), plus `cwd`, `figure_id`, and optional `output_relpath`.

## Output Policy

The server only writes under the provided `cwd`. Recommended paths:

```text
paper/figures/specs/<figure-id>.json
paper/figures/<figure-id>.svg
paper/figures/<figure-id>.pdf
paper/figures/prompts/<figure-id>.md
paper/figures/<figure-id>.png
```

The `Direct Image Prompt` block in the brief is the exact text to copy into another AI chat or pass
to a configured image API such as GPT-image2 or Gemini.

`write_picture_brief` auto-detects the picture API from standard environment
variables: `GEMINI_API_KEY` (Gemini), `OPENAI_API_KEY` (GPT-image), and optional
`GEMINI_IMAGE_MODEL` / `OPENAI_IMAGE_MODEL` / `GEMINI_BASE_URL` / `OPENAI_BASE_URL`.
No custom-prefix environment variables are needed.

`render_figurespec` renders a FigureSpec JSON (produced by `write_figurespec_skeleton` or
hand-written) to a clean academic-style SVG diagram with nodes, edges, groups, and arrowheads.
Use it for architecture, pipeline, workflow, and taxonomy diagrams after verifying the spec's
semantic accuracy.
