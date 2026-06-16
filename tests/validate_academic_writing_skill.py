#!/usr/bin/env python3
"""Validate the academic-writing collection contract.

After the split into a hub skill (academic-writing) plus sibling skills
(academic-figure, academic-citation, academic-review) and a shared layer (_shared/),
this validator checks two things:

1. Structural wiring: every skill's manifest path references resolve (including
   ../../_shared/* cross-skill references), and the shared layer has its essentials.
2. The most important semantic contracts, pointed at their new file locations.

It intentionally avoids checking external venue facts.

Run from the collection root:  python3 tests/validate_academic_writing_skill.py
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError as exc:  # pragma: no cover - environment guard
    raise SystemExit(f"PyYAML is required for validation: {exc}") from exc


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def read(path: Path) -> str:
    require(path.exists(), f"expected file missing: {path}")
    return path.read_text(encoding="utf-8")


def load_yaml(path: Path) -> dict:
    return yaml.safe_load(read(path)) or {}


SKILL_ALLOWED_FRONTMATTER = {"name", "description", "license", "allowed-tools", "metadata"}
MAX_SKILL_NAME_LENGTH = 64


def load_skill_frontmatter(skill_md: Path) -> dict:
    content = read(skill_md)
    require(content.startswith("---\n"), f"{skill_md}: no YAML frontmatter found")
    try:
        _, frontmatter_text, _ = content.split("---", 2)
    except ValueError as exc:
        raise AssertionError(f"{skill_md}: invalid frontmatter format") from exc
    frontmatter = yaml.safe_load(frontmatter_text) or {}
    require(isinstance(frontmatter, dict), f"{skill_md}: frontmatter must be a YAML dictionary")
    return frontmatter


def validate_standard_skill_frontmatter(skill_md: Path, expected_name: str | None = None) -> None:
    """Mirror the standard skill quick validator for SKILL.md frontmatter."""
    frontmatter = load_skill_frontmatter(skill_md)
    unexpected = set(frontmatter) - SKILL_ALLOWED_FRONTMATTER
    require(
        not unexpected,
        f"{skill_md}: unexpected SKILL.md frontmatter keys: {', '.join(sorted(unexpected))}",
    )
    require("name" in frontmatter, f"{skill_md}: missing name")
    require("description" in frontmatter, f"{skill_md}: missing description")

    name = str(frontmatter["name"]).strip()
    description = str(frontmatter["description"]).strip()
    require(
        re.match(r"^[a-z0-9-]+$", name) is not None
        and not name.startswith("-")
        and not name.endswith("-")
        and "--" not in name,
        f"{skill_md}: name must be lowercase hyphen-case",
    )
    require(len(name) <= MAX_SKILL_NAME_LENGTH, f"{skill_md}: name is too long")
    require("<" not in description and ">" not in description, f"{skill_md}: description has angle brackets")
    require(len(description) <= 1024, f"{skill_md}: description is too long")
    if expected_name:
        require(name == expected_name, f"{skill_md}: expected name {expected_name}, got {name}")


# --------------------------------------------------------------------------- #
# Structural wiring
# --------------------------------------------------------------------------- #

def iter_manifest_paths(manifest: dict):
    """Yield every relative path a manifest references."""
    for rel in manifest.get("always_load", []):
        yield rel
    for axis in manifest.get("axes", {}).values():
        for rel in axis.get("values", {}).values():
            yield rel
    for key in ("stages", "scripts"):
        for item in manifest.get(key, []):
            if isinstance(item, dict) and item.get("path"):
                yield item["path"]
    for item in manifest.get("delegates", []):
        if isinstance(item, dict) and item.get("path"):
            yield item["path"]
    for item in manifest.get("references", {}).get("on_demand", []):
        if isinstance(item, dict) and item.get("path"):
            yield item["path"]


def validate_skill_manifest_paths(skill_dir: Path) -> dict:
    manifest = load_yaml(skill_dir / "manifest.yaml")
    require((skill_dir / "SKILL.md").exists(), f"{skill_dir.name}: SKILL.md missing")
    for rel in iter_manifest_paths(manifest):
        resolved = (skill_dir / rel).resolve()
        require(resolved.exists(), f"{skill_dir.name}: manifest path does not resolve: {rel}")
    return manifest


def validate_evals(skill_dir: Path) -> None:
    """Each skill ships behavioral evals; keep them well-formed so they cannot rot silently."""
    evals_path = skill_dir / "evals/evals.json"
    require(evals_path.exists(), f"{skill_dir.name}: evals/evals.json missing")
    try:
        data = json.loads(read(evals_path))
    except json.JSONDecodeError as exc:
        raise AssertionError(f"{skill_dir.name}: evals/evals.json is not valid JSON: {exc}") from exc
    require(
        data.get("skill_name") == skill_dir.name,
        f"{skill_dir.name}: evals.json skill_name must equal the skill directory name",
    )
    evals = data.get("evals")
    require(
        isinstance(evals, list) and len(evals) > 0,
        f"{skill_dir.name}: evals.json must contain a non-empty evals list",
    )
    for item in evals:
        require(
            isinstance(item, dict) and item.get("id") and item.get("prompt"),
            f"{skill_dir.name}: every eval must have a non-empty id and prompt",
        )


def validate_root_router(root: Path) -> None:
    """The root SKILL.md is the discovered entry point; it must route to every sub-skill."""
    skill_md = root / "SKILL.md"
    validate_standard_skill_frontmatter(skill_md, expected_name="academic-writing-skills")
    router = read(skill_md)
    require("Academic-Writing-Skills" in router, "root SKILL.md must use the collection display name")
    for sib in (
        "skills/academic-writing/SKILL.md",
        "skills/academic-figure/SKILL.md",
        "skills/academic-citation/SKILL.md",
        "skills/academic-review/SKILL.md",
    ):
        require(sib in router, f"root SKILL.md must route to {sib}")


def validate_packaging_boundary(root: Path) -> None:
    """Local maintenance files may live in the workspace but must not be shipped."""
    gitignore = read(root / ".gitignore")
    for pattern in ("_local/", "SKILL-FLOW.md"):
        require(pattern in gitignore, f".gitignore must exclude local-only pattern: {pattern}")
    for doc_name in ("README.md", "README_EN.md"):
        doc = read(root / doc_name)
        require("--exclude '_local/'" in doc, f"{doc_name} must exclude _local/ in install commands")
        require("--exclude 'SKILL-FLOW.md'" in doc, f"{doc_name} must exclude SKILL-FLOW.md in install commands")
        require("--delete-excluded" in doc, f"{doc_name} must remove previously copied local-only files")
        require("cp -R Academic-writing" not in doc, f"{doc_name} must not use cp -R for installation")


def validate_shared_layer(root: Path) -> None:
    shared = root / "_shared"
    for rel in (
        "core/stance.md",
        "core/gates.md",
        "core/contract.md",
        "templates/index.md",
        "paper-types/index.md",
        "paper-types/journal/index.md",
        "venues/index.md",
        "checks/claim-evidence.md",
        "checks/metric-design.md",
    ):
        require((shared / rel).exists(), f"_shared essential missing: {rel}")
    metric_design = read(shared / "checks/metric-design.md")
    require(
        "Outcome semantics first" in metric_design
        and "compromise rate" in metric_design
        and "partial" in metric_design
        and "denominator" in metric_design,
        "metric-design must require explicit outcome semantics, compromise/partial handling, and denominators",
    )
    contract = read(shared / "core/contract.md")
    stance = read(shared / "core/stance.md")
    gates = read(shared / "core/gates.md")
    gates_flat = " ".join(gates.split())
    venues_index = read(shared / "venues/index.md")
    paper_types_index = read(shared / "paper-types/index.md")
    journal_index = read(shared / "paper-types/journal/index.md")
    journal_posture = read(shared / "venues/journal-vs-conference.md")

    require("static/core/gates.md" not in contract, "core contract must not point to removed static/core/gates.md")
    require("_shared/core/gates.md" in contract, "core contract must point to _shared/core/gates.md")
    require(
        "`academic-figure` skill's `references/figures/figure-planning.md`" in stance
        and "`academic-citation` skill's" in stance
        and "`academic-review` skill's" in stance,
        "shared stance must qualify sibling-skill figure and audit references",
    )
    require(
        "Terminal-facing checkpoint summaries mirror the user's interaction language" in stance
        and "Saved Writing Policy and Paper Framework artifacts stay English by default" in stance
        and "Do not use the artifact language as the terminal interaction language" in stance,
        "shared stance must separate terminal interaction language from saved artifact language",
    )
    require(
        "framework overview, Section Plan, Figure Plan" in stance
        and "localize their labels and natural-language cells" in stance,
        "shared stance must classify framework and Figure Plan checkpoint content as terminal interaction output",
    )
    require(
        "Always localize user-facing checkpoint labels to the interaction language" in gates_flat
        and "when appropriate" not in gates,
        "shared gates must make checkpoint label localization mandatory, not optional",
    )
    require(
        "_shared/paper-types/journal/" in venues_index
        and "_shared/paper-types/" in venues_index
        and "_shared/venues/journal-vs-conference.md" in venues_index,
        "venue index must use _shared paths for paper-type and journal-posture references",
    )
    require(
        "_shared/venues/index.md" in paper_types_index
        and "_shared/paper-types/journal/" in paper_types_index
        and "_shared/venues/journal-vs-conference.md" in paper_types_index,
        "paper-type index must use _shared paths",
    )
    for label, text in (
        ("conference paper-type index", paper_types_index),
        ("journal paper-type index", journal_index),
    ):
        require(
            "## Framework Main Content Contract" in text
            and "argument movement" in text
            and "one-sentence phrase" in text
            and "not a component checklist" in text
            and "problem/challenge -> gap -> contribution/insight -> advantage -> evidence" in text
            and "problem/gap -> contribution -> evidence preview" in text,
            f"{label} must define a concise Framework Main Content contract for section rows",
        )
    require(
        "_shared/venues/index.md" in journal_index
        and "_shared/paper-types/" in journal_index
        and "_shared/venues/journal-vs-conference.md" in journal_index,
        "journal paper-type index must use _shared paths",
    )
    require(
        "_shared/paper-types/journal/" in journal_posture
        and "`academic-writing` hub's `references/sections/journal/`" in journal_posture
        and "`academic-review` skill's `references/checks/journal-submission-elements.md`" in journal_posture,
        "journal-vs-conference must qualify journal paper-type, section-overlay, and review references",
    )
    for profile in (shared / "paper-types/journal").glob("*.md"):
        if profile.name == "index.md":
            continue
        text = read(profile)
        require(
            "references/venues/journal-vs-conference.md" not in text
            and "_shared/venues/journal-vs-conference.md" in text,
            f"{profile.relative_to(root)} must use _shared journal-posture path",
        )
    for venue in ("jmlr.md", "ieee-tpami.md", "journal-generic.md", "nature.md", "nature-communications.md"):
        text = read(shared / "venues" / venue)
        require(
            "academic-review` skill's `references/checks/journal-submission-elements.md" in text,
            f"_shared/venues/{venue} must qualify journal submission checks as academic-review-owned",
        )
    require(
        "Nature" in venues_index
        and "Nature Communications" in venues_index
        and "`nature.md`" in venues_index
        and "`nature-communications.md`" in venues_index,
        "venue index must expose Nature-family journal cards",
    )


def validate_no_stale_deleted_paths(root: Path) -> None:
    """Deleted academic-figure static/section files must not remain in live docs."""
    live_files = [root / "SKILL.md", root / "README.md", root / "README_EN.md"]
    local_flow = root / "SKILL-FLOW.md"
    if local_flow.exists():
        live_files.append(local_flow)
    live_files.extend((root / "_shared").rglob("*.md"))
    live_files.extend((root / "skills").rglob("*.md"))
    live_files.extend((root / "skills").rglob("*.yaml"))
    forbidden = (
        "../academic-figure/references/sections/figures-and-tables.md",
        "../academic-figure/static/figure-handling.md",
        "../academic-figure/static/table-handling.md",
        "references/sections/figures-and-tables.md",
        "static/figure-handling.md",
        "static/table-handling.md",
    )
    for path in live_files:
        if "_local" in path.parts:
            continue
        text = read(path)
        for stale in forbidden:
            require(stale not in text, f"{path.relative_to(root)} references deleted academic-figure path: {stale}")


# --------------------------------------------------------------------------- #
# Hub contract (academic-writing)
# --------------------------------------------------------------------------- #

def validate_hub(root: Path) -> None:
    hub = root / "skills/academic-writing"
    manifest = load_yaml(hub / "manifest.yaml")
    manifest_text = read(hub / "manifest.yaml")
    manifest_flat = " ".join(manifest_text.split())
    skill = read(hub / "SKILL.md")
    full_draft = read(hub / "static/workflow/full-draft.md")
    writing_policy = read(hub / "static/workflow/stages/writing-policy.md")
    paper_framework = read(hub / "static/workflow/stages/paper-framework.md")
    paper_framework_flat = " ".join(paper_framework.split())
    section_drafting = read(hub / "static/workflow/stages/section-drafting.md")
    latex_project = read(hub / "static/workflow/stages/latex-project.md")
    draft_revision = read(hub / "static/workflow/draft-revision.md")
    research_strategy = read(hub / "references/principles/research-strategy.md")
    paragraph_flow = read(hub / "references/sections/paragraph-flow.md")
    paragraph_flow_flat = " ".join(paragraph_flow.split())
    base_section_guides = {
        "abstract": read(hub / "references/sections/abstract.md"),
        "introduction": read(hub / "references/sections/introduction.md"),
        "related-work": read(hub / "references/sections/related-work.md"),
        "method": read(hub / "references/sections/method.md"),
        "experiments": read(hub / "references/sections/experiments.md"),
        "conclusion": read(hub / "references/sections/conclusion.md"),
        "appendix": read(hub / "references/sections/appendix.md"),
    }
    intro_guide = base_section_guides["introduction"]
    related_work_guide = base_section_guides["related-work"]
    method_guide = base_section_guides["method"]
    experiments_guide = base_section_guides["experiments"]
    experiments_flat = " ".join(experiments_guide.split())
    journal_intro = read(hub / "references/sections/journal/introduction.md")
    journal_index = read(hub / "references/sections/journal/index.md")
    journal_results = read(hub / "references/sections/journal/results.md")
    contract = read(root / "_shared/core/contract.md")

    # venue_kind routed before venue before paper_type
    require("venue_kind" in manifest_text, "manifest must define venue_kind axis")
    vk = skill.find("`venue_kind`")
    vn = skill.find("`venue`", vk + 1)
    pt = skill.find("`paper_type`", vn + 1)
    require(
        -1 not in {vk, vn, pt} and vk < vn < pt,
        "SKILL.md must route venue_kind before venue and paper_type",
    )
    require("default: conference" in manifest_text, "venue_kind must default to conference")
    require(
        "Select journal only when the user explicitly" in manifest_flat,
        "manifest must say journal is selected only from explicit user evidence",
    )
    venue_values = manifest["axes"]["venue"]["values"]
    require(
        venue_values.get("nature") == "../../_shared/venues/nature.md"
        and venue_values.get("nature-communications") == "../../_shared/venues/nature-communications.md"
        and "Nature-family" in manifest_flat
        and "Nature Communications" in manifest_flat,
        "manifest venue axis must route Nature-family journal targets to modeled journal cards",
    )
    require(
        "references/sections/journal/results.md" in manifest_text,
        "manifest must expose the journal Results overlay",
    )
    require(
        "manifest-mapped paper type profile path" in " ".join(writing_policy.split()),
        "Writing Policy stage must use the manifest-mapped paper type profile path",
    )
    require(
        "Do not load paper type, venue," not in full_draft
        and "Do not load venue cards, specific" in full_draft
        and "paper-type profiles" in full_draft
        and "figure/table references" in full_draft
        and "review references" in full_draft,
        "Full Draft gate must not forbid the Writing Policy's required paper-type family/check loads",
    )
    require(
        "Do NOT raise page/length budgets, per-section length" in writing_policy,
        "Writing Policy stage must defer page/length/budget decisions to Paper Framework",
    )
    require(
        "Do not encode numeric page counts in `Target venue`" in writing_policy
        and "submission / camera-ready / custom" in writing_policy,
        "Writing Policy stage must keep target venue identity separate from page-count or draft-stage decisions",
    )
    require(
        "venue kind" in contract.lower() and "conference" in contract and "journal" in contract,
        "core contract must include venue kind as part of paper identity",
    )

    # Core section budget contract lives in the Paper Framework stage now
    require(
        "#### Core Section Budget (protect the paper's center of gravity)" in paper_framework
        and "Primary core section" in paper_framework
        and "Evidence core section" in paper_framework
        and "Compress-first sections" in paper_framework
        and "Minimum floor" in paper_framework,
        "Paper Framework stage must identify core sections and minimum floors",
    )
    require(
        "| # | Section | Role | Main Content | Prose budget | Minimum floor | Compression rule |"
        in paper_framework,
        "Paper Framework checkpoint must expose role, prose budget, floor, and compression rule",
    )
    require(
        "Display-Item Page Budget" in paper_framework,
        "Paper Framework must budget display items separately from prose pages",
    )
    require(
        "Chart form" in paper_framework
        and "cross-figure visual variety check" in paper_framework
        and "do not let every numeric result figure default to bar charts" in paper_framework_flat,
        "Paper Framework must expose chart-form planning and block all-bar numeric figure sets",
    )
    require(
        "paper-type family index" in paper_framework
        and "Framework Main Content Contract" in paper_framework
        and "argument movement" in paper_framework
        and "one-sentence phrase" in paper_framework
        and "not a component checklist" in paper_framework,
        "Paper Framework must load and apply the paper-type Main Content contract",
    )
    require(
        "Journal Submission Package Plan" in paper_framework
        and "| Item | Required? | Source/status | Owner/reference | Blocker? |" in paper_framework
        and "Data/Code Availability" in paper_framework
        and "Reporting Summary" in paper_framework
        and "Cover letter" in paper_framework,
        "Paper Framework must materialize journal submission artifacts as a package plan",
    )
    require(
        "Terminal-facing Paper Framework checkpoint" in paper_framework_flat
        and "mirror the user's interaction language" in paper_framework_flat
        and "translate the overview headings, section summaries, Figure Plan summaries" in paper_framework_flat
        and "the saved framework artifact remains English by default" in paper_framework_flat,
        "Paper Framework checkpoint must mirror the user's interaction language while keeping the saved artifact English by default",
    )
    require(
        "Language routing invariant" in paper_framework
        and "Do not paste the English schema labels into a Chinese terminal checkpoint" in paper_framework_flat
        and "框架概览" in paper_framework
        and "章节计划" in paper_framework
        and "图表计划" in paper_framework
        and "请确认或修改" in paper_framework,
        "Paper Framework stage must include concrete interaction-language checkpoint labels for Chinese terminal output",
    )
    require(
        "Terminal checkpoints must include the Section Plan table" in paper_framework
        and "do not replace it with overview bullets" in paper_framework
        and "Section Plan is mandatory terminal output" in paper_framework,
        "Paper Framework terminal checkpoint must always show a concise Section Plan table",
    )
    require(
        "render `章节计划` as a Markdown table" in paper_framework
        and "| # | 章节 | 角色 | 主要内容 | 主文预算 | 底线 | 压缩规则 |" in paper_framework
        and "Do not write `章节为`" in paper_framework
        and "as a substitute for the table" in paper_framework,
        "Paper Framework terminal Section Plan must be a localized Markdown table, not prose",
    )
    require(
        "render `图表计划` as a Markdown table" in paper_framework
        and "| ID | 类型 | 图形形式 | 版式 | 位置章节 | 信息点 |" in paper_framework
        and "Do not write `图表计划包含`" in paper_framework
        and "as a substitute for the table" in paper_framework,
        "Paper Framework terminal Figure Plan must be a localized Markdown table, not prose",
    )
    require(
        "Chinese terminal chart-form values must be localized" in paper_framework
        and "schematic -> 示意图" in paper_framework
        and "donut -> 环形图" in paper_framework
        and "heatmap -> 热力图" in paper_framework
        and "table -> 表格" in paper_framework
        and "saved framework artifact keeps canonical English chart-form values" in paper_framework,
        "Paper Framework must localize terminal chart-form cell values while keeping saved artifacts canonical",
    )
    require(
        "Do not compress a primary-core section below its floor" in paper_framework
        and "return to the Paper Framework checkpoint" in paper_framework,
        "Paper Framework stage must block compressing core sections below the confirmed floor",
    )
    require(
        "Draft-stage page budget" in paper_framework
        and "submission / camera-ready / custom" in paper_framework
        and "Do not promote a camera-ready allowance into the submission limit" in paper_framework
        and "Submission content-page limit" in paper_framework
        and "Camera-ready allowance" in paper_framework,
        "Paper Framework stage must distinguish submission limits, camera-ready allowances, and custom page targets",
    )
    require(
        "Abstract and Introduction rows preserve the paper-type Main Content movement" in paper_framework
        and "not component inventories" in paper_framework,
        "Paper Framework self-check must block checklist-style Abstract/Introduction rows",
    )

    # Abstract / introduction logic chain (now in section-drafting stage)
    require(
        "problem -> challenge/gap -> insight/contribution -> advantage -> evidence" in section_drafting
        and "state purpose or advantage" in section_drafting,
        "Section drafting must gate Abstract/Introduction on a coherent logic chain",
    )
    require(
        "```mermaid" in intro_guide
        and "Evidence preview" in intro_guide
        and "550-750 words" in intro_guide
        and "% Evidence preview (optional one sentence, no specific experiment recap)" in intro_guide,
        "Introduction guide must use the reference-style logic map, length budget, and evidence-preview skeleton",
    )
    require(
        "% Experiment" not in intro_guide
        and "one brief experiment mention" not in intro_guide
        and "experiment mention" not in intro_guide,
        "Introduction guide must not model a separate experiment block or experiment mention",
    )
    require(
        "What technical problem do we solve, and why is there no well-established solution?" in intro_guide
        and "What are the contributions of our pipeline" in intro_guide
        and "what new insight do they bring?" in intro_guide
        and "How can prior methods be written to lead readers to the technical challenge we solve" in intro_guide
        and "Introduce the paper's task." in intro_guide
        and "Use discussion of prior methods to lead to the technical challenge we solve." in intro_guide
        and "To solve this technical challenge, present the contributions we propose." in intro_guide
        and "express our new insight" in intro_guide,
        "Introduction guide must use the approved backward/forward planning questions",
    )
    require(
        "## Required Output" not in intro_guide
        and "For Full Draft Workflow" not in intro_guide
        and "Draft Revision Workflow" not in intro_guide,
        "Introduction guide must not define workflow-specific output contracts",
    )
    for section_name, section_guide in base_section_guides.items():
        require(
            "## Required Output" not in section_guide
            and "For Full Draft Workflow" not in section_guide
            and "Draft Revision Workflow" not in section_guide
            and "corresponding section file" not in section_guide,
            f"{section_name} guide must not define workflow-specific output contracts",
    )
    require(
        "## Method Completeness Check" in method_guide
        and "motivation, design, technical advantage, and evidence hook" in " ".join(method_guide.split())
        and "reader cannot reconstruct the algorithm, architecture, training/inference flow, protocol, or implementation-critical settings"
        in " ".join(method_guide.split()),
        "Method guide must define content completeness, not page-floor enforcement",
    )
    for forbidden in (
        "## Method Floor Check",
        "page floor",
        "confirmed Paper Framework marks",
        "below the confirmed floor",
    ):
        require(
            forbidden not in method_guide,
            f"Method guide must not own page-floor enforcement: {forbidden}",
        )
    require(
        "motivation, design, technical advantage, and evidence hook" in " ".join(section_drafting.split())
        and "an overview/section-map opens the section" in " ".join(section_drafting.split())
        and "terms defined before use" in " ".join(section_drafting.split()),
        "Section drafting Method required moves must include evidence hooks and local completeness checks",
    )
    require(
        "Introduction chain:" in section_drafting
        and "no separate experiment paragraph" in section_drafting,
        "Section drafting must keep Introduction on rhetorical flow and forbid a separate experiment paragraph",
    )
    require(
        "## What Flow Means" in paragraph_flow
        and "clarity, coherence, and conciseness" in paragraph_flow_flat
        and "does this make sense" in paragraph_flow
        and "can readers understand" in paragraph_flow,
        "Paragraph flow guide must include the reference flow definition",
    )
    require(
        "## Reader Perspective Check" in paragraph_flow
        and "external reader" in paragraph_flow
        and "vocabulary" in paragraph_flow
        and "body paragraphs connect back to the section thesis" in paragraph_flow_flat
        and "not familiar with the topic" in paragraph_flow,
        "Paragraph flow guide must include the reader-perspective check",
    )
    require(
        "## Reverse Outline Check" in paragraph_flow
        and "thesis statement" in paragraph_flow
        and "topic sentence" in paragraph_flow
        and "points of evidence or explanation" in paragraph_flow
        and "revise it or remove it" in paragraph_flow,
        "Paragraph flow guide must include the reference reverse-outline contents",
    )
    require(
        "## Headings And Sections As Flow Check" in paragraph_flow
        and "complete outline" in paragraph_flow
        and "sections and subsections with headings" in paragraph_flow
        and "what each part is about" in paragraph_flow
        and "drafting and revision" in paragraph_flow,
        "Paragraph flow guide must include headings/sections as a flow diagnostic",
    )
    for required in (
        "## Transition Cues",
        "cause and effect",
        "comparison",
        "contrast or exception",
        "example",
        "place or position",
        "time",
        "summary or conclusion",
        "accordingly",
        "as a result",
        "because",
        "consequently",
        "hence",
        "therefore",
        "thus",
        "also",
        "in the same way",
        "likewise",
        "similarly",
        "although",
        "nevertheless",
        "nonetheless",
        "on the contrary",
        "for instance",
        "indeed",
        "adjacent to",
        "simultaneously",
        "thereafter",
        "in brief",
        "to summarize",
    ):
        require(
            required in paragraph_flow,
            f"Paragraph flow guide must include reference transition content: {required}",
        )
    require(
        not (hub / "references/sections/demo-application.md").exists(),
        "Demo/Application must not exist as a standalone section guide",
    )
    demo_scope_text = "\n".join((manifest_text, section_drafting, research_strategy, journal_index))
    for forbidden in (
        "references/sections/demo-application.md",
        "Demo / Application",
        "Demo/Application",
        "applications or demos",
    ):
        require(
            forbidden not in demo_scope_text,
            f"Hub must not route or recommend a standalone demo/application section: {forbidden}",
        )
    require(
        "main ablation table and matching visualization" in experiments_flat
        and "core contributions and major components affect method performance" in experiments_flat
        and "focused ablation tables and matching visualizations" in experiments_flat
        and "within one pipeline module" in experiments_flat
        and "hyperparameter sensitivity" in experiments_flat
        and "input-quality sensitivity" in experiments_flat
        and "removing a design choice" in experiments_flat,
        "Experiments guide must define main and module-level ablation tables with matching visualizations",
    )
    require(
        "## Display Evidence Role" in experiments_guide
        and "which claims need a table or figure" in experiments_flat
        and "what each display item proves" in experiments_flat
        and "academic-figure" in experiments_guide
        and "caption, span, booktabs, overflow, and QA" in experiments_flat,
        "Experiments guide must only decide display evidence roles and delegate design to academic-figure",
    )
    for forbidden in (
        "## Applications Or Demos",
        "applications or demos",
        "## Figure And Table Rules",
        "### Hard Rules",
        "### Readability Rules",
        "### Caption Rules",
        "Put caption above the table",
        "Use `booktabs` style",
        "diagnostics → demos",
    ):
        require(
            forbidden not in experiments_guide,
            f"Experiments guide must not own demo/display design rules: {forbidden}",
        )
    require(
        "List directly competing and recent baseline papers first" in related_work_guide
        and "Use 2-4 focused topics" in related_work_guide,
        "Related Work guide must preserve the reference-style baseline-first and focused-topic rules",
    )
    require(
        "base Section Skeleton" in journal_intro
        and "five-block Section Skeleton" not in journal_intro,
        "Journal introduction overlay must inherit the revised base skeleton, not the old five-block skeleton",
    )
    require(
        "Results narrative, not a conference dump" in journal_results
        and "Experiments / Evaluation" in journal_results
        and "research questions -> findings -> evidence -> interpretation" in journal_results
        and "Do not rename every empirical section to Results automatically" in journal_results,
        "Journal results overlay must adapt Experiments/Evaluation into journal-style Results without forcing renames",
    )
    require(
        "glossary-style taxonomy subsection" in section_drafting,
        "Section drafting must block glossary-style taxonomy definition lists",
    )
    require(
        "disguised form" in section_drafting
        and "\\textbf{V1 (...)}." in section_drafting
        and "do not also re-define every member in prose" in section_drafting,
        "Section drafting must ban the bold-run-in taxonomy dump and require the body->appendix move",
    )
    appendix_guide = base_section_guides["appendix"]
    require(
        "Appendix / Supplement Plan" in paper_framework
        and "`paper/appendix-plan.md`" in paper_framework
        and all(
            token in paper_framework
            for token in ("Claim backed", "Source availability", "Fill status", "Fallback", "Main-text anchor")
        ),
        "Paper Framework must explicitly plan appendix/supplement items and the appendix-plan fields",
    )
    require(
        "Appendix / Supplement" in section_drafting
        and "references/sections/appendix.md" in section_drafting
        and "Claim backed" in section_drafting,
        "Section drafting must route appendix/supplement drafting through the appendix guide",
    )
    require(
        "Appendix / Supplement rewrite" in draft_revision
        and "references/sections/appendix.md" in draft_revision
        and "table-placement.md" in draft_revision
        and "submission-readiness.md" in draft_revision,
        "Draft Revision must support appendix/supplement rewrite and audit requests",
    )
    stale_figure_paths = (
        "../academic-figure/references/sections/figures-and-tables.md",
        "../academic-figure/static/figure-handling.md",
        "../academic-figure/static/table-handling.md",
    )
    for stale_path in stale_figure_paths:
        require(
            stale_path not in draft_revision
            and stale_path not in full_draft
            and stale_path not in paper_framework
            and stale_path not in section_drafting,
            f"academic-writing hub must not reference stale academic-figure path: {stale_path}",
        )
    require(
        "../academic-figure/references/prose/display-in-prose.md" in draft_revision
        and "../academic-figure/references/tables/table-design.md" in draft_revision
        and "../academic-figure/references/tables/table-placement.md" in draft_revision,
        "Draft Revision must route figure/table prose and table mechanics through current academic-figure references",
    )
    require(
        "create `paper/appendix-plan.md`" in latex_project
        and "sections/A_appendix.tex" in latex_project
        and "delete the template appendix hook" in latex_project,
        "LaTeX project setup must create appendix artifacts when planned and remove stale appendix hooks otherwise",
    )
    require(
        "## Appendix Is Support, Not A Second Main Paper" in appendix_guide
        and "Do not hide main evidence" in appendix_guide
        and "2-4 sentence lead paragraph" in appendix_guide
        and "No stubs" in appendix_guide,
        "Appendix guide must keep appendix support-only, source-aware, substantive, and non-stubbed",
    )

    # Orchestrator delegates to the three sibling skills
    for sib in ("academic-figure", "academic-citation", "academic-review"):
        require(sib in full_draft, f"orchestrator must delegate to {sib}")

    # A "write the draft" request must complete the whole chain, not emit a marker-only skeleton
    require(
        "Completion means the whole chain, not a skeleton." in full_draft,
        "orchestrator must state that a draft request completes the figure/citation chain, not a skeleton",
    )
    require(
        "four mandatory parts" in full_draft
        and all(s in full_draft for s in ("academic-figure", "academic-citation", "academic-review")),
        "orchestrator must enumerate the four-part chain (hub + figure + citation + review) as mandatory",
    )
    require(
        "is NOT an acceptable end" in section_drafting,
        "section drafting must forbid deferring producible figures/tables/citations as markers",
    )

    # A named modeled venue (e.g. EMNLP) must force its bundled template, not a generic fallback
    require(
        "Silently falling back to" in latex_project and "_shared/templates/index.md" in latex_project,
        "latex-project must resolve the venue template via index.md and forbid the generic fallback",
    )
    require(
        "Silently falling back to" in paper_framework,
        "paper-framework must forbid the generic-template fallback when a modeled venue is confirmed",
    )
    templates_index = read(root / "_shared/templates/index.md")
    require(
        "search the web for and download the official template" in templates_index
        and "report this to the user explicitly" in templates_index,
        "templates index must require web fetch for unbundled named venues and a reported generic fallback",
    )

    # Paper type families
    values = manifest["axes"]["paper_type"]["values"]
    conference = [k for k in values if not k.startswith("journal-")]
    journal = [k for k in values if k.startswith("journal-")]
    require(conference and journal, "both conference and journal paper-type families required")
    for k in conference:
        require(
            "/paper-types/journal/" not in values[k],
            f"conference paper type points to journal profile: {k}",
        )
    for k in journal:
        require(
            "/paper-types/journal/" in values[k],
            f"journal paper type does not point to journal profile: {k}",
        )

    # Venue cards declare Venue Kind
    for venue, rel in manifest["axes"]["venue"]["values"].items():
        if venue == "generic":
            continue
        text = read((hub / rel))
        require("## Venue Kind\n\n- " in text, f"{rel} must declare Venue Kind")
        expected = (
            "journal"
            if venue in {"jmlr", "tpami", "ieee-tpami", "journal", "nature", "nature-communications"}
            else "conference"
        )
        require(f"## Venue Kind\n\n- {expected}" in text, f"{rel} must declare Venue Kind {expected}")

    nature = read(root / "_shared/venues/nature.md")
    nat_comms = read(root / "_shared/venues/nature-communications.md")
    require(
        "summary paragraph" in nature
        and "broad multidisciplinary audience" in nature
        and "Methods after references" in nature
        and "Extended Data" in nature,
        "Nature venue card must capture broad-audience, summary paragraph, Methods, and Extended Data constraints",
    )
    require(
        "Methods-in-cap trap" in nat_comms
        and "5,000" in nat_comms
        and "10 display items" in nat_comms
        and "Reporting Summary" in nat_comms
        and "Cover letter" in nat_comms,
        "Nature Communications card must capture Methods-in-cap, display cap, reporting, and cover-letter constraints",
    )

    emnlp = read(root / "_shared/venues/emnlp.md")
    require(
        "Verified for: EMNLP 2026 main conference plus ARR submission requirements" in emnlp
        and "Submission content limit: long papers 8 pages; short papers 4 pages" in emnlp
        and "Camera-ready allowance: accepted long papers up to 9 pages; accepted short papers up to 5 pages" in emnlp
        and "Do not use the camera-ready allowance as the submission-stage budget" in emnlp,
        "EMNLP venue card must separate current submission limits from camera-ready allowances",
    )

    # Paper-type profiles declare the Priority Contract
    for profile in (root / "_shared/paper-types").glob("**/*.md"):
        if profile.name == "index.md":
            continue
        text = profile.read_text(encoding="utf-8")
        rel = profile.relative_to(root)
        require("## Priority Contract" in text, f"{rel} must declare a Priority Contract")
        require("Primary core:" in text, f"{rel} must name its primary core section")
        require("Evidence core:" in text, f"{rel} must name its evidence core section")
        require("Compress first:" in text, f"{rel} must name compress-first sections")
        require("floor" in text.lower(), f"{rel} must state a core-section floor")
        require(
            "## Section Structure (Paper Framework hard default)" in text,
            f"{rel} must anchor its section list as a Paper Framework hard default",
        )
        require(
            "Do not copy this structure mechanically" not in text,
            f"{rel} must not invite mechanical-deviation language that contradicts the hard default",
        )


# --------------------------------------------------------------------------- #
# Sibling skills
# --------------------------------------------------------------------------- #

def validate_figure_skill(root: Path) -> None:
    fig = root / "skills/academic-figure"
    figure_router = read(fig / "workflows/figure.md")
    plot_handling = read(fig / "workflows/plot.md")
    schematic_handling = read(fig / "workflows/schematic.md")
    picture_handling = read(fig / "workflows/picture.md")
    table_handling = read(fig / "workflows/table.md")
    display_prose = read(fig / "references/prose/display-in-prose.md")
    table_design = read(fig / "references/tables/table-design.md")
    table_placement = read(fig / "references/tables/table-placement.md")
    figure_planning = read(fig / "references/figures/figure-planning.md")
    plot_style = read(fig / "references/figures/plot-style.md")
    chart_taxonomy = read(fig / "references/figures/chart-taxonomy.md")
    chart_patterns = read(fig / "references/figures/chart-patterns.md")
    conf_sizing = read(fig / "references/figures/conference/figure-sizing.md")
    schematic_design = read(fig / "references/figures/schematic-design.md")
    picture_generation = read(fig / "references/figures/picture-generation.md")
    paper_figure_server = read(fig / "mcp-servers/paper-figure/server.py")
    figure_manifest = read(fig / "manifest.yaml")
    figure_skill = read(fig / "SKILL.md")

    require(
        not (fig / "static/figure-handling.md").exists()
        and not (fig / "static/table-handling.md").exists()
        and not (fig / "references/sections/figures-and-tables.md").exists(),
        "academic-figure must use workflows/ and references/prose/ instead of stale static/sections paths",
    )
    require(
        "workflows/plot.md" in figure_manifest
        and "workflows/schematic.md" in figure_manifest
        and "workflows/picture.md" in figure_manifest
        and "workflows/table.md" in figure_manifest
        and "references/figures/schematic-design.md" in figure_manifest
        and "references/prose/display-in-prose.md" in figure_manifest
        and "static/figure-handling.md" not in figure_manifest
        and "static/table-handling.md" not in figure_manifest
        and "references/sections/figures-and-tables.md" not in figure_manifest,
        "academic-figure manifest must route through plot/schematic/picture/table workflows and prose display reference",
    )
    require(
        "Plot =" in figure_skill
        and "Schematic =" in figure_skill
        and "Picture =" in figure_skill
        and "Table =" in figure_skill
        and "manifest.yaml is the detailed routing table" in figure_skill
        and "static/" not in figure_skill
        and "references/sections/figures-and-tables.md" not in figure_skill,
        "academic-figure SKILL.md must be a concise router with explicit display-item distinctions",
    )

    require(
        "Column-Span Decision" in figure_planning
        and "pipeline / framework / architecture" in figure_planning
        and "teaser / first concept figure" in figure_planning
        and "one multi-panel `figure*` with a shared legend" in figure_planning,
        "figure-planning must define the column-span decision (teaser single, pipeline/multi-panel span)",
    )
    require(
        "terminal-facing Paper Framework checkpoint" in figure_planning
        and "saved framework artifact may keep the English schema" in figure_planning
        and "`图表计划`" in figure_planning
        and "`类型`" in figure_planning
        and "`生成路径`" in figure_planning,
        "figure-planning must localize terminal Figure Plan labels while preserving the saved artifact schema",
    )
    require(
        "Chinese terminal chart-form values must be localized" in figure_planning
        and "schematic -> 示意图" in figure_planning
        and "donut -> 环形图" in figure_planning
        and "heatmap -> 热力图" in figure_planning
        and "table -> 表格" in figure_planning,
        "figure-planning must localize terminal chart-form cell values",
    )
    require(
        "Figure Plan must be rendered as a Markdown table" in figure_planning
        and "Do not replace it with a prose list such as `图表计划包含`" in figure_planning,
        "figure-planning must forbid prose-only Figure Plan summaries",
    )
    require(
        "Chart Form Diversity Gate" in figure_planning
        and "claim-to-chart fit beats visual novelty" in figure_planning
        and "donut" in figure_planning
        and "not every numeric display item should be a bar chart" in figure_planning,
        "figure-planning must require semantics-first chart-form variety across a paper",
    )
    require(
        "cross-figure chart-form audit" in plot_handling
        and "composition / coverage" in plot_handling
        and "avoid defaulting every numeric plot to bars" in plot_handling,
        "plot workflow must audit chart-form diversity before rendering paper-level plot sets",
    )
    require(
        "Single-column papers have no cross-column float class" in figure_planning
        and "size by role as a fraction of `\\linewidth`" in figure_planning
        and "story/teaser" in figure_planning,
        "figure-planning must explicitly define single-column paper figure placement by linewidth fractions",
    )
    require(
        "First-figure vs. main-process rule" in figure_planning
        and "0.55--0.75\\linewidth" in figure_planning
        and "one-column full-width figures as `double-column`" in figure_planning,
        "figure-planning must distinguish two-column teaser/framework span from one-column width fractions",
    )
    require(
        "references/figures/chart-taxonomy.md" in figure_manifest
        and "references/figures/chart-taxonomy.md" in plot_handling
        and "chart family" in plot_handling,
        "academic-figure must route data plots through chart-taxonomy before plotting",
    )
    require(
        "deterministic technical diagrams" in schematic_handling
        and "references/figures/schematic-design.md" in schematic_handling
        and "Do not send formal framework/pipeline/architecture diagrams to an image model by default" in schematic_handling
        and "FigureSpec -> SVG/PDF/PNG" in schematic_handling
        and "FigureSpec is the default" in schematic_design
        and "Do not route a formal technical schematic to an image model by default" in schematic_design,
        "academic-figure must route framework/pipeline/architecture through deterministic schematic guidance by default",
    )
    require(
        "picture-style figures" in picture_handling
        and "Confirm this is not a formal framework/pipeline/architecture schematic" in picture_handling
        and "Picture Brief" in picture_handling
        and "Formal pipeline" in picture_generation
        and "default to" in picture_generation
        and "`schematic-design.md`" in picture_generation,
        "academic-figure must keep picture workflow separate from formal schematic diagrams",
    )
    require(
        "Core conclusion first" in chart_taxonomy
        and "Evidence chain" in chart_taxonomy
        and "Data and statistics contract" in chart_taxonomy
        and "Palette and label contract" in chart_taxonomy
        and "Export and QA contract" in chart_taxonomy,
        "chart-taxonomy must enforce the conclusion/evidence/statistics/layout/palette/export gate",
    )
    for required_chart_kind in (
        "Vertical bar chart",
        "Horizontal bar chart",
        "Grouped bar chart",
        "Stacked bar chart",
        "Line chart",
        "Scatter plot",
        "Pareto frontier plot",
        "Radar chart",
        "Heatmap",
        "Box plot",
        "Histogram",
        "Violin plot",
        "Density plot",
        "Pie chart",
        "Donut chart",
    ):
        require(
            required_chart_kind in chart_taxonomy,
            f"chart-taxonomy must include reusable guidance for {required_chart_kind}",
        )
    require(
        "Palette Presets" in chart_taxonomy
        and "hero-baseline" in chart_taxonomy
        and "semantic-risk-capability" in chart_taxonomy
        and "distribution-neutral" in chart_taxonomy
        and "composition-muted" in chart_taxonomy,
        "chart-taxonomy must define reusable palette presets",
    )
    require(
        "horizontal_bars" in chart_patterns
        and "stacked_bars" in chart_patterns
        and "scatter_with_pareto" in chart_patterns
        and "distribution_plot" in chart_patterns
        and "pie_or_donut" in chart_patterns,
        "chart-patterns must provide helpers for the expanded chart families",
    )
    require(
        "Preset: shared-legend radar" in chart_taxonomy
        and "two polar panels" in chart_taxonomy
        and "one shared legend below the figure" in chart_taxonomy
        and "no filled polygons" in chart_taxonomy,
        "chart-taxonomy must define the shared-legend radar preset",
    )
    require(
        "Preset: compact labeled donut" in chart_taxonomy
        and "thick ring" in chart_taxonomy
        and "outside code-percentage labels" in chart_taxonomy
        and "bottom legend maps codes to full labels" in chart_taxonomy,
        "chart-taxonomy must define the compact labeled donut preset",
    )
    require(
        "Body compact mode" in chart_taxonomy
        and "0.58--0.72\\textwidth" in chart_taxonomy
        and "omit the bottom legend" in chart_taxonomy
        and "full code definitions live in the caption, appendix, or nearby table" in chart_taxonomy,
        "chart-taxonomy must define a body-compact donut mode for non-hero coverage figures",
    )
    require(
        "draw_shared_legend_radar" in chart_patterns
        and "draw_compact_labeled_donut" in chart_patterns
        and "white wedge separators" in chart_patterns,
        "chart-patterns must expose reusable shared-legend radar and compact labeled donut helpers",
    )
    require(
        "body_compact=False" in chart_patterns
        and "if body_compact:" in chart_patterns
        and "legend should be omitted" in chart_patterns
        and "figsize=(5.6, 2.15)" in chart_patterns,
        "chart-patterns must support a body-compact labeled donut helper mode",
    )
    require(
        "Column-Span Quick Rule" in conf_sizing,
        "conference figure-sizing must carry the column-span quick rule",
    )
    require(
        "Span Decision Matrix" in conf_sizing
        and "ACL / EMNLP two-column" in conf_sizing
        and "`figure` + `width=\\columnwidth`" in conf_sizing
        and "`figure*` + `width=0.90--1.00\\textwidth`" in conf_sizing
        and "One-column template" in conf_sizing
        and "`figure` + `width=0.45--1.00\\linewidth`" in conf_sizing,
        "conference figure-sizing must provide a deterministic figure span decision matrix",
    )
    require(
        "Single-column paper quick rule" in conf_sizing
        and "`figure*` is unavailable" in conf_sizing,
        "conference figure-sizing must state the single-column paper quick rule",
    )
    require(
        "table-handling.md" not in figure_router
        and "table-handling.md" not in plot_handling
        and "table-handling.md" not in schematic_handling
        and "table-handling.md" not in picture_handling
        and "Python (matplotlib/seaborn) is the default plotting backend. Python" not in plot_style
        and table_handling.count("if no Figure Plan is available") == 1
        and "In short: do not special-case literal model names" not in table_handling,
        "academic-figure workflow/reference files must avoid stale paths and duplicated summary sentences",
    )
    require(
        "Long headers overflow narrow columns" in table_handling,
        "table-handling must flag long-header overflow at small column counts",
    )
    require(
        "load-bearing main-results table" in table_handling
        and "one-column paper" in table_handling
        and "table density class" in table_handling,
        "table-handling must define double-column and one-column table span decisions",
    )
    require(
        len(table_handling.split()) <= 900
        and "Execution-only table workflow" in table_handling
        and "Do not repeat table-design or placement rules here" in table_handling,
        "table-handling must stay a concise execution layer instead of duplicating deep table rules",
    )
    require(
        "scripts/inspect_table_data.py" in figure_manifest
        and "inspect_table_data.py" in table_handling
        and "schema inspection JSON" in table_handling,
        "academic-figure must expose and use a lightweight table schema inspector",
    )

    require(
        "paper/framework-execution-report.md" in figure_skill
        and "paper/framework-execution-report.md" in figure_router
        and "paper/framework-execution-report.md" in plot_handling
        and "paper/framework-execution-report.md" in schematic_handling
        and "paper/framework-execution-report.md" in picture_handling
        and "0.60--0.70\\linewidth" in figure_planning
        and ">0.70\\linewidth" in figure_planning,
        "academic-figure workflows must enforce Paper Framework Figure Plan alignment and compact widths",
    )
    require(
        "Never let a table overflow" in table_handling
        and "hard defect" in table_handling
        and "Generate width-safe table source on the first pass" in table_handling
        and "Never hard-code structural numbers in source" in table_handling,
        "table-handling must make overflow a hard defect and forbid hard-coded structural numbers",
    )
    require(
        "Never let a table overflow" in table_placement and "appendix" in table_placement.lower(),
        "table-placement guide must make body and appendix overflow a hard defect",
    )
    require(
        "Prose-only display guidance" in display_prose
        and "does not decide body-vs-appendix placement" in display_prose
        and "references/tables/table-placement.md" in display_prose
        and "What Belongs In The Main Text" not in display_prose
        and "Body-vs-Appendix Decision Checklist" not in display_prose
        and "Table Toolbox" not in display_prose
        and "Table Pattern Selection" not in display_prose
        and "Single-column vs. cross-column (`table` vs. `table*`)" not in display_prose,
        "display-in-prose must stay prose/caption guidance and delegate placement/table mechanics",
    )
    require(
        "Table Routing" not in plot_style
        and "references/tables/table-design.md" not in plot_style
        and "references/tables/table-placement.md" not in plot_style
        and "LaTeX Table Toolbox" not in plot_style
        and "tabularx" not in plot_style,
        "plot-style must not own table routing or LaTeX mechanics",
    )
    require(
        "Placement summary" in table_design
        and "Span Decision" not in table_design
        and "Body-vs-Appendix Decision Checklist" not in table_design
        and "claim criticality" not in table_design
        and "Table kind" in table_design
        and "Visual grammar" in table_design,
        "table-design must own visual/table-type contracts and delegate placement decisions",
    )
    require(
        "sparse headline result" in table_placement
        and "do not stretch sparse content" in table_placement
        and "Appendix Plan" in table_placement,
        "table/appendix guidance must cover sparse headline tables and appendix planning",
    )
    require(
        "Body-vs-Appendix Decision Checklist" in table_placement
        and "claim criticality" in table_placement
        and "reader necessity" in table_placement
        and "density" in table_placement
        and "novelty" in table_placement
        and "page pressure" in table_placement
        and "full-version need" in table_placement
        and "keep in the body" in table_placement
        and "move to appendix" in table_placement
        and "move to supplement" in table_placement,
        "table placement guidance must include an explicit body-vs-appendix decision checklist",
    )
    require(
        "Data source" in table_design
        and "Source artifact" in table_design
        and "Metric direction unknown" in table_design
        and "do not guess metric direction" in table_design
        and "Cross-table consistency" in table_design
        and "method order" in table_design
        and "metric precision" in table_design
        and "public method name" in table_design,
        "table-design must preserve provenance, metric-direction uncertainty, and cross-table consistency",
    )
    require(
        "central scorecard" in table_design
        and "scorecard" in table_design
        and "table-placement.md" in table_design,
        "table-design must define central scorecards as a table type while delegating span decisions",
    )
    require(
        "Do not promote compact secondary result tables to `table*`" in table_handling
        and "secondary multi-metric table" in table_placement
        and "single-column unless it is unreadable" in table_placement,
        "table guidance must keep compact secondary result tables single-column unless unreadable",
    )
    require(
        "Own-method row highlight" in table_handling
        and "bolding alone is not enough" in table_handling
        and "light `\\rowcolor`/`\\cellcolor`" in table_design
        and "redundant with bold" in table_design,
        "table guidance must require redundant light highlighting for a best own-method bottom row",
    )
    require(
        "heavier top/bottom booktabs rules" in table_design
        and "`\\heavyrulewidth`" in table_design
        and "`\\specialrule`" in table_design
        and "never box the table" in table_design,
        "table guidance must define polished booktabs outer-rule weight without boxed tables",
    )
    require(
        "italic group labels" in table_design
        and "`\\cmidrule`" in table_design
        and "fine grouping rules" in table_design
        and "category comparison" in table_handling,
        "table guidance must define grouped/category comparison styling",
    )
    require(
        "Bold table headers" in table_handling
        and "multi-level column headers" in table_design
        and "bold spanner headers" in table_design
        and "bold leaf column headers" in table_design,
        "table guidance must require bold spanner and leaf column headers for polished scorecards",
    )
    require(
        "Own-method separator" in table_handling
        and "before the own-method row" in table_design
        and "separate it with a `\\midrule`" in table_design,
        "table guidance must require a separator before the own-method row",
    )
    require(
        "Polished scorecard default" in table_design
        and "not example-specific" in table_design
        and "adapt the same visual grammar to the paper's metrics" in table_design
        and "general table-design default" in table_handling,
        "table guidance must make the polished scorecard style a general default, not a one-off example",
    )
    require(
        "Universal Table Visual Grammar" in table_design
        and "not fitted to one dataset" in table_design
        and "bold every header level" in table_design
        and "one explicit separator before an own/proposed/full-method final block" in table_design
        and "Do not special-case literal model names" in table_handling
        and "Reuse the visual grammar across future papers" in table_handling,
        "table guidance must generalize polished styling across future papers instead of sample-specific layouts",
    )
    require(
        "if no Figure Plan is available" in table_handling
        and "infer a provisional table type" in table_handling
        and "Table Type Pattern Library" in table_design
        and "core claim or reader task" in table_design,
        "table guidance must classify tables from evidence role and data shape when no Figure Plan exists",
    )
    require(
        "Never paste the prompt scaffolding into the image" in picture_generation
        and "`Message:`" in picture_generation
        and "f\"Message: {message}\"" not in paper_figure_server
        and "\"Show exactly these visual elements:\"" not in paper_figure_server
        and "\"Use exactly these labels:\"" not in paper_figure_server,
        "paper-figure MCP must generate clean Direct Image Prompts, not rubric-style prompt scaffolding",
    )
    require(
        "ET.SubElement(svg, \"text\")  # placeholder" not in paper_figure_server,
        "render_figurespec must not emit blank placeholder text nodes",
    )
    for required_table_kind in (
        "main result table",
        "multi-dataset comparison table",
        "multi-metric comparison table",
        "ablation table",
        "hyperparameter sensitivity table",
        "data split table",
        "benchmark summary table",
        "training configuration table",
    ):
        require(
            required_table_kind in table_design,
            f"table-design must include a reusable pattern for {required_table_kind}",
        )
    require(
        "selected/default setting row" in table_design
        and "counts and percentages" in table_design
        and "key-value or phase-grouped layout" in table_design
        and "not performance highlights" in table_design,
        "table-design must distinguish sensitivity, data split, and configuration table styling from result-table styling",
    )


def validate_citation_skill(root: Path) -> None:
    cit = root / "skills/academic-citation"
    skill = read(cit / "SKILL.md")
    manifest = read(cit / "manifest.yaml")
    workflow = read(cit / "static/citation-workflow.md")
    integrity = read(cit / "references/checks/citation-integrity.md")
    source_routing = read(cit / "references/search/source-routing.md")
    audit = read(cit / "scripts/audit_citations.py")

    require(
        not any(cit.rglob("__pycache__")) and not any(cit.rglob("*.pyc")),
        "academic-citation must not ship Python cache artifacts",
    )
    require(
        "axes:" in manifest
        and "workflow:" in manifest
        and "search:" in manifest
        and "verify:" in manifest
        and "audit:" in manifest
        and "references/search/source-routing.md" in manifest,
        "academic-citation manifest must expose search/verify/audit workflow routing and source-routing reference",
    )
    require(
        "workflow axis" in skill
        and "Source routing" in skill
        and "Do not copy the detailed BibTeX rules into this router" in skill,
        "academic-citation SKILL.md must stay a concise router and delegate deep rules",
    )
    require(
        "Complete author lists required" in workflow
        and "Stable identifier required" in workflow
        and "generated `*.bbl`" in workflow
        and "rendered `and N others`" in workflow
        and "audit_citations.py" in workflow,
        "citation-workflow must state author-list, identifier, rendered-bibliography, and audit rules",
    )
    require(
        "Static audit boundary" in workflow
        and "does not prove claim support" in workflow
        and "Citation Evidence Ledger" in workflow
        and "Claim ID" in workflow
        and "metadata source" in workflow
        and "support grade" in workflow,
        "citation workflow must separate static audit from support verification and define the evidence ledger",
    )
    require(
        "Source Tier Routing" in source_routing
        and "DBLP" in source_routing
        and "CrossRef" in source_routing
        and "arXiv" in source_routing
        and "Semantic Scholar" in source_routing
        and "OpenAlex" in source_routing
        and "PubMed" in source_routing
        and "metadata-only candidate" in source_routing
        and "Google Scholar is not the default verification backbone" in source_routing,
        "source-routing must define trusted-source selection, fallback, and metadata-only limits",
    )
    require(
        "paper/*.bbl" in integrity
        and "visible DOI, URL, or arXiv marker" in integrity,
        "citation-integrity must treat generated .bbl files as part of the audit surface",
    )
    require(len(integrity) > 0, "citation-integrity reference must exist")
    require(
        ("min-citations" in audit or "min_citations" in audit)
        and "audit_rendered_bibliography" in audit
        and "RENDERED_PLACEHOLDER_AUTHOR_RE" in audit,
        "audit_citations.py must exist, run, and check rendered bibliography artifacts",
    )
    require(
        "low citation coverage" in audit and "errors.append" in audit,
        "audit_citations.py must make an explicit min-citations floor blocking when requested",
    )


def validate_review_skill(root: Path) -> None:
    rev = root / "skills/academic-review"
    manifest = read(rev / "manifest.yaml")
    closing = read(rev / "static/closing-gates.md")
    paper_review = read(rev / "references/sections/paper-review.md")
    reviewer_risk = read(rev / "references/checks/reviewer-risk.md")
    submission = read(rev / "references/checks/submission-readiness.md")
    journal_submission = read(rev / "references/checks/journal-submission-elements.md")
    data_code = read(rev / "references/checks/data-code-availability.md")
    high_impact = read(rev / "references/checks/high-impact-journal-review.md")
    audit = read(rev / "scripts/audit_draft.py")
    compile_check = read(rev / "scripts/check_compile_env.py")

    # Compile-environment detection: the agent must detect, not guess, and warn on failure
    require(
        "check_compile_env.py" in closing
        and "Compile unavailable" in closing
        and "tell the user explicitly" in closing,
        "closing-gates must run check_compile_env.py and warn the user when compilation is unavailable",
    )
    for token in ("def detect_tools", "def evaluate", "can_compile", "latexmk"):
        require(token in compile_check, f"check_compile_env.py must define {token}")

    # Automatic post-draft review
    require(
        "## Draft Completion Review Gate" in closing
        and "Do not wait for the user to ask for review" in closing
        and "reviewed-and-revised draft" in closing,
        "closing-gates must run review automatically after draft completion",
    )
    require(
        "triggered automatically by the Full Draft Workflow" in paper_review,
        "paper-review.md must say the Full Draft workflow triggers it automatically",
    )
    # Page budget gate
    require(
        "--max-content-pages" in closing
        and "--min-content-pages" in closing
        and "--max-content-pages" in submission,
        "page-limited venues must require compiled content-page auditing",
    )
    require(
        "numeric content-page limit" in closing
        and "compiled content-page count" in paper_review
        and "moving Limitations to an appendix" in submission,
        "review and submission gates must block page-limit overflow and define Limitations movement",
    )
    require(
        "primary core section below its confirmed floor" in paper_review
        and "Method must explain the algorithm" in paper_review
        and "evidence hook for each load-bearing module" in paper_review,
        "paper-review must own primary-core floor enforcement and method-paper underdevelopment findings",
    )
    require(
        "Bounded Review Intake" in paper_review
        and "complete `paper/` draft" in paper_review
        and "must not produce a `PASS` submission-readiness verdict" in paper_review,
        "paper-review must define bounded review behavior when a complete paper/ draft is unavailable",
    )
    require(
        "references/checks/data-code-availability.md" in manifest
        and "references/checks/high-impact-journal-review.md" in manifest
        and "Data/Code Availability" in journal_submission
        and "data-code-availability.md" in journal_submission,
        "academic-review must route journal data/code availability and high-impact journal review references",
    )
    require(
        "Inventory every supporting dataset" in data_code
        and "Do not invent DOIs, accession numbers, repository URLs, or embargo terms" in data_code
        and "Access route" in data_code
        and "Availability Ledger" in data_code
        and "OPEN_DECISION" in data_code,
        "data-code-availability reference must define an inventory-led availability workflow",
    )
    require(
        "originality" in high_impact
        and "scientific importance" in high_impact
        and "interdisciplinary readership" in high_impact
        and "readability for nonspecialists" in high_impact
        and "Do not claim editor fit as settled" in high_impact
        and "Nature-family" in high_impact,
        "high-impact journal review must define broad-interest reviewer axes and fit limits",
    )
    require(
        "data-code-availability.md" in submission
        and "high-impact-journal-review.md" in reviewer_risk,
        "submission-readiness and reviewer-risk must point to the new journal-specific checks",
    )
    require(
        "Finding Evidence Schema" in paper_review
        and "Location" in paper_review
        and "Evidence basis" in paper_review
        and "Assessment boundary" in paper_review
        and "Action type" in paper_review,
        "paper-review findings must carry evidence, boundary, and action fields",
    )
    require(
        "paper/closing-gate-log.md" in closing
        and "audit command" in closing
        and "verdict" in closing,
        "closing-gates must require a compact durable gate receipt for full paper closing runs",
    )
    require(
        "Risk Action Mapping" in reviewer_risk
        and all(
            token in reviewer_risk
            for token in (
                "PROSE_REVISION",
                "CLAIM_WEAKENING",
                "CITATION_VERIFICATION",
                "ADDITIONAL_ANALYSIS",
                "NEW_EXPERIMENT",
                "OPEN_DECISION",
                "BLOCKED",
            )
        ),
        "reviewer-risk must map risks to concrete writing/evidence action types",
    )
    require(
        "undefined references or citations" in submission and "BLOCKED" in submission,
        "submission-readiness must block undefined references and citations",
    )
    # audit_draft.py mechanical checks
    for token in (
        "check_invalid_latex_environments",
        "check_unresolved_pdf_refs",
        "UNRESOLVED_RENDERED_REF_RE",
        "check_hardcoded_structural_refs",
        "HARDCODED_STRUCTURAL_REF_RE",
        "check_framework_alignment",
        "parse_framework_display_items",
        "check_appendix_plan",
        "check_content_page_bounds_from_pages",
        "min_content_pages",
        "content-page budget underfilled",
        "DISPLAY_REF_RE",
        "COMPACT_SINGLE_COLUMN_WIDTH_MAX",
        "LIMITATIONS_MAX_WORDS = 180",
        "TAXONOMY_LABEL_RE",
        "BODY_TAXONOMY_RUNIN_RE",
        "LONG_HEADER_CHARS",
    ):
        require(token in audit, f"audit_draft.py must define {token}")


def main(argv: list[str]) -> int:
    root = Path(argv[1] if len(argv) > 1 else ".").resolve()

    validate_root_router(root)
    validate_packaging_boundary(root)
    validate_shared_layer(root)
    validate_no_stale_deleted_paths(root)

    skills_dir = root / "skills"
    require(skills_dir.is_dir(), "skills/ directory missing")
    skill_dirs = [d for d in skills_dir.iterdir() if (d / "SKILL.md").exists()]
    require(
        {d.name for d in skill_dirs}
        >= {"academic-writing", "academic-figure", "academic-citation", "academic-review"},
        "collection must contain the hub plus figure, citation, and review skills",
    )
    for skill_dir in skill_dirs:
        validate_standard_skill_frontmatter(skill_dir / "SKILL.md", expected_name=skill_dir.name)
        validate_skill_manifest_paths(skill_dir)
        validate_evals(skill_dir)

    validate_hub(root)
    validate_figure_skill(root)
    validate_citation_skill(root)
    validate_review_skill(root)

    print(f"academic-writing collection validation passed: {root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
