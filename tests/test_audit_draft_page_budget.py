#!/usr/bin/env python3
"""Tests for page-budget checks in scripts/audit_draft.py."""

from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "audit_draft", ROOT / "skills/academic-review/scripts/audit_draft.py"
)
assert SPEC is not None and SPEC.loader is not None
audit_draft = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(audit_draft)


class PageBudgetTests(unittest.TestCase):
    def test_references_page_counts_as_content_when_main_text_reaches_it(self) -> None:
        pages = [
            "Title\nAbstract\nIntroduction",
            "Experiments and Empirical Findings",
            "Conclusion text reaches this page.\nReferences\nSmith et al. 2024",
            "Appendix\nFull tables",
        ]

        self.assertEqual(audit_draft.content_pages_before_references(pages), 3)

    def test_missing_references_heading_uses_total_pdf_pages(self) -> None:
        pages = ["Title\nAbstract", "Main body", "Conclusion"]

        self.assertEqual(audit_draft.content_pages_before_references(pages), 3)

    def test_dedicated_limitations_section_excluded_from_budget(self) -> None:
        # A Limitations heading at the top of the next page is post-matter and should not make the
        # body appear to have reached that page.
        pages = [
            "Title\nAbstract\nIntroduction",
            "Experiments",
            "Conclusion",
            "Limitations",
            "References\nSmith et al. 2024",
        ]

        self.assertEqual(audit_draft.content_pages_before_references(pages), 3)

    def test_postmatter_mid_page_counts_the_page_reached_by_body(self) -> None:
        pages = [
            "Title\nAbstract\nIntroduction",
            "Experiments",
            "Conclusion paragraph with final body text.\nLimitations\nScope details",
            "References\nSmith et al. 2024",
        ]

        self.assertEqual(audit_draft.content_pages_before_references(pages), 3)

    def test_inline_limitations_runin_does_not_truncate_count(self) -> None:
        # An inline "Limitations of current evaluation." run-in inside a body section renders as part
        # of a paragraph line, so it must NOT be treated as a post-matter heading.
        pages = [
            "Title\nAbstract",
            "Experiments\nLimitations of current evaluation. We acknowledge that ...",
            "Conclusion\nReferences",
        ]

        self.assertEqual(audit_draft.content_pages_before_references(pages), 3)

    def test_min_content_pages_blocks_underfilled_page_limited_draft(self) -> None:
        pages = [
            "Title\nAbstract\nIntroduction",
            "Benchmark",
            "Experiments",
            "Conclusion\nReferences",
            "Appendix",
        ]
        errors: list[str] = []
        warnings: list[str] = []

        audit_draft.check_content_page_bounds_from_pages(
            pages,
            max_content_pages=9,
            min_content_pages=9,
            errors=errors,
            warnings=warnings,
        )

        self.assertTrue(any("content-page budget underfilled" in e for e in errors), errors)

    def test_exact_content_page_target_passes_when_main_text_reaches_limit_page(self) -> None:
        pages = [
            "Title\nAbstract\nIntroduction",
            "Related Work",
            "Benchmark",
            "Benchmark continued",
            "Experiments",
            "Experiments continued",
            "Analysis",
            "Discussion",
            "Conclusion\nReferences",
            "Appendix",
        ]
        errors: list[str] = []
        warnings: list[str] = []

        audit_draft.check_content_page_bounds_from_pages(
            pages,
            max_content_pages=9,
            min_content_pages=9,
            errors=errors,
            warnings=warnings,
        )

        self.assertEqual(errors, [])
        self.assertTrue(any("content-page budget ok: main text reaches page 9/9" in w for w in warnings), warnings)


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

    def test_taxonomy_definition_list_in_body_is_error(self) -> None:
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            path = base / "sections" / "benchmark-design.tex"
            path.parent.mkdir()
            path.write_text(
                "\\section{Benchmark Design}\n"
                "\\begin{itemize}\n"
                "\\item \\textbf{V1 -- Email}: malicious instructions in email bodies.\n"
                "\\item \\textbf{V2 -- SMS}: injected content in SMS messages.\n"
                "\\item \\textbf{V3 -- Web}: instructions embedded in web pages.\n"
                "\\item \\textbf{V4 -- Social}: injected posts on social platforms.\n"
                "\\item \\textbf{V5 -- Chat}: malicious content in work chat.\n"
                "\\end{itemize}\n",
                encoding="utf-8",
            )
            errors: list[str] = []

            audit_draft.check_enumeration(path, base, errors)

        self.assertTrue(any("taxonomy/inventory definition list" in e for e in errors), errors)

    def test_checklist_tex_is_not_body_taxonomy_prose(self) -> None:
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            path = base / "checklist.tex"
            path.write_text(
                "\\begin{enumerate}\n"
                "\\item {\\bf Claims}\n"
                "\\item[] Question: Do claims reflect scope?\n"
                "\\item[] Answer: \\answerTODO{}\n"
                "\\item[] Justification: \\justificationTODO{}\n"
                "\\item[] Guidelines:\n"
                "\\begin{itemize}\n"
                "\\item The abstract should clearly state the claims.\n"
                "\\item The claims should match results.\n"
                "\\item Aspirational goals must be marked as motivation.\n"
                "\\end{itemize}\n"
                "\\item {\\bf Limitations}\n"
                "\\item[] Question: Does the paper discuss limitations?\n"
                "\\item[] Answer: \\answerTODO{}\n"
                "\\item[] Justification: \\justificationTODO{}\n"
                "\\item[] Guidelines:\n"
                "\\begin{itemize}\n"
                "\\item The authors should create a Limitations section.\n"
                "\\item The paper should discuss scope.\n"
                "\\item The paper should discuss efficiency.\n"
                "\\end{itemize}\n"
                "\\end{enumerate}\n",
                encoding="utf-8",
            )
            errors: list[str] = []

            audit_draft.check_enumeration(path, base, errors)

        self.assertEqual(errors, [])

    def test_framework_planned_teaser_must_materialize(self) -> None:
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            framework = root / "writing-policies" / "paper-framework.md"
            framework.parent.mkdir()
            framework.write_text(
                "## 4. Figure Plan\n\n"
                "| ID | Type | Layout | Section | Message | Source | Generation route |\n"
                "|---|---|---|---|---|---|---|\n"
                "| Fig. 1 | teaser / pipeline | double-column | Introduction | Shows the attack chain. | Policy | AI illustration (picture-generation.md) |\n"
                "| Fig. 2 | heatmap | single-column | Benchmark | Shows coverage. | Data | Python matplotlib heatmap |\n",
                encoding="utf-8",
            )
            paper = root / "paper"
            (paper / "figures").mkdir(parents=True)
            (paper / "sections").mkdir()
            (paper / "main.tex").write_text(
                "\\input{sections/introduction}\n"
                "\\input{sections/benchmark}\n",
                encoding="utf-8",
            )
            (paper / "sections" / "introduction.tex").write_text(
                "\\section{Introduction}\nNo teaser here.\n",
                encoding="utf-8",
            )
            (paper / "sections" / "benchmark.tex").write_text(
                "\\section{Benchmark}\n"
                "\\begin{figure}[t]\n"
                "\\centering\n"
                "\\includegraphics[width=\\linewidth]{figures/vh_heatmap.pdf}\n"
                "\\caption{Coverage.}\n"
                "\\label{fig:vh_heatmap}\n"
                "\\end{figure}\n",
                encoding="utf-8",
            )
            (paper / "figures" / "latex_includes.tex").write_text(
                "% Fig. 1 (teaser): not yet generated -- see paper/figures/prompts/fig1_teaser.md\n"
                "% Fig. 2 (vh_heatmap): embedded in sections/benchmark.tex\n",
                encoding="utf-8",
            )

            errors, _warnings = audit_draft.audit(paper, framework_path=framework)

        self.assertTrue(any("planned figure missing" in e for e in errors), errors)
        self.assertTrue(any("not yet generated" in e for e in errors), errors)

    def test_framework_compact_heatmap_cannot_use_near_full_linewidth(self) -> None:
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            framework = root / "writing-policies" / "paper-framework.md"
            framework.parent.mkdir()
            framework.write_text(
                "## 4. Figure Plan\n\n"
                "| ID | Type | Layout | Section | Message | Source | Generation route |\n"
                "|---|---|---|---|---|---|---|\n"
                "| Fig. 1 | heatmap | single-column | Benchmark | Shows compact coverage. | Data | Python matplotlib heatmap |\n",
                encoding="utf-8",
            )
            paper = root / "paper"
            (paper / "figures").mkdir(parents=True)
            (paper / "sections").mkdir()
            (paper / "main.tex").write_text("\\input{sections/benchmark}\n", encoding="utf-8")
            (paper / "sections" / "benchmark.tex").write_text(
                "\\section{Benchmark}\n"
                "\\begin{figure}[t]\n"
                "\\centering\n"
                "\\includegraphics[width=0.85\\linewidth]{figures/vh_heatmap.pdf}\n"
                "\\caption{Coverage.}\n"
                "\\label{fig:vh_heatmap}\n"
                "\\end{figure}\n",
                encoding="utf-8",
            )

            errors, _warnings = audit_draft.audit(paper, framework_path=framework)

        self.assertTrue(any("oversized compact single-column figure" in e for e in errors), errors)

    def test_framework_compact_heatmap_is_not_confused_with_later_large_result_figure(self) -> None:
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            framework = root / "writing-policies" / "paper-framework.md"
            framework.parent.mkdir()
            framework.write_text(
                "## 4. Figure Plan\n\n"
                "| ID | Type | Layout | Section | Message | Source | Generation route |\n"
                "|---|---|---|---|---|---|---|\n"
                "| Fig. 1 | teaser / pipeline | double-column | Introduction | Shows the attack chain. | Policy | AI illustration |\n"
                "| Fig. 2 | heatmap | single-column | Benchmark | Shows compact coverage. | Data | Python matplotlib heatmap |\n"
                "| Fig. 3 | grouped bar chart | double-column | Experiments | Shows main results. | Data | Python matplotlib grouped bar chart |\n",
                encoding="utf-8",
            )
            paper = root / "paper"
            (paper / "figures" / "prompts").mkdir(parents=True)
            (paper / "sections").mkdir()
            (paper / "main.tex").write_text(
                "\\input{sections/introduction}\n"
                "\\input{sections/benchmark}\n"
                "\\input{sections/experiments}\n",
                encoding="utf-8",
            )
            (paper / "sections" / "introduction.tex").write_text(
                "\\section{Introduction}\n"
                "\\begin{figure}[t]\\includegraphics[width=\\textwidth]{figures/fig1_teaser.png}\\end{figure}\n",
                encoding="utf-8",
            )
            (paper / "sections" / "benchmark.tex").write_text(
                "\\section{Benchmark}\n"
                "\\begin{figure}[t]\n"
                "\\includegraphics[width=0.64\\linewidth]{figures/vh_heatmap.pdf}\n"
                "\\caption{Coverage heatmap.}\n"
                "\\label{fig:vh_heatmap}\n"
                "\\end{figure}\n",
                encoding="utf-8",
            )
            (paper / "sections" / "experiments.tex").write_text(
                "\\section{Experiments}\n"
                "\\begin{figure}[t]\n"
                "\\includegraphics[width=0.95\\textwidth]{figures/main_results.pdf}\n"
                "\\caption{Main results.}\n"
                "\\label{fig:main_results}\n"
                "\\end{figure}\n",
                encoding="utf-8",
            )
            (paper / "figures" / "prompts" / "fig1_teaser.md").write_text("brief", encoding="utf-8")
            (paper / "figures" / "fig1_teaser.png").write_bytes(b"fake")

            errors, _warnings = audit_draft.audit(paper, framework_path=framework)

        self.assertFalse(any("oversized compact single-column figure" in e for e in errors), errors)

    def test_framework_main_results_table_must_fill_textwidth(self) -> None:
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            framework = root / "writing-policies" / "paper-framework.md"
            framework.parent.mkdir()
            framework.write_text(
                "## 4. Figure Plan\n\n"
                "| ID | Type | Layout | Section | Message | Source | Generation route |\n"
                "|---|---|---|---|---|---|---|\n"
                "| Tab. 1 | main results table | double-column | Experiments | Shows headline metrics. | Data | LaTeX table |\n",
                encoding="utf-8",
            )
            paper = root / "paper"
            (paper / "sections").mkdir(parents=True)
            (paper / "main.tex").write_text("\\input{sections/experiments}\n", encoding="utf-8")
            (paper / "sections" / "experiments.tex").write_text(
                "\\section{Experiments}\n"
                "\\begin{table}[t]\n"
                "\\centering\n"
                "\\caption{Main results.}\n"
                "\\label{tab:main_results}\n"
                "\\begin{tabular}{l r r r r r}\n"
                "\\toprule\n"
                "Model & ASR & TCR & Exec & Def & RF \\\\\n"
                "\\bottomrule\n"
                "\\end{tabular}\n"
                "\\end{table}\n",
                encoding="utf-8",
            )

            errors, _warnings = audit_draft.audit(paper, framework_path=framework)

        self.assertTrue(any("planned full-width table" in e for e in errors), errors)

    def test_framework_compact_table_must_not_be_planned_double_column(self) -> None:
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            framework = root / "writing-policies" / "paper-framework.md"
            framework.parent.mkdir()
            framework.write_text(
                "## 4. Figure Plan\n\n"
                "| ID | Type | Layout | Section | Message | Source | Generation route |\n"
                "|---|---|---|---|---|---|---|\n"
                "| Tab. 1 | compact ablation table | double-column | Experiments | Shows a small 3-row ablation. | Data | LaTeX table |\n",
                encoding="utf-8",
            )
            paper = root / "paper"
            (paper / "sections").mkdir(parents=True)
            (paper / "main.tex").write_text("\\input{sections/experiments}\n", encoding="utf-8")
            (paper / "sections" / "experiments.tex").write_text(
                "\\section{Experiments}\n"
                "\\begin{table}[t]\n"
                "\\centering\n"
                "\\caption{Compact ablation.}\n"
                "\\label{tab:ablation}\n"
                "\\begin{tabular}{l r r}\n"
                "\\toprule\n"
                "Setting & ASR & TCR \\\\\n"
                "\\bottomrule\n"
                "\\end{tabular}\n"
                "\\end{table}\n",
                encoding="utf-8",
            )

            errors, _warnings = audit_draft.audit(paper, framework_path=framework)

        self.assertTrue(any("unjustified double-column table plan" in e for e in errors), errors)

    def test_framework_story_teaser_defaults_single_column(self) -> None:
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            framework = root / "writing-policies" / "paper-framework.md"
            framework.parent.mkdir()
            framework.write_text(
                "## 4. Figure Plan\n\n"
                "| ID | Type | Layout | Section | Message | Source | Generation route |\n"
                "|---|---|---|---|---|---|---|\n"
                "| Fig. 1 | story teaser / overview | double-column | Introduction | Introduces the paper story. | Policy | AI illustration |\n",
                encoding="utf-8",
            )
            paper = root / "paper"
            (paper / "figures" / "prompts").mkdir(parents=True)
            (paper / "sections").mkdir()
            (paper / "main.tex").write_text("\\input{sections/introduction}\n", encoding="utf-8")
            (paper / "sections" / "introduction.tex").write_text(
                "\\section{Introduction}\n"
                "\\begin{figure*}[t]\n"
                "\\includegraphics[width=\\textwidth]{figures/fig1_teaser.png}\n"
                "\\caption{Story overview.}\n"
                "\\label{fig:teaser}\n"
                "\\end{figure*}\n",
                encoding="utf-8",
            )
            (paper / "figures" / "prompts" / "fig1_teaser.md").write_text("brief", encoding="utf-8")
            (paper / "figures" / "fig1_teaser.png").write_bytes(b"fake")

            errors, _warnings = audit_draft.audit(paper, framework_path=framework)

        self.assertTrue(any("story/teaser figure should default to single-column" in e for e in errors), errors)

    def test_framework_double_column_figure_must_use_wide_figure_environment(self) -> None:
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            framework = root / "writing-policies" / "paper-framework.md"
            framework.parent.mkdir()
            framework.write_text(
                "## 4. Figure Plan\n\n"
                "| ID | Type | Layout | Section | Message | Source | Generation route |\n"
                "|---|---|---|---|---|---|---|\n"
                "| Fig. 1 | pipeline / framework diagram | double-column | Benchmark | Shows the benchmark construction pipeline. | Policy | AI illustration |\n",
                encoding="utf-8",
            )
            paper = root / "paper"
            (paper / "figures" / "prompts").mkdir(parents=True)
            (paper / "sections").mkdir()
            (paper / "main.tex").write_text("\\input{sections/benchmark}\n", encoding="utf-8")
            (paper / "sections" / "benchmark.tex").write_text(
                "\\section{Benchmark}\n"
                "\\begin{figure}[t]\n"
                "\\includegraphics[width=\\linewidth]{figures/fig1_pipeline.png}\n"
                "\\caption{Pipeline.}\n"
                "\\label{fig:pipeline}\n"
                "\\end{figure}\n",
                encoding="utf-8",
            )
            (paper / "figures" / "prompts" / "fig1_pipeline.md").write_text("brief", encoding="utf-8")
            (paper / "figures" / "fig1_pipeline.png").write_bytes(b"fake")

            errors, _warnings = audit_draft.audit(paper, framework_path=framework)

        self.assertTrue(any("planned double-column figure" in e for e in errors), errors)

    def test_framework_cannot_reference_unplanned_display_item(self) -> None:
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            framework = root / "writing-policies" / "paper-framework.md"
            framework.parent.mkdir()
            framework.write_text(
                "## 4. Figure Plan\n\n"
                "| ID | Type | Layout | Section | Message | Source | Generation route |\n"
                "|---|---|---|---|---|---|---|\n"
                "| Fig. 1 | teaser | single-column | Introduction | Shows the story. | Policy | existing image |\n"
                "| Tab. 1 | taxonomy table | single-column | Benchmark | Defines categories. | Manifest | LaTeX table |\n\n"
                "## 9. Open Decisions\n\n"
                "| Decision | Status | Default | Affects |\n"
                "|---|---|---|---|\n"
                "| Breakdown data | Needs verification | Use current data | Fig. 2, Fig. 4, Tab. 3 |\n",
                encoding="utf-8",
            )
            paper = root / "paper"
            (paper / "figures" / "prompts").mkdir(parents=True)
            (paper / "figures" / "fig1_teaser.png").write_bytes(b"fake")
            (paper / "figures" / "prompts" / "fig1_teaser.md").write_text("brief", encoding="utf-8")
            (paper / "sections").mkdir()
            (paper / "main.tex").write_text(
                "\\input{sections/introduction}\n\\input{sections/benchmark}\n",
                encoding="utf-8",
            )
            (paper / "sections" / "introduction.tex").write_text(
                "\\section{Introduction}\n"
                "\\begin{figure}[t]\n"
                "\\includegraphics[width=.6\\linewidth]{figures/fig1_teaser.png}\n"
                "\\caption{Story.}\n"
                "\\label{fig:teaser}\n"
                "\\end{figure}\n",
                encoding="utf-8",
            )
            (paper / "sections" / "benchmark.tex").write_text(
                "\\section{Benchmark}\n"
                "\\begin{table}[t]\n"
                "\\caption{Taxonomy.}\n"
                "\\label{tab:taxonomy}\n"
                "\\begin{tabular}{lr}\\toprule ID & Count \\\\\\bottomrule\\end{tabular}\n"
                "\\end{table}\n",
                encoding="utf-8",
            )

            errors, _warnings = audit_draft.audit(paper, framework_path=framework)

        self.assertTrue(any("unplanned display reference" in e for e in errors), errors)

    def test_framework_main_results_scorecard_should_not_be_single_column_in_two_column_plan(self) -> None:
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            framework = root / "writing-policies" / "paper-framework.md"
            framework.parent.mkdir()
            framework.write_text(
                "## 4. Figure Plan\n\n"
                "| ID | Type | Layout | Section | Message | Source | Generation route |\n"
                "|---|---|---|---|---|---|---|\n"
                "| Tab. 2 | Main results scorecard | single-column | Experiments | Per-model defend, compromise, and unresolved rates for eight evaluated agents. | Results | LaTeX table |\n",
                encoding="utf-8",
            )
            paper = root / "paper"
            (paper / "sections").mkdir(parents=True)
            (paper / "main.tex").write_text("\\input{sections/experiments}\n", encoding="utf-8")
            (paper / "sections" / "experiments.tex").write_text(
                "\\section{Experiments}\n"
                "\\begin{table}[t]\n"
                "\\caption{Overall results.}\n"
                "\\label{tab:main_results}\n"
                "\\begin{tabular}{lrrr}\\toprule Model & DR & CR & Other \\\\\\bottomrule\\end{tabular}\n"
                "\\end{table}\n",
                encoding="utf-8",
            )

            errors, _warnings = audit_draft.audit(paper, framework_path=framework)

        self.assertTrue(any("load-bearing main-results table" in e for e in errors), errors)

    def test_appendix_requires_plan_when_content_exists(self) -> None:
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            paper = Path(tmp)
            (paper / "sections").mkdir()
            (paper / "main.tex").write_text(
                "\\documentclass{article}\n"
                "\\begin{document}\n"
                "\\input{sections/appendix}\n"
                "\\appendix\n"
                "\\input{sections/appendix}\n"
                "\\end{document}\n",
                encoding="utf-8",
            )
            (paper / "sections" / "appendix.tex").write_text(
                "\\section{Extra Results}\n"
                "This appendix reports complete evidence for the main claim.\n",
                encoding="utf-8",
            )
            errors: list[str] = []

            audit_draft.check_appendix_plan(paper, errors)

        self.assertTrue(any("missing appendix plan" in e for e in errors), errors)

    def test_appendix_plan_must_record_source_status_and_fallback(self) -> None:
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            paper = Path(tmp)
            (paper / "sections").mkdir()
            (paper / "main.tex").write_text(
                "\\documentclass{article}\n"
                "\\begin{document}\n"
                "\\appendix\n"
                "\\input{sections/appendix}\n"
                "\\end{document}\n",
                encoding="utf-8",
            )
            (paper / "sections" / "appendix.tex").write_text(
                "\\section{Extra Results}\n"
                "This appendix reports complete evidence for the main claim.\n",
                encoding="utf-8",
            )
            (paper / "appendix-plan.md").write_text(
                "| Item | Claim backed |\n"
                "|---|---|\n"
                "| A | Main claim |\n",
                encoding="utf-8",
            )
            errors: list[str] = []

            audit_draft.check_appendix_plan(paper, errors)

        self.assertTrue(any("incomplete appendix plan" in e for e in errors), errors)

    def test_table_star_must_fill_textwidth(self) -> None:
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            path = base / "sections" / "experiments.tex"
            path.parent.mkdir()
            path.write_text(
                "\\section{Experiments}\n"
                "\\begin{table*}[t]\n"
                "\\centering\n"
                "\\caption{Main results.}\n"
                "\\label{tab:main_results}\n"
                "\\begin{tabular}{l r r}\n"
                "\\toprule\n"
                "Model & ASR & TCR \\\\\n"
                "\\bottomrule\n"
                "\\end{tabular}\n"
                "\\end{table*}\n",
                encoding="utf-8",
            )
            errors: list[str] = []

            audit_draft.check_tables(path, base, errors, [])

        self.assertTrue(any("narrow double-column table" in e for e in errors), errors)


if __name__ == "__main__":
    unittest.main()
