# Academic Writing：图片 API

本 skill 可以为论文中的非数据类 picture 可选接入图像生成 API。柱状图、雷达图、折线图、热力图、表格等数据图表仍默认由当前 agent 直接生成，通常使用 Python。

英文版本：[README.md](README.md)

## API 配置

使用 GPT-image2 风格渲染：

```bash
export ACADEMIC_WRITING_PICTURE_RENDERER="gpt-image2"
export OPENAI_API_KEY="..."
export ACADEMIC_WRITING_OPENAI_IMAGE_MODEL="gpt-image-1.5"
```

使用 Gemini 风格渲染：

```bash
export ACADEMIC_WRITING_PICTURE_RENDERER="gemini"
export GEMINI_API_KEY="..."
export ACADEMIC_WRITING_GEMINI_IMAGE_MODEL="gemini-2.5-flash-image"
```

## 生成内容

每个 picture figure 会先生成一份可直接复制的 prompt：

```text
paper/figures/prompts/<figure-id>.md
```

其中的 `Direct Image Prompt` 会原样用于 API 生成，也可以由用户复制到其他 AI 对话中自行生成图片。

生成的图片会保存为：

```text
paper/figures/<figure-id>.png
```

## 未配置 API

如果没有配置 picture API，当前执行任务的 agent 会根据同一份 `Direct Image Prompt` 生成图片并插入论文。默认不在论文中留下空白 picture。
