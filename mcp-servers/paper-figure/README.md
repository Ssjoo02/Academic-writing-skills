# paper-figure MCP

Narrow MCP helper for the `academic-writing` skill.

It is intentionally limited to figure-specific work:

- classify a figure/table idea into a generation route,
- write a simple FigureSpec JSON skeleton for architecture, pipeline, workflow, and taxonomy
  diagrams.
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

## Output Policy

The server only writes under the provided `cwd`. Recommended paths:

```text
paper/figures/specs/<figure-id>.json
paper/figures/prompts/<figure-id>.md
paper/figures/<figure-id>.png
```

The `Direct Image Prompt` block in the brief is the exact text to copy into another AI chat or pass
to a configured image API such as GPT-image2 or Gemini.

Render the resulting FigureSpec JSON with a FigureSpec-compatible renderer when available.
