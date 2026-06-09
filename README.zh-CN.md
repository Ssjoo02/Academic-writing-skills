# Academic Writing

Academic Writing 是一个用于学术论文写作的 Codex skill。它把已有研究材料转化为有约束的论文草稿，默认只做写作工作：改结构、论证链、claim-evidence 对齐、venue fit、引用卫生、图表表达和投稿前 review，不默认修改研究 idea，不跑实验，不编造结果，也不伪造引用。

English version: [README.md](README.md)

## 这个 Skill 用来做什么

适合在这些场景使用：

- 从项目 workspace 创建完整论文初稿；
- 在写正文前生成 Writing Policy；
- 把 Writing Policy 转成 section-level Paper Framework；
- 基于确认后的 Framework 生成 LaTeX `paper/` 项目；
- 修改、润色、压缩或 review 已有论文草稿；
- 在不越过证据边界的前提下适配会议或期刊 venue。

这个 skill 把论文看成一个结构化论证：

```text
问题 -> 缺口 -> 挑战 -> 洞察 -> 方法 / 研究 / benchmark -> 证据 -> 主张
```

每个主要 claim 都必须能追到可见证据；否则就要弱化、延后、标记未解决，不能写强。

## 核心流程

完整初稿 workflow 是三阶段、两个强制检查点。

```text
Workspace Discovery
  -> Writing Policy
  -> Checkpoint 1：用户确认或修改 policy
  -> Paper Framework
  -> Checkpoint 2：用户确认或修改 framework
  -> Full Draft LaTeX Project
  -> 自动 Post-Draft Review
  -> Final Audits / Submission Readiness Summary
```

这两个检查点是硬门控。用户要求“写完整初稿”只表示允许进入这个 workflow，不表示可以跳过 Writing Policy 或 Paper Framework。

### 阶段 1：Writing Policy

Writing Policy 是论文的紧凑写作契约，保存到：

```text
writing-policies/<paper-slug>-writing-policy.md
```

它记录：

- source snapshot 和已检查文件；
- paper identity：venue kind、venue、paper type、目标读者、核心研究问题；
- core story 和一句话 contribution；
- claims 与 evidence boundary；
- 关键术语和命名决策；
- 可见资产与约束；
- 会影响论文方向的 open decisions。

路由顺序必须是先判断 `venue_kind`，再判断 `venue`，最后判断 `paper_type`。

```text
venue_kind -> venue -> paper_type
```

只有当用户明确说这是 journal article / journal paper，或明确点名期刊 venue 时，才进入 journal 模式。只要用户没有明确指定 journal，默认就是 conference。

### 阶段 2：Paper Framework

Paper Framework 是 section-level 规划，不是正文，也不是逐段大纲。保存到：

```text
writing-policies/<paper-slug>-paper-framework.md
```

它定义：

- 标题方向和章节列表；
- 每个 section 的 main content；
- 是否遵守 paper-type profile，以及任何必要偏离；
- 正文 page budget；
- 图表的 display-item page budget；
- template 和 venue assembly plan；
- 进入 draft 前仍未解决的 blocker。

对严格 page limit 的会议，图和表必须单独计入预算。双栏图、大表会真实占页；不能只按 prose 估算页数。

### 阶段 3：Full Draft

用户确认 Paper Framework 后，skill 创建完整 LaTeX 项目：

```text
paper/
  main.tex
  math_commands.tex
  references.bib
  sections/
  figures/
```

初稿使用确认过的 template 和 section plan。官方 venue template 只作为格式壳使用：示例正文和说明文字必须删除后再写入论文内容。

## 自动 Review 和 Audits

最终交给用户的第一版 draft 不是未经 review 的 raw draft。只要完整 `paper/` 初稿存在，skill 就自动加载 `references/sections/paper-review.md` 并运行 post-draft review gate。

review 分两轮：

1. 自审：检查 contribution、clarity、evidence、evaluation completeness、method soundness、visual/layout 和 format hygiene。
2. 独立 reviewer：有 subagent 能力时启动独立 reviewer；没有时使用 fresh second self-pass fallback。

所有 blocking 问题和所有能在 writing-only 范围内修复的 high-priority 问题，都必须在最终交付前修完。

最终 audits 是硬门控：

```bash
python3 scripts/audit_citations.py paper
python3 scripts/audit_draft.py paper
python3 scripts/audit_draft.py paper --max-content-pages <limit>
```

page-limit audit 以编译后的 PDF 为准。EMNLP/ACL-style long paper 使用 8 个 content pages；short paper 使用 4 个。只要超过确认的 venue page limit，这个 draft 就不完整，即使 Paper Framework 里的计划页数看起来没有超。

## 会议和期刊路由

skill 同时支持 conference 和 journal，但默认保守：

- 用户明确点名期刊或说 journal paper，才使用 `venue_kind=journal`。
- 其他情况使用 `venue_kind=conference`。
- conference paper type 使用 `references/paper-types/*.md`。
- journal paper type 使用 `references/paper-types/journal/*.md`。
- journal-only section overlays 和 submission-element checks 只在 journal 模式加载。

这样可以避免一个 generic 或未指定 venue 的请求被误写成期刊论文。

## 可选图片 API

对 teaser、概念图、overview image 等非数据类论文图片，skill 可以可选接入图像生成 API。数据图表仍由当前 agent 直接用 Python 生成。

Gemini：

```bash
export GEMINI_API_KEY="..."
export GEMINI_IMAGE_MODEL="gemini-2.5-flash-image"   # 可选
export GEMINI_BASE_URL="..."                          # 可选，中继地址
```

GPT-image：

```bash
export OPENAI_API_KEY="..."
export OPENAI_IMAGE_MODEL="gpt-image-2"              # 可选
export OPENAI_BASE_URL="..."                          # 可选，中继地址
```

未配置图片 API 时，当前 agent 会直接绘制或组装图片。

## 安装

请复制完整 `academic-writing` 目录，而不是只复制 `SKILL.md`。这个 skill 依赖 `manifest.yaml`、`static/`、`references/`、`templates/`、`scripts/` 和 `tests/`。

Codex 安装示例：

```bash
mkdir -p ~/.codex/skills
cp -R /path/to/academic-writing ~/.codex/skills/
```

安装或更新后，建议开启新会话。

## 示例请求

```text
Use academic-writing to create a full draft from this workspace for EMNLP.
Use academic-writing to write the Writing Policy first; do not draft yet.
Use academic-writing to build the Paper Framework from the confirmed policy.
Use academic-writing to revise this introduction for ACL-style clarity.
Use academic-writing to review this full paper before submission.
Use academic-writing for a journal paper targeting JMLR.
```

## 范围边界

这个 skill 不会：

- 默认运行新实验或修改实验 pipeline；
- 编造数字、引用、baseline、dataset 或 claim；
- 静默改变研究 idea、方法机制或证据边界；
- 在 compilation、citation、page-limit 或 review gate 失败时宣称 draft submission-ready。

当写作需要缺失证据时，skill 会弱化 claim、标记 gap、询问用户，或把问题报告为 unresolved。
