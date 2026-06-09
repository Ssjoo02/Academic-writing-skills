# Academic Writing

Academic Writing 是一个 agent-readable 的学术论文写作 skill，可用于 Claude Code、Codex 等本地 skill 环境，也可以被任何能读取 `SKILL.md` 和 Markdown 引用文件的 agent 或研究者手动使用。

English: [README.md](README.md)

## 项目定位

Academic Writing 关注的是研究流程中的论文建构阶段：把实验结果、研究笔记、图表、证据和 claim 组织成一篇连贯的论文初稿。

它默认只做写作，不静默改变研究本身。它可以改结构、论证链、章节逻辑、claim-evidence 对齐、venue fit、引用卫生、图表表达和 reviewer-facing clarity；但不会默认修改研究 idea、运行实验、编造结果、伪造引用，或把证据不足的 claim 写强。

这个 skill 的核心前提是：

```text
问题 -> 缺口 -> 挑战 -> 洞察 -> 方法 / 研究 / benchmark -> 证据 -> 主张
```

论文不是结果堆砌，而是一条可辩护的论证链。每个主要 claim 都必须有明确的证据边界。

## 写作理念与参考来源

这套写作方法不是我们闭门造车，而是提炼自被广泛认可的科研写作经验。最直接的参考是彭思达老师整理的
*learning_research* 中的科研与论文写作经验，同时结合了若干经典的科学写作建议：

- *learning_research* — 彭思达的科研经验：
  <https://github.com/pengsida/learning_research/tree/master>
- *Ten Tips for Writing CS Papers* — Sebastian Nowozin：
  <https://www.nowozin.net/sebastian/blog/ten-tips-for-writing-cs-papers-part-1.html>
- *Writing a Good Introduction* — Henning Schulzrinne（源自 Jim Kurose）：
  <https://www.cs.columbia.edu/~hgs/etc/intro-style.html>

从这些来源中，skill 内化了几条贯穿全文的写作习惯：尽早、明确地陈述 contribution，并将其归类为
*insight*（洞察）/ *performance*（性能）/ *capability*（能力）；把每个 section 都当作这一个
contribution 的不同切面；用简单直接的语言而非华丽辞藻；引言遵循"动机 → 具体问题 → 贡献 →
与已有工作的区别 → 结构导引"的弧线。上面那条主线，正是把这些习惯串起来的脊梁。

## 核心流程

完整论文初稿 workflow 是三阶段、两个强制检查点。

```text
Workspace Discovery
  -> Writing Policy
  -> Checkpoint 1：确认或修改 policy
  -> Paper Framework
  -> Checkpoint 2：确认或修改 framework
  -> 论文初稿
```

这两个检查点是刻意设计的。大模型完全可以一次性把整篇论文生成出来，但这种"一键生成"的初稿往往会塌缩成一种泛泛的、平均化的写作风格，很难贴合这项工作真正应该被讲述的方式。两个 gate 就是为了打破这种惯性：agent 必须在 Writing Policy 和 Paper Framework 处分别停下来，把本会被静默决定的东西——论文身份、证据边界、venue、章节结构、图表计划——摊开给作者确认或修正。用户要求"写完整论文"只会启动 workflow，并不会跳过这两道关。最终得到的是一篇按作者思路展开的论文，而不是一份模板化的自动产物。

### 1. Writing Policy

Writing Policy 是论文契约。它记录 source snapshot、paper identity、core story、claim-evidence map、关键术语、可见资产和 open decisions。

它也负责按固定顺序完成路由：

```text
venue_kind -> venue -> paper_type
```

只有当用户明确说目标是 journal article / journal paper，或明确点名期刊 venue 时，才进入 journal 模式。其他情况默认按 conference 论文处理。

### 2. Paper Framework

Paper Framework 把 policy 转成 section-level 计划。它定义章节列表、每个 section 的角色、paper-type profile 对齐、venue/template 组装方式、正文预算，以及图表的 display-item budget。

