#!/usr/bin/env python3
"""Tests for the academic-figure table schema inspector."""

from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills/academic-figure/scripts/inspect_table_data.py"
SPEC = importlib.util.spec_from_file_location("inspect_table_data", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
inspect_table_data = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(inspect_table_data)


class InspectTableDataTests(unittest.TestCase):
    def test_markdown_scorecard_reports_width_and_direction_risks(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "main_result.md"
            path.write_text(
                "\n".join(
                    [
                        "| Method | AID | SIRI | WHU | UCM | Avg. | Latency ↓ |",
                        "|---|---:|---:|---:|---:|---:|---:|",
                        "| Base-VL | 71.20 | 68.40 | 82.50 | 76.30 | 74.60 | 1.20 |",
                        "| Ours | 83.60 | 78.50 | 91.20 | 86.70 | 84.10 | 1.05 |",
                    ]
                ),
                encoding="utf-8",
            )

            report = inspect_table_data.inspect_table(path)

        self.assertEqual(report["format"], "markdown")
        self.assertEqual(report["n_rows"], 2)
        self.assertEqual(report["n_columns"], 7)
        self.assertIn("main result table", report["suggested_table_kinds"])
        self.assertTrue(report["wide_table_risk"])
        self.assertIn("AID", report["metric_direction_unknown_columns"])
        self.assertIn("many_columns", report["width_risks"])
        self.assertEqual(report["precision_by_column"]["AID"], [2])

    def test_csv_training_configuration_is_not_treated_as_result_table(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "config.csv"
            path.write_text(
                "\n".join(
                    [
                        "Phase,Setting,Value",
                        "Data,Input resolution,1024 x 1024 crops",
                        "Optimization,Learning rate,2e-5 with cosine decay",
                        "Inference,Beam size,1",
                    ]
                ),
                encoding="utf-8",
            )

            report = inspect_table_data.inspect_table(path)

        self.assertEqual(report["format"], "csv")
        self.assertEqual(report["n_columns"], 3)
        self.assertIn("training configuration table", report["suggested_table_kinds"])
        self.assertFalse(report["wide_table_risk"])
        self.assertEqual(report["numeric_columns"], [])

    def test_grouped_method_scorecard_still_suggests_main_result(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "grouped_result.md"
            path.write_text(
                "\n".join(
                    [
                        "| Group | Method | AID | SIRI | WHU | UCM | Avg |",
                        "|---|---|---:|---:|---:|---:|---:|",
                        "| General | Base-VL | 71.2 | 68.4 | 82.5 | 76.3 | 74.6 |",
                        "| Ours | RsEvi-8B | 83.6 | 78.5 | 91.2 | 86.7 | 84.1 |",
                    ]
                ),
                encoding="utf-8",
            )

            report = inspect_table_data.inspect_table(path)

        self.assertIn("main result table", report["suggested_table_kinds"])

    def test_cli_outputs_json(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "split.md"
            path.write_text(
                "\n".join(
                    [
                        "| Dataset | Train | Dev | Test | Total |",
                        "|---|---:|---:|---:|---:|",
                        "| A | 100 | 10 | 10 | 120 |",
                    ]
                ),
                encoding="utf-8",
            )

            proc = subprocess.run(
                [sys.executable, str(SCRIPT), str(path)],
                check=True,
                text=True,
                stdout=subprocess.PIPE,
            )

        report = json.loads(proc.stdout)
        self.assertIn("data split table", report["suggested_table_kinds"])
        self.assertEqual(report["source"], str(path))


if __name__ == "__main__":
    unittest.main()
