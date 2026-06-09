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

This route now covers **both** conceptual teasers **and** pipeline / architecture
/ workflow concept figures, because the goal is a polished *illustrative* figure
(devices, UI panels, icons, actors, a scene), not a flowchart of rounded
rectangles. Use AI generation for the **visual**; do not use it for the **text**
(see the next section). Reserve a deterministic node-edge diagram (FigureSpec /
TikZ) only when the user explicitly asks for an editable schematic, or when the
figure is genuinely a formal graph/state machine where a clean schematic reads
better than an illustration.

## Text Is Never Rendered By The Image Model (critical)

Raster image models **cannot spell**. They reliably corrupt exact labels — real
generations from this skill produced `Indulator` (Emulator), `Doicker`
(Docker), `Missformation` (Misinformation), and `pipeine` (pipeline). Garbled
text in a paper figure is fatal. Therefore:

- **The image model renders only the illustration, with no text.** State this in
  the prompt explicitly: *"Do not render any text, letters, words, numbers, or
  labels anywhere in the image."* Any text the model adds is treated as noise to
  be cropped or covered, never trusted.
- **All exact labels are added deterministically after generation**, as a LaTeX /
  TikZ overlay on top of `\includegraphics`, so every word is spelled from the
  Writing Policy and stays editable. This is the **hybrid pattern** and it is the
  default for every picture figure.
- **Never paste the prompt scaffolding into the image.** The lines `Message:`,
  `Show exactly these components:`, and `Use exactly these labels:` are
  instructions to *you*, not text to be drawn. A clean Direct Image Prompt is a
  single visual description with no rubric headers (a past run drew the literal
  `Message:` sentence into the figure).

### Hybrid Overlay Pattern (LaTeX/TikZ)

Generate the text-free illustration, then place labels over it with TikZ in a
normalized 0–1 coordinate space, tuning anchor positions by **looking at the
rendered PNG** and adjusting:

```tex
\begin{figure*}[t]
\centering
\begin{tikzpicture}
  % background illustration drawn by the image model (text-free)
  \node[anchor=south west,inner sep=0] (img) at (0,0)
    {\includegraphics[width=\textwidth]{figures/fig1_teaser.png}};
  % overlay exact labels in normalized (x,y) ∈ [0,1] over the image
  \begin{scope}[x={(img.south east)},y={(img.north west)}]
    \node[font=\sffamily\small\bfseries] at (0.10,0.52) {User};
    \node[font=\sffamily\small\bfseries] at (0.46,0.55) {GUI Agent};
    \node[font=\sffamily\footnotesize]   at (0.86,0.74) {HARM};
    % ... place each label, then recompile and re-inspect alignment
  \end{scope}
\end{tikzpicture}
\caption{...}
\label{fig:teaser}
\end{figure*}
```

Requires `\usepackage{tikz}` in the preamble. Iterate: compile → look at the PDF
→ nudge coordinates until every label sits on its element. If precise overlay is
impractical for a dense figure, fall back to a clean deterministic figure (TikZ
schematic or a compact labeled illustration) rather than shipping garbled
in-image text.

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
- Title:
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
<A single clean paragraph describing the illustration only. No rubric headers, no
label lists, no spelled-out words to draw. End with the no-text instruction.>

## Text Overlay Plan
- Labels to overlay (exact spelling from Writing Policy): ...
- Approximate normalized positions (x,y in 0–1): ...

