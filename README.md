# Academic-Writing-Skills

**Academic-Writing-Skills** 是一个专注于学术论文写作的 skill 集合，用于生成符合具体会议或期刊格式要求的完整论文初稿，可在 Claude Code、Codex 等本地 skill 环境中使用。

English: [README_EN.md](README_EN.md)

## 仓库结构（多 skill 集合）

本仓库由一个**主 skill（hub）** 加三个可独立调用的**子 skill** 组成，跨 skill 复用的内容放在仓库根的 `_shared/`。仓库根的 `SKILL.md` 是**入口路由器**：被安装环境发现后第一个加载，再据请求分派到对应子 skill：

```text
Academic-Writing-Skills/           ← 仓库根 = 集合根
├── SKILL.md                       ← 入口路由器（被发现后第一个读取，分派到下面某个子 skill）
├── _shared/                       ← 跨 skill 复用：核心 stance/gates/contract、venue 模板、
│   ├── core/  templates/  paper-types/  venues/  checks/
└── skills/
    ├── academic-writing/          ← HUB：写作流水线编排 + 写作本体（Policy→Framework→正文）
    ├── academic-figure/           ← 图/表子系统（可单独调用：只画图/排表）
    ├── academic-citation/         ← 引文检索与 bib 完整性审计（可单独调用：只查引文）
    └── academic-review/           ← 投稿前 review + 静态审计 + readiness（可单独调用：只审稿）
```

安装时整仓被同步到 `.../skills/academic-writing/`，环境据**仓库根 `SKILL.md`** 发现并启动本集合。
hub 在需要图表/引文/review 时**委托**对应子 skill，规则零重复。三个子 skill 各自带独立的 `SKILL.md`，
因此「只画一张图」「只查引文」「只审一遍稿」也可由入口路由器直接分派到对应子 skill，而不必走完整写作流程。

## 适用场景

Academic Writing 面向研究流程中的**论文建构阶段**：将实验结果、研究笔记、图表、证据和 claim 组织成一篇结构完整、论证连贯的论文初稿。

它默认只处理写作相关任务，不会改变研究本身。也就是说，它可以帮助你改进论文结构、论证链、章节逻辑、claim-evidence 对齐、venue fit、引用卫生、图表表达和 reviewer-facing clarity；但不会默认修改研究 idea、运行实验、编造结果、伪造引用，或将证据不足的 claim 写得过强。

该 skill 适合以下场景：

- **已有部分实验结果，想写论文初稿**：实验已经完成或部分完成，手中已有结果与研究笔记，希望将其组织成一篇结构完整、逻辑连贯的论文初稿。
- **已有初稿，希望润色或重写**：针对 Introduction、Method、Experiments 等章节进行起草、重构，或按照特定 venue 风格进行润色。
- **指定 venue 的成稿需求**：明确目标会议或期刊，例如 EMNLP、NeurIPS、JMLR，需要根据对应模板、篇幅预算和投稿要求组织论文。
- **分步推进写作流程**：只想先生成 Writing Policy 或 Paper Framework，在确认论文身份、证据边界和章节结构后，再继续生成正文。
- **投稿前自检**：在提交前对已有手稿进行 review 和 readiness pass，暴露证据、引用、排版和 venue-limit 等潜在风险。
- **会议与期刊模式切换**：在 conference 与 journal 两种模式之间组织论文，包括期刊特有的 section overlay 与投稿要素检查。

这个 skill 的核心前提是：

```text
问题 -> 缺口 -> 挑战 -> 洞察 -> 方法 / 研究 / benchmark -> 证据 -> 主张
```

论文不是结果的堆砌，而是一条可辩护的论证链。每个主要 claim 都必须有清晰的证据边界。

## 写作理念与参考来源

该 skill 的写作方式提炼自被广泛认可的科研写作经验，具体包括：

- *learning_research* — 彭思达的科研经验：  
  <https://github.com/pengsida/learning_research/tree/master>
- *Ten Tips for Writing CS Papers* — Sebastian Nowozin：  
  <https://www.nowozin.net/sebastian/blog/ten-tips-for-writing-cs-papers-part-1.html>
- *Writing a Good Introduction* — Henning Schulzrinne，源自 Jim Kurose：  
  <https://www.cs.columbia.edu/~hgs/etc/intro-style.html>

我们的目标是让 AI 学习这些真实可用的论文写作经验，使生成的论文更贴近真实研究者的写作习惯与表达风格。

## 核心流程

完整论文初稿 workflow 分为三个阶段，并包含两个强制检查点：

```text
Workspace Discovery
  -> Writing Policy
  -> Checkpoint 1：确认或修改 policy
  -> Paper Framework
  -> Checkpoint 2：确认或修改 framework
  -> 论文初稿
```

为了避免“一键生成”的初稿不符合真实论文写作习惯，Academic Writing 在生成完整初稿之前设置了两个检查点：agent 必须分别在 Writing Policy 和 Paper Framework 阶段停下来，将原本可能被静默决定的内容展示给作者确认或修改，包括论文身份、证据边界、目标 venue、section 结构和图表计划等。

