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


class CompileIntegrityTests(unittest.TestCase):
    def test_undefined_references_in_log_are_errors(self) -> None:
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            paper = Path(tmp)
            (paper / "main.log").write_text(
                "LaTeX Warning: Reference `tab:missing' on page 3 undefined on input line 42.\n"
                "LaTeX Warning: There were undefined references.\n",
                encoding="utf-8",
            )
            errors: list[str] = []
            warnings: list[str] = []

            audit_draft.check_log(paper, errors, warnings)

        self.assertTrue(any("undefined references" in e for e in errors), errors)

    def test_unresolved_question_mark_refs_in_pdf_text_are_errors(self) -> None:
        errors: list[str] = []

        audit_draft.check_unresolved_pdf_refs(
            ["Table ?? provides details.", "Figure 2 is fine.", "Section ?? is not fine."],
            errors,
        )

        self.assertTrue(any("unresolved rendered reference" in e for e in errors), errors)

    def test_invalid_end_section_environment_is_error(self) -> None:
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            path = base / "sections" / "experiments.tex"
            path.parent.mkdir()
            path.write_text("\\section{Experiments}\nText.\n\\end{section}\n", encoding="utf-8")
            errors: list[str] = []

            audit_draft.check_invalid_latex_environments([path], base, errors)

        self.assertTrue(any("invalid LaTeX section environment" in e for e in errors), errors)

    def test_hardcoded_structural_reference_is_error(self) -> None:
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            path = base / "sections" / "appendix.tex"
            path.parent.mkdir()
            path.write_text("This supplements the analysis in Section~5.4.\n", encoding="utf-8")
            errors: list[str] = []

            audit_draft.check_hardcoded_structural_refs([path], base, errors)

        self.assertTrue(any("hard-coded structural reference" in e for e in errors), errors)

    def test_wide_single_column_table_is_error(self) -> None:
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            path = base / "sections" / "appendix.tex"
            path.parent.mkdir()
            path.write_text(
                "\\begin{table}[t]\n"
                "\\begin{tabular}{l r r r r r}\n"
                "App & A & B & C & D & E \\\\\n"
                "\\end{tabular}\n"
                "\\end{table}\n",
                encoding="utf-8",
            )
            errors: list[str] = []
            warnings: list[str] = []

            audit_draft.check_wide_tables(path, base, errors, warnings)

        self.assertTrue(any("wide table" in e for e in errors), errors)

    def test_prose_in_non_wrapping_table_column_is_error(self) -> None:
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            path = base / "sections" / "appendix.tex"
            path.parent.mkdir()
            path.write_text(
                "\\begin{tabular}{l l}\n"
                "ID & This cell contains several prose words \\\\\n"
                "\\end{tabular}\n",
                encoding="utf-8",
            )
            errors: list[str] = []

            audit_draft.check_prose_in_narrow_column(path, base, errors)

        self.assertTrue(any("prose in a non-wrapping column" in e for e in errors), errors)


if __name__ == "__main__":
    unittest.main()