## Renderer Route
- Preferred renderer:
- Renderer status:
- Output path:
- API prompt source: use the exact `Direct Image Prompt` block above
- Review notes:
```

## Writing the Direct Image Prompt

The Direct Image Prompt is **one clean visual paragraph**, not a filled-in rubric.
Describe the scene the way you would commission an illustrator, then end with the
no-text instruction. Quality guardrails:

- **Illustrative, not a flowchart.** Aim for a scene with concrete objects —
  smartphone / device frames, app UI panels, channel icons (envelope, chat
  bubble, browser, file), an attacker motif, harm/safe outcome icons — connected
  by clean arrows. **Do not ask for "rounded rectangles", "boxes in a row", or a
  "flat box-and-arrow flowchart"**; that is exactly the look the user rejected.
- **Academic aesthetic**: flat vector illustration, clean lines, minimalist,
  generous but balanced whitespace (no large empty bands; fill the canvas evenly).
- **Restrained color**: soft professional tones, a small consistent palette; no
  oversaturated colors.
- **No text in the image**: finish every prompt with *"Do not render any text,
  letters, words, numbers, or labels anywhere — leave clean space where labels
  will be added later."* Labels come from the Text Overlay Plan, not the model.
- **Avoid**: photorealism, messy sketch lines, heavy drop shadows, rainbow
  gradients, 3D bevels, glow effects, and any embedded words.

The rest — palette, exact layout, icon choice — is decided per figure from the
Evidence Boundary and Visual Plan. Do not copy a fixed style string into every
prompt.

### Example Direct Image Prompt (pipeline, illustrative, text-free)

> A clean flat vector academic illustration of a left-to-right process for
> building a mobile-app safety benchmark. Six evenly spaced circular icon
> medallions in a single horizontal row, equal spacing, connected by thin clean
> right-pointing arrows: a checklist clipboard, a smartphone showing an app
> screen, a hand typing a chat message, a magnifier over a warning shield, a
> stack of Android emulator phone frames, and a padlocked archive box. Below the
> row, a slim horizontal band suggesting a worked example with small app icons
> (envelope, calendar) and an arrow flow. Soft professional palette of blue,
> teal, amber, and slate on a white background, minimalist, balanced, filling the
> full width evenly. Do not render any text, letters, words, numbers, or labels
> anywhere — leave clean space where labels will be added later.

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
asks for a different image language or renderer-specific syntax.

### Gemini API

Detected when `GEMINI_API_KEY` is set.

```bash
# Construct the endpoint from env vars
GEMINI_BASE_URL="${GEMINI_BASE_URL:-https://generativelanguage.googleapis.com}"
MODEL="${GEMINI_IMAGE_MODEL:-gemini-2.5-flash-image}"
URL="${GEMINI_BASE_URL}/v1beta/models/${MODEL}:generateContent"

# Call the API
curl -s -X POST "$URL" \
  -H "Content-Type: application/json" \
  -H "x-goog-api-key: $GEMINI_API_KEY" \
  -d '{
    "contents": [{"parts": [{"text": "<Direct Image Prompt here>"}], "role": "user"}],
    "generationConfig": {"responseModalities": ["IMAGE", "TEXT"]}
  }'

# Extract base64 image from response: candidates[0].content.parts[*].inlineData.data
# Save as paper/figures/<figure-id>.png
```

### OpenAI / GPT-Image API

Detected when `OPENAI_API_KEY` is set (and `GEMINI_API_KEY` is not).

```bash
OPENAI_BASE_URL="${OPENAI_BASE_URL:-https://api.openai.com}"
MODEL="${OPENAI_IMAGE_MODEL:-gpt-image-2}"
URL="${OPENAI_BASE_URL}/v1/images/generations"

curl -s -X POST "$URL" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -d '{
    "model": "'"$MODEL"'",
    "prompt": "<Direct Image Prompt here>",
    "n": 1,
    "size": "1024x1024"
  }'
# Response: data[0].b64_json or data[0].url
```

### Current Agent Fallback

If neither `GEMINI_API_KEY` nor `OPENAI_API_KEY` is set, the current executing
agent draws the picture from the Direct Image Prompt. A lower-fidelity but
accurate paper-safe picture is better than an empty figure slot.

## Review Gate

Open the rendered PNG and inspect it (do not infer from the prompt). Reject and
regenerate or redraw if **any** of these fail:

- **No raw text rendered by the model.** If the illustration contains any words,
  the model has spelled them — assume they are garbled. Either crop/cover them
  and overlay correct labels, or regenerate with a stronger no-text instruction.
- **No misspellings / no leaked scaffolding.** Specifically check for corrupted
  words (e.g. `Indulator`, `Missformation`) and for prompt headers like
  `Message:` drawn into the image. Either means reject.
- **Illustrative, not a box-and-arrow flowchart.** If it is just rounded
  rectangles in a row, the prompt was wrong — rewrite it toward a scene.
- **No large empty bands**; the composition fills the canvas evenly.
- All required components appear; no extra claim, dataset, metric, or module was
  invented; arrows and relationships are directionally correct.
- After the TikZ text overlay, **every label sits on its element** and is legible
  at paper scale.
- The generated file is non-empty and stored at the recorded output path.

If any check fails, revise the prompt or the overlay coordinates and regenerate.
Keep rejected versions only when useful for audit.
