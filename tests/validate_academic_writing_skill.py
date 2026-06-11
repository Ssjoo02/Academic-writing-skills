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
    router = read(root / "SKILL.md")
    require("name: academic-writing" in router, "root SKILL.md must declare name: academic-writing")
    for sib in (
        "skills/academic-writing/SKILL.md",
        "skills/academic-figure/SKILL.md",
        "skills/academic-citation/SKILL.md",
        "skills/academic-review/SKILL.md",
    ):
        require(sib in router, f"root SKILL.md must route to {sib}")


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
    section_drafting = read(hub / "static/workflow/stages/section-drafting.md")
    latex_project = read(hub / "static/workflow/stages/latex-project.md")
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
    require(
        "manifest-mapped paper type profile path" in " ".join(writing_policy.split()),
        "Writing Policy stage must use the manifest-mapped paper type profile path",
    )
    require(
        "Do NOT raise page/length budgets, per-section length" in writing_policy,
        "Writing Policy stage must defer page/length/budget decisions to Paper Framework",
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
        "Do not compress a primary-core section below its floor" in paper_framework
        and "return to the Paper Framework checkpoint" in paper_framework,
        "Paper Framework stage must block compressing core sections below the confirmed floor",
    )

    # Abstract / introduction logic chain (now in section-drafting stage)
    require(
        "problem -> challenge/gap -> insight/contribution -> advantage -> evidence" in section_drafting
        and "state purpose or advantage" in section_drafting,
        "Section drafting must gate Abstract/Introduction on a coherent logic chain",
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
        expected = "journal" if venue in {"jmlr", "tpami", "ieee-tpami", "journal"} else "conference"
        require(f"## Venue Kind\n\n- {expected}" in text, f"{rel} must declare Venue Kind {expected}")

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
    figure_handling = read(fig / "static/figure-handling.md")
    table_handling = read(fig / "static/table-handling.md")
    figures_tables = read(fig / "references/sections/figures-and-tables.md")
    table_design = read(fig / "references/tables/table-design.md")
    figure_planning = read(fig / "references/figures/figure-planning.md")
    conf_sizing = read(fig / "references/figures/conference/figure-sizing.md")

    require(
        "Column-Span Decision" in figure_planning
        and "pipeline / framework / architecture" in figure_planning
        and "teaser / first concept figure" in figure_planning
        and "one multi-panel `figure*` with a shared legend" in figure_planning,
        "figure-planning must define the column-span decision (teaser single, pipeline/multi-panel span)",
    )
    require(
        "Column-Span Quick Rule" in conf_sizing,
        "conference figure-sizing must carry the column-span quick rule",
    )
    require(
        "Long headers overflow narrow columns" in table_handling,
        "table-handling must flag long-header overflow at small column counts",
    )

    require(
        "Framework-to-artifact alignment is a hard gate" in figure_handling
        and "paper/framework-execution-report.md" in figure_handling
        and "0.60--0.70\\linewidth" in figure_handling
        and ">0.70\\linewidth" in figure_handling,
        "figure-handling must enforce Paper Framework Figure Plan alignment and compact widths",
    )
    require(
        "Never let a table overflow" in table_handling
        and "hard defect" in table_handling
        and "Generate width-safe table source on the first pass" in table_handling
        and "Never hard-code structural numbers in source" in table_handling,
        "table-handling must make overflow a hard defect and forbid hard-coded structural numbers",
    )
    require(
        "Never let a table overflow" in figures_tables and "appendix" in figures_tables.lower(),
        "figures-and-tables guide must make body and appendix overflow a hard defect",
    )
    require(
        "Span Decision" in table_design
        and "Table kind" in table_design
        and "Span justification" in table_design,
        "table-design must define the span decision contract",
    )


def validate_citation_skill(root: Path) -> None:
    cit = root / "skills/academic-citation"
    workflow = read(cit / "static/citation-workflow.md")
    integrity = read(cit / "references/checks/citation-integrity.md")
    audit = read(cit / "scripts/audit_citations.py")

    require(
        "Complete author lists required" in workflow
        and "Stable identifier required" in workflow
        and "audit_citations.py" in workflow,
        "citation-workflow must state author-list, identifier, and audit rules",
    )
    require(len(integrity) > 0, "citation-integrity reference must exist")
    require("min-citations" in audit or "min_citations" in audit, "audit_citations.py must exist and run")


def validate_review_skill(root: Path) -> None:
    rev = root / "skills/academic-review"
    closing = read(rev / "static/closing-gates.md")
    paper_review = read(rev / "references/sections/paper-review.md")
    submission = read(rev / "references/checks/submission-readiness.md")
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
        "--max-content-pages" in closing and "--max-content-pages" in submission,
        "page-limited venues must require compiled content-page auditing",
    )
    require(
        "numeric content-page limit" in closing
        and "compiled content-page count" in paper_review
        and "moving Limitations to an appendix" in submission,
        "review and submission gates must block page-limit overflow and define Limitations movement",
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
    validate_shared_layer(root)

    skills_dir = root / "skills"
    require(skills_dir.is_dir(), "skills/ directory missing")
    skill_dirs = [d for d in skills_dir.iterdir() if (d / "SKILL.md").exists()]
    require(
        {d.name for d in skill_dirs}
        >= {"academic-writing", "academic-figure", "academic-citation", "academic-review"},
        "collection must contain the hub plus figure, citation, and review skills",
    )
    for skill_dir in skill_dirs:
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