因此，用户提出“写完整论文”的请求只会启动 workflow，而不会跳过这两个检查点。最终生成的应当是一篇围绕作者思路展开的论文初稿，而不是模板化的自动产物。

### 1. Writing Policy

Writing Policy 是论文写作契约，用于记录 source snapshot、paper identity、core story、claim-evidence map、关键术语、可见资产和 open decisions。

建议在使用 skill 之初先指定目标会议或期刊。若未指定，则默认采用 conference 模式下的通用模板。

### 2. Paper Framework

skill 内置了多种 paper-type profile，用于匹配不同类型论文的常见结构和写作思路，主要包括 section 分布、章节目标和内容组织方式，从而避免 AI 写作思路过于发散。

Paper Framework 会将 Writing Policy 转化为 section-level 计划，明确章节列表、每个 section 的核心内容、venue/template 组装方式、正文预算，以及图表和表格的 display-item budget。用户可以先基于 Paper Framework 进行调整与确认，再进入正文生成阶段。

### 3. 论文初稿

用户确认 Paper Framework 后，skill 会创建完整的 LaTeX 论文项目，包括确认后的论文结构、模板、引用、章节和图表计划。

官方 venue template 仅作为格式壳使用：示例文字和说明内容会被移除，然后写入论文正文。

初稿交付前，skill 会完成内部 review 和 readiness pass。

## 会议和期刊支持

Academic Writing 同时内置会议和期刊的模板与 paper-type profile，并不只服务于会议论文。

会议模板覆盖 ICLR、NeurIPS、ICML、CVPR、ACL、EMNLP、NAACL、AAAI、IJCAI 等；期刊方向支持 IEEE Transactions、JMLR，以及面向未单独建模期刊的通用 journal profile。

| 情况 | 行为 |
| --- | --- |
| 用户明确点名会议 | 若对应 venue profile 可用，则加载该 profile。 |
| 用户未指定 venue | 默认使用 conference 模式，并标记为 generic / venue TBD。 |
| 用户明确点名期刊 | 使用 journal 模式和 journal paper-type profiles。 |
| 用户点名未建模期刊 | 使用 generic journal profile，并将期刊特定字段保留为待确认。 |

这种保守路由可以避免用户只是说“写论文”时，系统误将其组织成期刊论文。

## 安装

请同步**整个仓库**（包含 `skills/` 与根目录的 `_shared/`），不要只复制单个 `SKILL.md` 或单个子 skill 目录，因为各子 skill 通过相对路径依赖 `_shared/`（核心 stance/gates/contract、venue 模板、paper-type/venue 卡片、共享 check 规则）。同步整个仓库后，四个 skill（`academic-writing`、`academic-figure`、`academic-citation`、`academic-review`）会一起可用。

不要把本地维护材料打包进安装副本：`_local/` 和 `SKILL-FLOW.md` 只给仓库维护者自查使用。`.gitignore` 会防止它们进入 Git，但不会影响 `cp -R`，所以安装/同步请使用下面的 `rsync --exclude` 命令。

**Clone the repo**（Windows 与 Mac/Linux 相同）

```bash
git clone https://github.com/Ssjoo02/Academic-writing-skills
cd Academic-writing-skills
```

---

### 1. Codex

**Mac/Linux：**
```bash
CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"
mkdir -p "$CODEX_HOME/skills/academic-writing"
rsync -a --delete --delete-excluded \
  --exclude '.git/' \
  --exclude '_local/' \
  --exclude 'SKILL-FLOW.md' \
  ./ "$CODEX_HOME/skills/academic-writing/"
```

**Windows（PowerShell）：**
```powershell
mkdir -p "$env:USERPROFILE\.codex\skills"
Copy-Item -Path "." -Destination "$env:USERPROFILE\.codex\skills\academic-writing" -Recurse -Force
Remove-Item -Path "$env:USERPROFILE\.codex\skills\academic-writing\_local" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item -Path "$env:USERPROFILE\.codex\skills\academic-writing\SKILL-FLOW.md" -Force -ErrorAction SilentlyContinue
```

使用示例：
```text
Use academic-writing to revise my paper's Introduction.
```

---

### 2. CC / Claude Code

支持全局安装或项目级安装。

**Mac/Linux：**

全局安装：
```bash
mkdir -p "$HOME/.claude/skills/academic-writing"
rsync -a --delete --delete-excluded \
  --exclude '.git/' \
  --exclude '_local/' \
  --exclude 'SKILL-FLOW.md' \
  ./ "$HOME/.claude/skills/academic-writing/"
```

项目级安装：
```bash
mkdir -p .claude/skills/academic-writing
rsync -a --delete --delete-excluded \
  --exclude '.git/' \
  --exclude '_local/' \
  --exclude 'SKILL-FLOW.md' \
  ./ .claude/skills/academic-writing/
```

