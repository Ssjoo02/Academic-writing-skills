# paper-figure MCP

Narrow MCP display helper for the `academic-writing` skill.

It is intentionally limited to display-specific work:

- classify a figure/table idea into a plot, schematic, picture, or table route,
- write a FigureSpec JSON skeleton from built-in templates for pipeline/framework, architecture,
  taxonomy, benchmark-construction, or a minimal custom diagram,
- validate and render a medium-complexity FigureSpec JSON to an editable academic-style SVG diagram,
- write a Picture Brief Markdown file with a Direct Image Prompt for AI-generated paper pictures.

It does not write paper prose, invent claims, invent results, manage the paper workflow, or call an
image-generation API. The Picture Brief records the renderer route; a separate renderer or current
agent performs the actual picture generation.

## Register

```bash
codex mcp add paper-figure -- python3 /path/to/academic-writing/mcp-servers/paper-figure/server.py
```

Use the equivalent MCP registration command for non-Codex hosts.

## Tools

- `classify_figure`
- `write_figurespec_skeleton` — accepts optional `template` values: `pipeline`, `architecture`,
  `taxonomy`, `benchmark`, or `minimal`.
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
to a configured picture renderer such as GPT-image or Gemini.

`write_picture_brief` auto-detects the picture route from standard provider environment variables:
`GEMINI_API_KEY` (Gemini), `OPENAI_API_KEY` (GPT-image), and optional `GEMINI_IMAGE_MODEL` /
`OPENAI_IMAGE_MODEL` / `GEMINI_BASE_URL` / `OPENAI_BASE_URL`. It records the route in the brief;
it does not call the provider.

`render_figurespec` renders a FigureSpec JSON (produced by `write_figurespec_skeleton` or
hand-written) to a clean academic-style SVG diagram with nodes, edges, groups, and arrowheads.
Use it for deterministic architecture, pipeline, workflow, and taxonomy schematics after verifying
the spec's semantic accuracy. For dense, non-rectilinear, or heavily annotated diagrams, use the
FigureSpec output as a starting point and move to hand-authored SVG or TikZ rather than forcing the
basic renderer.
