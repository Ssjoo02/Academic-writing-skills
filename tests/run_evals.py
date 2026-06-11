#!/usr/bin/env python3
"""Behavioral eval runner for the academic-writing collection.

Each skill ships ``evals/evals.json`` describing prompts, an expected_output,
and judgeable ``assertions``. This runner:

1. Discovers every ``skills/*/evals/evals.json`` in the collection.
2. Rebuilds each skill's real routing context (the root ``SKILL.md``, the skill's
   own ``SKILL.md`` + ``manifest.yaml``, and the manifest's ``always_load`` files)
   so the model under test sees the same rules a host environment would load.
3. Sends each eval prompt to an OpenAI-compatible chat API (the "agent").
4. Judges every assertion with an LLM judge that must answer strict JSON.
5. Writes a JSON report and prints a console summary; exit code is non-zero if
   any assertion fails or any eval errors.

It is dependency-free (standard library only) and talks to any OpenAI-compatible
``/v1/chat/completions`` endpoint, reusing the same env vars the collection's
image config documents (``OPENAI_API_KEY`` / ``OPENAI_BASE_URL``).

Usage
-----
    # Offline: discover, validate, and print the plan without any API calls.
    python3 tests/run_evals.py --dry-run

    # Run everything against a model (judge defaults to the same model).
    export OPENAI_API_KEY=sk-...
    python3 tests/run_evals.py --model gpt-4o --out eval-report.json

    # Filter to one skill / one eval id.
    python3 tests/run_evals.py --skill academic-figure --dry-run
    python3 tests/run_evals.py --eval full-draft-stops-at-policy-gate --model gpt-4o

Environment variables
---------------------
    OPENAI_API_KEY    API key (required unless --dry-run or --api-key given).
    OPENAI_BASE_URL   Base URL, default https://api.openai.com
    OPENAI_MODEL      Default model when --model is omitted.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

# Per-file and total caps so a large always_load file cannot blow the context.
PER_FILE_CHARS = 20_000
TOTAL_CONTEXT_CHARS = 120_000
DEFAULT_BASE_URL = "https://api.openai.com"


# --------------------------------------------------------------------------- #
# Discovery
# --------------------------------------------------------------------------- #

@dataclass
class EvalCase:
    skill_name: str
    skill_dir: Path
    id: str
    prompt: str
    expected_output: str
    assertions: list[dict[str, str]] = field(default_factory=list)


def discover_evals(root: Path) -> list[EvalCase]:
    """Find and parse every skills/*/evals/evals.json under the collection root."""
    cases: list[EvalCase] = []
    skills_dir = root / "skills"
    if not skills_dir.is_dir():
        raise SystemExit(f"skills/ directory not found under {root}")
    for skill_dir in sorted(p for p in skills_dir.iterdir() if (p / "SKILL.md").exists()):
        evals_path = skill_dir / "evals/evals.json"
        if not evals_path.exists():
            continue
        data = json.loads(evals_path.read_text(encoding="utf-8"))
        skill_name = data.get("skill_name", skill_dir.name)
        for item in data.get("evals", []):
            cases.append(
                EvalCase(
                    skill_name=skill_name,
                    skill_dir=skill_dir,
                    id=str(item.get("id")),
                    prompt=item.get("prompt", ""),
                    expected_output=item.get("expected_output", ""),
                    assertions=list(item.get("assertions", [])),
                )
            )
    return cases


# --------------------------------------------------------------------------- #
# Context reconstruction
# --------------------------------------------------------------------------- #

def _read_capped(path: Path, cap: int = PER_FILE_CHARS) -> str:
    text = path.read_text(encoding="utf-8")
    if len(text) > cap:
        text = text[:cap] + f"\n... [truncated, {len(text) - cap} more chars] ...\n"
    return text


def _always_load_paths(skill_dir: Path) -> list[Path]:
    """Resolve the manifest's always_load entries relative to the skill dir."""
    manifest_path = skill_dir / "manifest.yaml"
    if not manifest_path.exists():
        return []
    # Tiny YAML-free extraction: read the always_load block without importing PyYAML
    # so the runner stays dependency-free even where PyYAML is absent.
    out: list[Path] = []
    in_block = False
    for line in manifest_path.read_text(encoding="utf-8").splitlines():
        if line.startswith("always_load:"):
            in_block = True
            continue
        if in_block:
            stripped = line.strip()
            if stripped.startswith("- "):
                rel = stripped[2:].strip()
                resolved = (skill_dir / rel).resolve()
                if resolved.exists():
                    out.append(resolved)
            elif stripped and not stripped.startswith("#"):
                break
    return out


def build_skill_context(root: Path, skill_dir: Path) -> str:
    """Assemble the routing context a host would load before this skill runs."""
    parts: list[str] = []

    def add(label: str, path: Path) -> None:
        if path.exists():
            parts.append(f"===== {label}: {path.relative_to(root)} =====\n{_read_capped(path)}")

    add("ENTRY ROUTER (read first)", root / "SKILL.md")
    add("SKILL", skill_dir / "SKILL.md")
    add("MANIFEST", skill_dir / "manifest.yaml")
    for p in _always_load_paths(skill_dir):
        add("ALWAYS-LOAD", p)

    context = "\n\n".join(parts)
    if len(context) > TOTAL_CONTEXT_CHARS:
        context = context[:TOTAL_CONTEXT_CHARS] + "\n... [context truncated] ...\n"
    return context


# --------------------------------------------------------------------------- #
# Prompt builders (pure functions, unit-testable)
# --------------------------------------------------------------------------- #

AGENT_SYSTEM_PREFIX = (
    "You are an AI agent that has loaded the academic-writing skill collection. "
    "The rules below are the collection's entry router, the relevant skill's SKILL.md and "
    "manifest, and its always-load core files. Behave exactly as these rules dictate: route "
    "correctly, honor the confirmation gates and STOP-never-guess rule, stay in writing-only "
    "scope, delegate to sibling skills instead of improvising, and mirror the user's interaction "
    "language. If a rule says to stop and ask, stop and ask rather than completing the task.\n\n"
    "Respond as you would to the real user. Do not narrate that you are being evaluated."
)


def build_agent_messages(case: EvalCase, context: str) -> list[dict[str, str]]:
    return [
        {"role": "system", "content": f"{AGENT_SYSTEM_PREFIX}\n\n# Loaded skill rules\n\n{context}"},
        {"role": "user", "content": case.prompt},
    ]


def build_judge_messages(case: EvalCase, response: str, assertion: dict[str, str]) -> list[dict[str, str]]:
    system = (
        "You are a strict evaluator for an AI skill. Given the user prompt, the expected behavior, "
        "the assistant's response, and a single assertion, decide whether the response satisfies the "
        "assertion. Be conservative: if the response violates the assertion or is ambiguous about it, "
        'fail it. Respond with ONLY a JSON object: {"pass": true|false, "reason": "<one sentence>"}.'
    )
    user = (
        f"User prompt:\n{case.prompt}\n\n"
        f"Expected behavior:\n{case.expected_output}\n\n"
        f"Assertion to check ({assertion.get('name', 'assertion')}):\n{assertion.get('description', '')}\n\n"
        f"Assistant response:\n{response}\n\n"
        'Return only the JSON object {"pass": ..., "reason": ...}.'
    )
    return [{"role": "system", "content": system}, {"role": "user", "content": user}]


# --------------------------------------------------------------------------- #
# OpenAI-compatible chat call (stdlib only)
# --------------------------------------------------------------------------- #

def _chat_endpoint(base_url: str) -> str:
    base = base_url.rstrip("/")
    if base.endswith("/chat/completions"):
        return base
    if base.endswith("/v1"):
        return base + "/chat/completions"
    return base + "/v1/chat/completions"


def call_chat(
    messages: list[dict[str, str]],
    *,
    model: str,
    api_key: str,
    base_url: str,
    temperature: float = 0.0,
    max_tokens: int = 1024,
    timeout: int = 120,
    retries: int = 2,
) -> str:
    payload = json.dumps(
        {"model": model, "messages": messages, "temperature": temperature, "max_tokens": max_tokens}
    ).encode("utf-8")
    url = _chat_endpoint(base_url)
    last_err: Exception | None = None
    for attempt in range(retries + 1):
        req = urllib.request.Request(
            url,
            data=payload,
            headers={"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                body = json.loads(resp.read().decode("utf-8"))
            return body["choices"][0]["message"]["content"]
        except (urllib.error.URLError, urllib.error.HTTPError, KeyError, json.JSONDecodeError) as exc:
            last_err = exc
            if attempt < retries:
                time.sleep(2 * (attempt + 1))
    raise RuntimeError(f"chat call failed after {retries + 1} attempts: {last_err}")


def parse_judge_json(text: str) -> dict[str, Any]:
    """Extract the first {...} JSON object from a judge response, leniently."""
    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end == -1 or end <= start:
        raise ValueError(f"no JSON object in judge response: {text!r}")
    obj = json.loads(text[start : end + 1])
    return {"pass": bool(obj.get("pass")), "reason": str(obj.get("reason", "")).strip()}


# --------------------------------------------------------------------------- #
# Runner
# --------------------------------------------------------------------------- #

def run_case(
    case: EvalCase,
    root: Path,
    *,
    model: str,
    judge_model: str,
    api_key: str,
    base_url: str,
    temperature: float,
    max_tokens: int,
) -> dict[str, Any]:
    context = build_skill_context(root, case.skill_dir)
    result: dict[str, Any] = {
        "skill": case.skill_name,
        "eval_id": case.id,
        "prompt": case.prompt,
        "response": None,
        "assertions": [],
        "error": None,
    }
    try:
        response = call_chat(
            build_agent_messages(case, context),
            model=model,
            api_key=api_key,
            base_url=base_url,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        result["response"] = response
        for assertion in case.assertions:
            verdict = call_chat(
                build_judge_messages(case, response, assertion),
                model=judge_model,
                api_key=api_key,
                base_url=base_url,
                temperature=0.0,
                max_tokens=256,
            )
            parsed = parse_judge_json(verdict)
            result["assertions"].append(
                {"name": assertion.get("name", "assertion"), "passed": parsed["pass"], "reason": parsed["reason"]}
            )
    except Exception as exc:  # noqa: BLE001 - report any failure per case, keep going
        result["error"] = str(exc)
    return result


def summarize(results: list[dict[str, Any]]) -> dict[str, int]:
    summary = {"evals": len(results), "assertions": 0, "passed": 0, "failed": 0, "errors": 0}
    for r in results:
        if r["error"]:
            summary["errors"] += 1
        for a in r["assertions"]:
            summary["assertions"] += 1
            summary["passed" if a["passed"] else "failed"] += 1
    return summary


def print_plan(cases: list[EvalCase], root: Path) -> None:
    by_skill: dict[str, int] = {}
    assertion_total = 0
    for c in cases:
        by_skill[c.skill_name] = by_skill.get(c.skill_name, 0) + 1
        assertion_total += len(c.assertions)
    print("Eval plan (dry run — no API calls):")
    for skill, n in sorted(by_skill.items()):
        print(f"  {skill:20s} {n} evals")
    print(f"  {'TOTAL':20s} {len(cases)} evals, {assertion_total} assertions")
    if cases:
        sample = cases[0]
        ctx = build_skill_context(root, sample.skill_dir)
        print(f"\nContext sample for '{sample.skill_name}/{sample.id}': {len(ctx)} chars assembled.")


def print_report(results: list[dict[str, Any]]) -> None:
    print("\nEval results:")
    for r in results:
        if r["error"]:
            print(f"  [ERROR] {r['skill']}/{r['eval_id']}: {r['error']}")
            continue
        for a in r["assertions"]:
            mark = "PASS" if a["passed"] else "FAIL"
            print(f"  [{mark}] {r['skill']}/{r['eval_id']} :: {a['name']} — {a['reason']}")
    s = summarize(results)
    print(
        f"\nSummary: {s['passed']}/{s['assertions']} assertions passed, "
        f"{s['failed']} failed, {s['errors']} eval errors across {s['evals']} evals."
    )


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Run behavioral evals for the academic-writing collection.")
    parser.add_argument("--root", default=".", help="Collection root (default: cwd).")
    parser.add_argument("--skill", help="Only run evals for this skill name.")
    parser.add_argument("--eval", dest="eval_id", help="Only run the eval with this id.")
    parser.add_argument("--model", default=os.environ.get("OPENAI_MODEL"), help="Agent model.")
    parser.add_argument("--judge-model", help="Judge model (default: same as --model).")
    parser.add_argument("--base-url", default=os.environ.get("OPENAI_BASE_URL", DEFAULT_BASE_URL))
    parser.add_argument("--api-key", default=os.environ.get("OPENAI_API_KEY"))
    parser.add_argument("--temperature", type=float, default=0.0)
    parser.add_argument("--max-tokens", type=int, default=1024)
    parser.add_argument("--out", help="Write a JSON report to this path.")
    parser.add_argument("--dry-run", action="store_true", help="Discover and plan only; no API calls.")
    args = parser.parse_args(argv)

    root = Path(args.root).resolve()
    cases = discover_evals(root)
    if args.skill:
        cases = [c for c in cases if c.skill_name == args.skill]
    if args.eval_id:
        cases = [c for c in cases if c.id == args.eval_id]
    if not cases:
        print("No matching evals found.", file=sys.stderr)
        return 2

    if args.dry_run:
        print_plan(cases, root)
        return 0

    if not args.model:
        print("error: --model (or OPENAI_MODEL) is required unless --dry-run.", file=sys.stderr)
        return 2
    if not args.api_key:
        print("error: --api-key (or OPENAI_API_KEY) is required unless --dry-run.", file=sys.stderr)
        return 2

    judge_model = args.judge_model or args.model
    results = [
        run_case(
            c,
            root,
            model=args.model,
            judge_model=judge_model,
            api_key=args.api_key,
            base_url=args.base_url,
            temperature=args.temperature,
            max_tokens=args.max_tokens,
        )
        for c in cases
    ]

    print_report(results)
    summary = summarize(results)
    if args.out:
        report = {
            "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
            "model": args.model,
            "judge_model": judge_model,
            "base_url": args.base_url,
            "summary": summary,
            "results": results,
        }
        Path(args.out).write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"\nReport written to {args.out}")

    return 0 if summary["failed"] == 0 and summary["errors"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