---

**Windows（PowerShell）：**

全局安装：
```powershell
mkdir -p "$env:USERPROFILE\.claude\skills"
Copy-Item -Path "." -Destination "$env:USERPROFILE\.claude\skills\academic-writing" -Recurse -Force
Remove-Item -Path "$env:USERPROFILE\.claude\skills\academic-writing\_local" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item -Path "$env:USERPROFILE\.claude\skills\academic-writing\SKILL-FLOW.md" -Force -ErrorAction SilentlyContinue
```

项目级安装：
```powershell
mkdir -p .claude/skills
Copy-Item -Path "." -Destination ".claude/skills/academic-writing" -Recurse -Force
Remove-Item -Path ".claude\skills\academic-writing\_local" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item -Path ".claude\skills\academic-writing\SKILL-FLOW.md" -Force -ErrorAction SilentlyContinue
```

---

安装后重启 Claude Code，并在 prompt 中明确点名该 skill，例如：
```text
Please use the academic-writing skill to revise my Introduction.
```

## 绘图

数据图表，如柱状图、折线图、雷达图、热力图、散点图和表格，会由当前 agent 直接根据项目数据生成，不需要额外配置。

对于 teaser、概念图、overview image 等非数据类论文图片，skill 可选接入 Gemini 或 GPT-image 生图模型。

未配置图片 API 时，默认由当前 agent 直接绘制；若配置了生图 API，则使用对应模型进行渲染。

### 生图模型 API 配置

skill 会通过环境变量自动检测可用的生图 API：

- 设置 `GEMINI_API_KEY` 时，使用 Gemini；
- 设置 `OPENAI_API_KEY` 时，使用 GPT-image；
- 两者都设置时，优先使用 Gemini。

普通官方 key 即可使用，也支持中继或自建网关的 base URL。

**Gemini**

```bash
export GEMINI_API_KEY="你的_key"

# 可选：使用中继或自建网关时覆盖 base URL
# 默认：https://generativelanguage.googleapis.com
export GEMINI_BASE_URL="https://your-relay.example.com"

# 可选：覆盖模型
# 默认：gemini-2.5-flash-image
export GEMINI_IMAGE_MODEL="gemini-2.5-flash-image"
```

**OpenAI / GPT-image**

```bash
export OPENAI_API_KEY="你的_key"

# 可选：使用中继或自建网关时覆盖 base URL
# 默认：https://api.openai.com
export OPENAI_BASE_URL="https://your-relay.example.com"

# 可选：覆盖模型
# 默认：gpt-image-2
export OPENAI_IMAGE_MODEL="gpt-image-2"
```

请将这些变量配置到运行 agent 的环境中，例如写入 shell 的 `~/.bashrc` / `~/.zshrc`，或在启动 agent 前执行 `export`。skill 在生成图片时会自动读取这些变量，无需设置任何自定义前缀变量。

## 编译为 PDF

skill 产出的是一个**可编译的完整 LaTeX 项目**，默认位于 `paper/` 目录下，通常包含：

```text
paper/
  main.tex
  sections/*.tex
  references.bib
  math_commands.tex
  venue template files
```

它不是一段零散的 `.tex` 文本，而是一个完整论文项目。为了将其编译为 PDF，并让版面检查真正生效，建议在运行环境中安装以下工具：

- `latexmk` 或 `pdflatex`：来自 TeX Live / MacTeX，用于编译 LaTeX；
- `pdfinfo` / `pdftotext`：来自 poppler-utils，用于读取编译后的 PDF，并进行页数预算等检查。

agent 会通过 `skills/academic-review/scripts/check_compile_env.py` **自动检测当前环境是否具备编译工具链**。只要存在 `latexmk` 或 `pdflatex`，agent 在写作流程中会**自动编译论文，并以编译出的 PDF 为准**进行版面检查。检查内容包括但不限于：

- 图表是否出界；
- 是否存在 `Overfull \hbox`；
- 表格是否溢出；
- 附录排版是否异常；
- 页数是否超过目标 venue 的预算。

如果检测不到编译工具链，agent 仍会生成完整的 LaTeX 源码并进行静态审计，但会**显式提醒你**：PDF 未能编译、缺少哪些工具、页数/版面等以编译 PDF 为准的检查仅做了静态版本（不会静默跳过）。

本地编译方式如下：

```bash
cd paper
latexmk -pdf main.tex
```

建议先装好 LaTeX 与 poppler 工具链，再让 agent 生成完整初稿。这样，版面相关的 gate 才能真正生效。

## 示例请求

推荐在一开始就指定实验目录和目标会议，例如：

```text
Use academic-writing to build a first manuscript from this workspace for EMNLP, my workspace is xxx/xxx.
Use academic-writing to revise this Introduction for ACL-style clarity, this is my paper xxx/xxx.
```

## 维护声明

本项目会持续更新。欢迎大家试用，也非常感谢任何形式的反馈、建议或修改意见。
