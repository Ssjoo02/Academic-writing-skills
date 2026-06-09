#!/usr/bin/env python3
"""Validate the academic-writing skill contract.

This is a lightweight structural validator for routing and profile contracts.
It intentionally avoids checking external venue facts.
"""

from __future__ import annotations

import sys
from pathlib import Path

try:
    import yaml
except ImportError as exc:  # pragma: no cover - environment guard
    raise SystemExit(f"PyYAML is required for validation: {exc}") from exc


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def load_manifest(root: Path) -> dict:
    manifest_path = root / "manifest.yaml"
    require(manifest_path.exists(), "manifest.yaml is missing")
    return yaml.safe_load(manifest_path.read_text()) or {}


def validate_manifest_paths(root: Path, manifest: dict) -> None:
    for rel in manifest.get("always_load", []):
        require((root / rel).exists(), f"always_load path missing: {rel}")

    for axis_name, axis in manifest.get("axes", {}).items():
        for value, rel in axis.get("values", {}).items():
            require((root / rel).exists(), f"{axis_name}.{value} path missing: {rel}")

    for item in manifest.get("references", {}).get("on_demand", []):
        rel = item.get("path")
        if rel:
            require((root / rel).exists(), f"on_demand path missing: {rel}")


def validate_venue_kind_first_contract(root: Path, manifest: dict) -> None:
    skill = (root / "SKILL.md").read_text()
    manifest_text = (root / "manifest.yaml").read_text()
    manifest_flat = " ".join(manifest_text.split())
    full_draft = (root / "static/workflow/full-draft.md").read_text()
    contract = (root / "static/core/contract.md").read_text()
    submission_readiness = (root / "references/checks/submission-readiness.md").read_text()

    require(
        "venue_kind" in manifest_text,
        "manifest must define venue_kind as an explicit axis before paper_type",
    )
    venue_kind_pos = skill.find("`venue_kind`")
    venue_pos = skill.find("`venue`", venue_kind_pos + 1)
    paper_type_pos = skill.find("`paper_type`", venue_pos + 1)
    require(
        -1 not in {venue_kind_pos, venue_pos, paper_type_pos}
        and venue_kind_pos < venue_pos < paper_type_pos,
        "SKILL.md must route venue_kind before venue and paper_type",
    )
    require(
        "default: conference" in manifest_text,
        "venue_kind must default to conference",
    )
    require(
        "Select journal only when the user explicitly" in manifest_flat,
        "manifest must say journal is selected only from explicit user evidence",
    )
    require(
        "manifest-mapped paper type profile path" in full_draft,
        "Full Draft workflow must use the manifest-mapped paper type profile path",
    )
    require(
        "venue kind" in contract.lower() and "conference" in contract and "journal" in contract,
        "core contract must include venue kind as part of paper identity",
    )
    require(
        "--max-content-pages" in full_draft and "--max-content-pages" in submission_readiness,
        "page-limited venues must require compiled content-page auditing",
    )
    require(
        "Display-Item Page Budget" in full_draft
        and "display-item page cost" in full_draft
        and "compression margin" in full_draft,
        "Paper Framework must budget display items separately from prose pages",
    )


def validate_post_draft_review_contract(root: Path, manifest: dict) -> None:
    skill = (root / "SKILL.md").read_text()
    full_draft = (root / "static/workflow/full-draft.md").read_text()
    paper_review = (root / "references/sections/paper-review.md").read_text()
    on_demand = manifest.get("references", {}).get("on_demand", [])
    review_conditions = [
        item.get("condition", "")
        for item in on_demand
        if item.get("path") == "references/sections/paper-review.md"
    ]

    require(review_conditions, "manifest must include paper-review.md in on_demand references")
    require(
        any("automatic post-draft review" in condition for condition in review_conditions),
        "manifest must make paper-review an automatic post-draft review trigger",
    )
    require(
        "Post-draft review (automatic after Full Draft)" in skill,
        "SKILL.md must expose automatic post-draft review in the router reference list",
    )
    require(
        "### Draft Completion Review Gate" in full_draft
        and "Do not wait for the user to ask for review" in full_draft
        and "reviewed-and-revised draft" in full_draft,
        "Full Draft workflow must load and run review automatically after draft completion",
    )
    require(
        "triggered automatically by the Full Draft Workflow" in paper_review,
        "paper-review.md must say the Full Draft workflow triggers it automatically",
    )


