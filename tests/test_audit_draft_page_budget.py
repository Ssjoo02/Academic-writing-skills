#!/usr/bin/env python3
"""Tests for page-budget checks in scripts/audit_draft.py."""

from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("audit_draft", ROOT / "scripts/audit_draft.py")
assert SPEC is not None and SPEC.loader is not None
audit_draft = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(audit_draft)


class PageBudgetTests(unittest.TestCase):
    def test_references_page_counts_as_content_when_main_text_reaches_it(self) -> None:
        pages = [
            "Title\nAbstract\nIntroduction",
            "Experiments and Empirical Findings",
            "Limitations\nReferences\nSmith et al. 2024",
            "Appendix\nFull tables",
        ]

        self.assertEqual(audit_draft.content_pages_before_references(pages), 3)

    def test_missing_references_heading_uses_total_pdf_pages(self) -> None:
        pages = ["Title\nAbstract", "Main body", "Conclusion"]

        self.assertEqual(audit_draft.content_pages_before_references(pages), 3)

    def test_dedicated_limitations_section_excluded_from_budget(self) -> None:
        # Limitations heading on its own line ends the content count before References.
        pages = [
            "Title\nAbstract\nIntroduction",
            "Experiments",
            "Conclusion",
            "Limitations",
            "References\nSmith et al. 2024",
        ]

        self.assertEqual(audit_draft.content_pages_before_references(pages), 4)

    def test_inline_limitations_runin_does_not_truncate_count(self) -> None:
        # An inline "Limitations of current evaluation." run-in inside a body section renders as part
        # of a paragraph line, so it must NOT be treated as a post-matter heading.
        pages = [
            "Title\nAbstract",
            "Experiments\nLimitations of current evaluation. We acknowledge that ...",
            "Conclusion\nReferences",
        ]

        self.assertEqual(audit_draft.content_pages_before_references(pages), 3)


class LimitationsPlacementTests(unittest.TestCase):
    def _run(self, tmp_files: dict[str, str]) -> list[str]:
        import tempfile

        errors: list[str] = []
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            paths = []
            for name, content in tmp_files.items():
                p = base / name
                p.parent.mkdir(parents=True, exist_ok=True)
                p.write_text(content, encoding="utf-8")
                paths.append(p)
            audit_draft.check_limitations_placement(paths, base, errors)
        return errors

    def test_runin_limitations_inside_body_is_flagged(self) -> None:
        errors = self._run(
            {"sections/experiments.tex": "Results are strong.\n\\textbf{Limitations of current evaluation.} We note ..."}
        )
        self.assertTrue(any("misplaced Limitations unit" in e for e in errors), errors)

    def test_dedicated_section_is_clean(self) -> None:
        errors = self._run({"sections/limitations.tex": "\\section{Limitations}\nWe discuss three ..."})
        self.assertEqual(errors, [])

    def test_duplicate_dedicated_sections_flagged(self) -> None:
        errors = self._run(
            {
                "sections/limitations.tex": "\\section{Limitations}\nFirst home.",
                "sections/extra.tex": "\\section*{Limitations}\nSecond home.",
            }
        )
        self.assertTrue(any("more than one dedicated Limitations section" in e for e in errors), errors)


if __name__ == "__main__":
    unittest.main()
