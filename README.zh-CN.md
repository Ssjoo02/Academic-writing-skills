# Academic Writing：图片 API

本 skill 可以为论文中的非数据类 picture（teaser、概念插图、精修 overview 图）
可选接入图像生成 API。数据图表由当前 agent 直接用 Python 生成。

英文版本：[README.md](README.md)

## 配置

```bash
export GEMINI_API_KEY="..."
export GEMINI_IMAGE_MODEL="gemini-2.5-flash-image"   # 可选
export GEMINI_BASE_URL="..."                          # 可选，中继地址
```

或者 GPT-image：

```bash
export OPENAI_API_KEY="..."
export OPENAI_IMAGE_MODEL="gpt-image-2"              # 可选
export OPENAI_BASE_URL="..."                          # 可选，中继地址
```

未配置 API 时，当前 agent 直接绘制。
