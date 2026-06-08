# Academic Writing: Picture API

This skill can optionally use an image-generation API for non-data paper
pictures (teasers, conceptual illustrations, polished overview pictures).
Data charts are generated directly by the current agent with Python.

Chinese version: [README.zh-CN.md](README.zh-CN.md)

## Configuration

```bash
export GEMINI_API_KEY="..."
export GEMINI_IMAGE_MODEL="gemini-2.5-flash-image"   # optional
export GEMINI_BASE_URL="..."                          # optional, for relay
```

Or for GPT-image:

```bash
export OPENAI_API_KEY="..."
export OPENAI_IMAGE_MODEL="gpt-image-2"              # optional
export OPENAI_BASE_URL="..."                          # optional, for relay
```

If no API is configured, the current agent draws the picture directly.
