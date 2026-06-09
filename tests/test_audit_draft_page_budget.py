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


if __name__ == "__main__":
    unittest.main()
