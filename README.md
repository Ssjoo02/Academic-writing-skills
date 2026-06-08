# Academic Writing: Picture API

This skill can optionally use an image-generation API for non-data paper
pictures. Data charts such as bar charts, radar charts, line charts, heatmaps,
and tables are still generated directly by the current agent, normally with
Python.

Chinese version: [README.zh-CN.md](README.zh-CN.md)

## API Configuration

For GPT-image2-style rendering:

```bash
export ACADEMIC_WRITING_PICTURE_RENDERER="gpt-image2"
export OPENAI_API_KEY="..."
export ACADEMIC_WRITING_OPENAI_IMAGE_MODEL="gpt-image-1.5"
```

For Gemini-style rendering:

```bash
export ACADEMIC_WRITING_PICTURE_RENDERER="gemini"
export GEMINI_API_KEY="..."
export ACADEMIC_WRITING_GEMINI_IMAGE_MODEL="gemini-2.5-flash-image"
```

## Output

For each picture figure, the workflow first writes a copyable prompt:

```text
paper/figures/prompts/<figure-id>.md
```

The `Direct Image Prompt` block in that file is used unchanged for API
generation, and can also be copied into another AI chat by the user.

The generated picture is saved as:

```text
paper/figures/<figure-id>.png
```

## No API

If no picture API is configured, the current executing agent generates the
picture from the same `Direct Image Prompt` and inserts it into the paper. The
paper should not leave picture figures blank by default.