def validate_final_quality_gates(root: Path) -> None:
    full_draft = (root / "static/workflow/full-draft.md").read_text()
    submission_readiness = (root / "references/checks/submission-readiness.md").read_text()
    figures_tables = (root / "references/sections/figures-and-tables.md").read_text()
    conclusion = (root / "references/sections/conclusion.md").read_text()
    audit_script = (root / "scripts/audit_draft.py").read_text()

    require(
        "Table ??" in full_draft and "undefined references" in full_draft,
        "Full Draft workflow must block unresolved rendered references such as Table ??",
    )
    require(
        "invalid LaTeX section environment" in audit_script
        and "check_invalid_latex_environments" in audit_script,
        "audit_draft.py must block invalid section environments such as \\end{section}",
    )
    require(
        "check_unresolved_pdf_refs" in audit_script
        and "UNRESOLVED_RENDERED_REF_RE" in audit_script,
        "audit_draft.py must scan the rendered PDF for Table ?? / Figure ?? references",
    )
    require(
        "undefined references present" in audit_script
        and "errors.append" in audit_script,
        "audit_draft.py must treat undefined references as errors",
    )
    require(
        "section is long" in audit_script
        and "errors.append" in audit_script
        and "120-180 words" in conclusion
        and "blocking" in conclusion.lower(),
        "over-long Limitations must be a blocking defect, not a warning-only style note",
    )
    require(
        "Never let a table overflow" in figures_tables
        and "hard defect" in figures_tables
        and "appendix" in figures_tables.lower(),
        "figure/table guide must make body and appendix overflow a hard defect",
    )
    require(
        "undefined references or citations" in submission_readiness
        and "BLOCKED" in submission_readiness,
        "submission-readiness must block undefined references and citations",
    )


def validate_paper_type_families(root: Path, manifest: dict) -> None:
    paper_type_values = manifest["axes"]["paper_type"]["values"]
    conference = [key for key in paper_type_values if not key.startswith("journal-")]
    journal = [key for key in paper_type_values if key.startswith("journal-")]

    require(conference, "conference paper type family is empty")
    require(journal, "journal paper type family is empty")

    for key in conference:
        rel = paper_type_values[key]
        require(
            not rel.startswith("references/paper-types/journal/"),
            f"conference paper type points to journal profile: {key} -> {rel}",
        )

    for key in journal:
        rel = paper_type_values[key]
        require(
            rel.startswith("references/paper-types/journal/"),
            f"journal paper type does not point to journal profile: {key} -> {rel}",
        )


def validate_venue_cards(root: Path, manifest: dict) -> None:
    venue_values = manifest["axes"]["venue"]["values"]
    for venue, rel in venue_values.items():
        if venue == "generic":
            continue
        path = root / rel
        text = path.read_text()
        require(f"## Venue Kind\n\n- " in text, f"{rel} must declare Venue Kind")

        expected = "journal" if venue in {"jmlr", "tpami", "ieee-tpami", "journal"} else "conference"
        require(
            f"## Venue Kind\n\n- {expected}" in text,
            f"{rel} must declare Venue Kind {expected}",
        )


def main(argv: list[str]) -> int:
    root = Path(argv[1] if len(argv) > 1 else ".").resolve()
    manifest = load_manifest(root)
    validate_manifest_paths(root, manifest)
    validate_venue_kind_first_contract(root, manifest)
    validate_post_draft_review_contract(root, manifest)
    validate_final_quality_gates(root)
    validate_paper_type_families(root, manifest)
    validate_venue_cards(root, manifest)
    print(f"academic-writing skill validation passed: {root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
