#!/usr/bin/env python3
"""Offline unit tests for check_compile_env.py (no real binaries required)."""
from __future__ import annotations

import contextlib
import importlib.util
import io
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
_SCRIPT = ROOT / "skills" / "academic-review" / "scripts" / "check_compile_env.py"
_SPEC = importlib.util.spec_from_file_location("check_compile_env", _SCRIPT)
cce = importlib.util.module_from_spec(_SPEC)
assert _SPEC and _SPEC.loader
sys.modules["check_compile_env"] = cce
_SPEC.loader.exec_module(cce)


def fake_which(available: set[str]):
    """Build a shutil.which replacement that only resolves the named tools."""
    return lambda name: f"/usr/bin/{name}" if name in available else None


class DetectTests(unittest.TestCase):
    def test_detect_reports_every_known_tool(self) -> None:
        tools = cce.detect_tools(which=fake_which({"latexmk"}))
        self.assertEqual(set(tools), set(cce.ALL_TOOLS))
        self.assertTrue(tools["latexmk"])
        self.assertIsNone(tools["pdflatex"])


class EvaluateTests(unittest.TestCase):
    def test_full_toolchain_can_compile_and_read_pdf(self) -> None:
        tools = cce.detect_tools(which=fake_which({"latexmk", "biber", "pdfinfo", "pdftotext"}))
        result = cce.evaluate(tools)
        self.assertTrue(result["can_compile"])
        self.assertEqual(result["compiler"], "latexmk")
        self.assertTrue(result["can_read_pdf"])
        self.assertTrue(result["has_bib_tool"])
        self.assertEqual(result["recommended_command"], "latexmk -pdf main.tex")

    def test_no_engine_cannot_compile(self) -> None:
        result = cce.evaluate(cce.detect_tools(which=fake_which(set())))
        self.assertFalse(result["can_compile"])
        self.assertIsNone(result["compiler"])
        self.assertIsNone(result["recommended_command"])
        self.assertIn("UNAVAILABLE", result["message"])

    def test_prefers_latexmk_over_pdflatex(self) -> None:
        result = cce.evaluate(cce.detect_tools(which=fake_which({"pdflatex", "latexmk"})))
        self.assertEqual(result["compiler"], "latexmk")

    def test_plain_engine_uses_two_pass_command(self) -> None:
        result = cce.evaluate(cce.detect_tools(which=fake_which({"pdflatex"})))
        self.assertEqual(result["compiler"], "pdflatex")
        self.assertIn("&&", result["recommended_command"])

    def test_compile_without_pdf_reader_warns_about_page_counting(self) -> None:
        result = cce.evaluate(cce.detect_tools(which=fake_which({"pdflatex"})))
        self.assertTrue(result["can_compile"])
        self.assertFalse(result["can_read_pdf"])
        self.assertIn("page count", result["message"].lower())


class MainExitCodeTests(unittest.TestCase):
    def _run_main(self, argv: list[str], available: set[str]) -> tuple[int, str]:
        original = cce.shutil.which
        cce.shutil.which = fake_which(available)
        buf = io.StringIO()
        try:
            with contextlib.redirect_stdout(buf):
                code = cce.main(argv)
        finally:
            cce.shutil.which = original
        return code, buf.getvalue()

    def test_exit_zero_when_compile_available(self) -> None:
        code, out = self._run_main([], {"latexmk", "pdfinfo"})
        self.assertEqual(code, 0)
        self.assertIn("can_compile : True", out)

    def test_exit_one_when_no_engine(self) -> None:
        code, out = self._run_main([], set())
        self.assertEqual(code, 1)
        self.assertIn("UNAVAILABLE", out)

    def test_json_output_is_parseable(self) -> None:
        code, out = self._run_main(["--json"], {"latexmk", "pdfinfo", "pdftotext"})
        self.assertEqual(code, 0)
        data = json.loads(out)
        self.assertTrue(data["can_compile"])
        self.assertEqual(data["compiler"], "latexmk")


if __name__ == "__main__":
    unittest.main()
