# Picture Generation

Use this reference when the confirmed Figure Plan contains a non-data picture:
teaser, overview illustration, conceptual method picture, qualitative visual
summary, paper-ready raster illustration, or a generated architecture-style
picture that is not better handled by deterministic FigureSpec.

## Boundary

Picture generation supports visual communication. It must not create new
scientific content. Do not let the renderer invent paper claims, modules,
datasets, results, or labels. Every visible element must come from the
confirmed Writing Policy, confirmed Paper Framework, or concrete workspace
source files.

For formal architecture, workflow, topology, audit cascade, or node-edge
diagrams, prefer FigureSpec when deterministic editable SVG matters. Use AI
picture generation when the figure needs a polished raster illustration,
teaser, qualitative method scene, or concept visual that a deterministic diagram
would not express well.

## Required Dual Output

Always create both planning artifacts before considering the picture complete:

```text
paper/figures/prompts/<figure-id>.md
paper/figures/<figure-id>.png
```

Do not leave a planned picture blank. If the user does not provide an external
picture API, the current executing agent must draw the picture from the Picture
Brief and insert it into the paper. A lower-fidelity but accurate paper-safe
picture is better than an empty figure slot.

## Picture Brief

The Picture Brief is the agent's picture design plan generated from the paper.
It must be directly usable in two ways:

1. the user can copy it into another AI chat to generate the picture,
2. the current workflow can pass the same prompt to GPT-image2, Gemini, or
   another configured image API.

The Direct Image Prompt is the prompt passed to image APIs and the prompt copied
into another AI chat. Do not rewrite or summarize it before API submission.

Use this file shape:

```markdown
# Picture Brief: <figure-id>

## Figure Identity
- Figure ID:
- Section:
- Figure type:
- One-sentence message:
- Supported claim:

## Evidence Boundary
- Source files:
- Confirmed concepts:
- Labels allowed in the image:
- Labels or claims forbidden in the image:

## Visual Plan
- Canvas:
- Layout:
- Main visual elements:
- Data flow or relationships:
- Style:
- Accessibility:

## Direct Image Prompt
Create a publication-quality academic figure for a research paper.

Message: ...
Show exactly these components: ...
Use exactly these labels: ...
Relationships/arrows: ...
Style constraints: clean white background, restrained academic palette,
readable English labels, no decorative clip art, no unsupported numbers.
Avoid: ...

## Renderer Route
- Preferred renderer:
- Renderer status:
- Output path:
- API prompt source: use the exact `Direct Image Prompt` block above
- Review notes:
```

## Image Renderer Preference

Resolve the picture renderer at the beginning of the workflow or as soon as the
user provides the preference:

1. If the user explicitly configures `GPT-image2`, use that picture API after
   the Picture Brief is written.
2. If the user explicitly configures `Gemini`, use the Gemini-compatible image
   API after the Picture Brief is written.
3. If the user configures another image renderer, use that renderer only for
   picture figures.
4. If the user does not provide a picture API, the current executing agent draws
   the picture from the brief.

This preference applies only to non-data pictures. Bar charts, line charts,
radar charts, heatmaps, scatter plots, and tables are generated directly by the
current agent from data.

## Renderer Route

After writing the Picture Brief, generate the picture. For every renderer, use
the exact `Direct Image Prompt` block as the image prompt. Do not rewrite,
shorten, translate, or embellish it for the API call unless the user explicitly
asks for a different image language or renderer-specific syntax. Supported
renderer classes:

| Renderer | Use when | Notes |
|---|---|---|
| GPT-image2 or equivalent user-configured API | The user explicitly provides this picture renderer | Save the accepted result as `paper/figures/<figure-id>.png`. |
| Gemini-compatible API | `GEMINI_API_KEY` or an equivalent configured Gemini client is explicitly provided | Use the current official image-generation API and runtime model configuration. |
| current executing agent | No user picture API is provided | Draw a paper-safe picture from the Picture Brief and save it as `paper/figures/<figure-id>.png`. |

For Gemini, use official current documentation at execution time. As of the
2026-06-08 workflow update, Google's Gemini API image-generation examples use
`generateContent` with image response modalities, but model names and regional
availability may drift.

## Review Gate

Before accepting a generated picture, inspect it against the brief:

- all required components appear,
- no extra claim, dataset, metric, or module was invented,
- visible text is readable and matches the allowed labels,
- arrows and relationships are directionally correct,
- the figure is paper-ready rather than slide-deck decorative,
- the generated file is non-empty and stored at the recorded output path.

If any check fails, revise the prompt in the Picture Brief and regenerate or
redraw. Keep rejected versions only when useful for audit.