这对真实投稿很重要：双栏图和大表会真实占页，所以在生成初稿前就必须把图表占用纳入预算。

### 3. 论文初稿

用户确认 Framework 后，skill 会创建完整 LaTeX 论文项目，包括确认后的结构、模板、引用、章节和图表计划。官方 venue template 只作为格式壳使用：示例文字和说明文字会被移除，再写入论文内容。

初稿交付前，skill 会完成内部 review 和 readiness pass。能在 writing-only 范围内修复的 blocking 问题会先修复；不能修复的证据、引用、排版或 venue-limit 风险会作为 unresolved risks 报告，而不是被隐藏。

## 会议和期刊支持

Academic Writing **同时内置会议和期刊**的模板与 paper-type profile，并不只服务会议论文。会议模板涵盖
ICLR、NeurIPS、ICML、CVPR、ACL/EMNLP/NAACL、AAAI、IJCAI 等；期刊方向包含 IEEE Transactions、JMLR，
以及面向任意未单独建模期刊的通用期刊 profile。期刊模式还会在基础写作规则之上叠加期刊特有的 section
overlay 与投稿要素检查（必需声明、display item 上限、Methods 位置、篇幅预算等）。

| 情况 | 行为 |
| --- | --- |
| 用户明确点名会议 | 可用时加载对应 venue profile。 |
| 用户没有指定 venue | 默认 conference 模式，使用 generic / venue TBD。 |
| 用户明确点名期刊 | 使用 journal 模式和 journal paper-type profiles。 |
| 用户点名未建模期刊 | 使用 generic journal profile，并把期刊特定字段保持为待确认。 |

这种保守路由可以避免用户只是说“写论文”时，被误写成期刊论文。

## 可选图像生成

数据图表由当前 agent 根据项目数据生成。对 teaser、概念图、overview image 等非数据类论文图片，skill 可以可选接入 Gemini 或 GPT-image，也支持普通 API key 和中继/base URL 配置。

未配置图片 API 时，只要任务在能力范围内，当前 agent 仍可直接绘制或组装图。

## 安装

请复制完整 `academic-writing` 目录，不要只复制 `SKILL.md`。这个 skill 依赖 `manifest.yaml`、`static/`、`references/`、`templates/` 和支持脚本。

### Claude Code

用户级安装：

```bash
mkdir -p ~/.claude/skills
cp -R /path/to/academic-writing ~/.claude/skills/
```

项目级安装：

```bash
mkdir -p your-paper-repo/.claude/skills
cp -R /path/to/academic-writing your-paper-repo/.claude/skills/
```

安装或更新后，重启 Claude Code。

### Codex

用户级安装：

```bash
mkdir -p ~/.codex/skills
cp -R /path/to/academic-writing ~/.codex/skills/
```

如果你使用自定义 `$CODEX_HOME`，请把目录放到 `$CODEX_HOME/skills/` 下。

### 其他 agent 或手动使用

保持目录结构不变，先读取 `SKILL.md`。当它指向 `static/`、`references/` 或 `templates/` 时，在同一个 `academic-writing` 目录内解析路径。只加载当前任务真正需要的文件。

## 示例请求

```text
Use academic-writing to build a first manuscript from this workspace for EMNLP.
Use academic-writing to write only the Writing Policy first.
Use academic-writing to build the Paper Framework after I confirm the policy.
Use academic-writing to revise this Introduction for ACL-style clarity.
Use academic-writing to prepare a journal manuscript targeting JMLR.
Use academic-writing to review this manuscript before submission.
```

## 范围边界

Academic Writing 能帮助你得到更清晰、更可辩护的论文初稿，但不保证录用。它不会伪造证据，不会隐藏 unsupported claims，也不会把缺失实验包装成自信结论。证据不足时，论文应该写得更克制，而不是更夸张。
