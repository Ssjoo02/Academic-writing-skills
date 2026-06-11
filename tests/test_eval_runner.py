#!/usr/bin/env python3
"""Offline unit tests for the eval runner (no network calls)."""
from __future__ import annotations

import contextlib
import importlib.util
import io
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
_SPEC = importlib.util.spec_from_file_location("run_evals", ROOT / "tests" / "run_evals.py")
run_evals = importlib.util.module_from_spec(_SPEC)
assert _SPEC and _SPEC.loader
# Register before exec so dataclasses can resolve the module's namespace.
sys.modules["run_evals"] = run_evals
_SPEC.loader.exec_module(run_evals)


class DiscoveryTests(unittest.TestCase):
    def test_discovers_all_four_skills(self) -> None:
        cases = run_evals.discover_evals(ROOT)
        skills = {c.skill_name for c in cases}
        self.assertEqual(
            skills,
            {"academic-writing", "academic-figure", "academic-citation", "academic-review"},
        )

    def test_every_case_has_id_prompt_and_assertions(self) -> None:
        cases = run_evals.discover_evals(ROOT)
        self.assertGreaterEqual(len(cases), 15)
        for c in cases:
            self.assertTrue(c.id, "eval id must be non-empty")
            self.assertTrue(c.prompt, f"{c.skill_name}/{c.id}: prompt must be non-empty")
            self.assertTrue(c.assertions, f"{c.skill_name}/{c.id}: must declare assertions")
            for a in c.assertions:
                self.assertIn("name", a)
                self.assertIn("description", a)


class ContextTests(unittest.TestCase):
    def test_context_includes_router_and_skill(self) -> None:
        skill_dir = ROOT / "skills" / "academic-figure"
        ctx = run_evals.build_skill_context(ROOT, skill_dir)
        self.assertIn("ENTRY ROUTER", ctx)
        self.assertIn("Academic Figure", ctx)
        # academic-figure always_load resolves _shared/core/stance.md
        self.assertIn("stance", ctx.lower())

    def test_always_load_resolution_for_hub(self) -> None:
        hub = ROOT / "skills" / "academic-writing"
        paths = run_evals._always_load_paths(hub)
        names = {p.name for p in paths}
        self.assertEqual(names, {"stance.md", "gates.md", "contract.md"})


class PromptBuilderTests(unittest.TestCase):
    def test_agent_messages_shape(self) -> None:
        case = run_evals.EvalCase(
            skill_name="academic-figure",
            skill_dir=ROOT / "skills" / "academic-figure",
            id="x",
            prompt="make a plot",
            expected_output="renders and inspects",
            assertions=[{"name": "a", "description": "d"}],
        )
        msgs = run_evals.build_agent_messages(case, "CTX")
        self.assertEqual([m["role"] for m in msgs], ["system", "user"])
        self.assertIn("CTX", msgs[0]["content"])
        self.assertEqual(msgs[1]["content"], "make a plot")

    def test_judge_messages_contain_assertion(self) -> None:
        case = run_evals.EvalCase(
            skill_name="s", skill_dir=ROOT, id="x", prompt="p", expected_output="e",
            assertions=[],
        )
        msgs = run_evals.build_judge_messages(case, "the response", {"name": "n", "description": "the rule"})
        joined = " ".join(m["content"] for m in msgs)
        self.assertIn("the rule", joined)
        self.assertIn("the response", joined)


class JudgeParsingTests(unittest.TestCase):
    def test_parses_clean_json(self) -> None:
        out = run_evals.parse_judge_json('{"pass": true, "reason": "ok"}')
        self.assertTrue(out["pass"])
        self.assertEqual(out["reason"], "ok")

    def test_parses_json_with_surrounding_text(self) -> None:
        out = run_evals.parse_judge_json('Sure!\n{"pass": false, "reason": "violates gate"}\nDone.')
        self.assertFalse(out["pass"])
        self.assertEqual(out["reason"], "violates gate")

    def test_raises_without_json(self) -> None:
        with self.assertRaises(ValueError):
            run_evals.parse_judge_json("no json here")


class EndpointTests(unittest.TestCase):
    def test_endpoint_normalization(self) -> None:
        self.assertEqual(run_evals._chat_endpoint("https://api.openai.com"), "https://api.openai.com/v1/chat/completions")
        self.assertEqual(run_evals._chat_endpoint("https://relay.example.com/v1"), "https://relay.example.com/v1/chat/completions")
        self.assertEqual(
            run_evals._chat_endpoint("https://relay.example.com/v1/chat/completions"),
            "https://relay.example.com/v1/chat/completions",
        )


class DryRunTests(unittest.TestCase):
    @staticmethod
    def _run(args: list[str]) -> int:
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            return run_evals.main(args)

    def test_dry_run_returns_zero_without_network(self) -> None:
        self.assertEqual(self._run(["--root", str(ROOT), "--dry-run"]), 0)

    def test_filter_to_one_skill(self) -> None:
        self.assertEqual(self._run(["--root", str(ROOT), "--skill", "academic-citation", "--dry-run"]), 0)

    def test_unknown_filter_returns_two(self) -> None:
        self.assertEqual(self._run(["--root", str(ROOT), "--eval", "does-not-exist", "--dry-run"]), 2)


if __name__ == "__main__":
    unittest.main()
