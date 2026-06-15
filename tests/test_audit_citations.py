#!/usr/bin/env python3
"""Tests for citation and rendered bibliography integrity."""

from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "audit_citations", ROOT / "skills/academic-citation/scripts/audit_citations.py"
)
assert SPEC is not None and SPEC.loader is not None
audit_citations = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(audit_citations)


class RenderedBibliographyTests(unittest.TestCase):
    def _audit(self, *, bbl: str) -> list[str]:
        with tempfile.TemporaryDirectory() as tmp:
            paper = Path(tmp)
            (paper / "main.tex").write_text(
                "\\documentclass{article}\n"
                "\\begin{document}\n"
                "Prior work matters~\\cite{chen2024indirect}.\n"
                "\\bibliography{references}\n"
                "\\end{document}\n",
                encoding="utf-8",
            )
            (paper / "references.bib").write_text(
                "@misc{chen2024indirect,\n"
                "  title = {Indirect Prompt Injection in Retrieval-Augmented Generation},\n"
                "  author = {Chen, Sizhe and Piet, Julien and Sitawarin, Chawin and Wagner, David},\n"
                "  year = {2024},\n"
                "  eprint = {2406.07057},\n"
                "  archivePrefix = {arXiv},\n"
                "  url = {https://arxiv.org/abs/2406.07057}\n"
                "}\n",
                encoding="utf-8",
            )
            (paper / "main.bbl").write_text(bbl, encoding="utf-8")

            errors, _warnings = audit_citations.audit(paper)
            return errors

    def test_rendered_bibliography_placeholder_author_is_error(self) -> None:
        errors = self._audit(
            bbl=(
                "\\begin{thebibliography}{1}\n"
                "\\bibitem[{Chen et~al.(2024)}]{chen2024indirect}\n"
                "Sizhe Chen and 1 others. 2024.\n"
                "\\newblock Indirect prompt injection in retrieval-augmented generation.\n"
                "\\newblock \\href{https://arxiv.org/abs/2406.07057}{Preprint}, arXiv:2406.07057.\n"
                "\\end{thebibliography}\n"
            )
        )

        self.assertTrue(
            any("rendered bibliography placeholder author" in error for error in errors),
            errors,
        )

    def test_modern_rendered_bibliography_without_visible_identifier_is_error(self) -> None:
        errors = self._audit(
            bbl=(
                "\\begin{thebibliography}{1}\n"
                "\\bibitem[{Chen et~al.(2024)}]{chen2024indirect}\n"
                "Sizhe Chen, Julien Piet, Chawin Sitawarin, and David Wagner. 2024.\n"
                "\\newblock Indirect prompt injection in retrieval-augmented generation.\n"
                "\\end{thebibliography}\n"
            )
        )

        self.assertTrue(
            any("rendered bibliography lacks visible DOI/URL/arXiv" in error for error in errors),
            errors,
        )

    def test_min_citation_floor_is_error(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            paper = Path(tmp)
            (paper / "main.tex").write_text(
                "\\documentclass{article}\n"
                "\\begin{document}\n"
                "Prior work matters~\\cite{chen2024indirect}.\n"
                "\\bibliography{references}\n"
                "\\end{document}\n",
                encoding="utf-8",
            )
            (paper / "references.bib").write_text(
                "@misc{chen2024indirect,\n"
                "  title = {Indirect Prompt Injection in Retrieval-Augmented Generation},\n"
                "  author = {Chen, Sizhe and Piet, Julien and Sitawarin, Chawin and Wagner, David},\n"
                "  year = {2024},\n"
                "  eprint = {2406.07057},\n"
                "  archivePrefix = {arXiv},\n"
                "  url = {https://arxiv.org/abs/2406.07057}\n"
                "}\n",
                encoding="utf-8",
            )

            errors, warnings = audit_citations.audit(paper, min_citations=2)

        self.assertEqual(warnings, [])
        self.assertTrue(any("low citation coverage" in error for error in errors), errors)


if __name__ == "__main__":
    unittest.main()
