#!/usr/bin/env python3
"""Static citation audit for academic-writing drafts.

This does not prove that a source supports a claim. It catches local bibliography
integrity failures before a draft is described as citation-clean.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


CITE_RE = re.compile(r"\\cite\w*\s*(?:\[[^\]]*\]\s*){0,2}\{([^}]*)\}")
ENTRY_RE = re.compile(r"@(\w+)\s*\{\s*([^,\s]+)\s*,", re.I)
FIELD_RE = re.compile(r"(?m)^\s*([A-Za-z][A-Za-z0-9_-]*)\s*=\s*[{'\"]")
MARKER_RE = re.compile(r"%\s*(CITATION_NEEDED|EVIDENCE_NEEDED)\b")
PLACEHOLDER_AUTHOR_RE = re.compile(r"\band\s+others\b|\bet\s+al\.?\b", re.I)
ARXIV_RE = re.compile(r"\b\d{4}\.\d{4,5}(?:v\d+)?\b|[a-z-]+/\d{7}(?:v\d+)?", re.I)


def strip_comments(text: str) -> str:
    lines = []
    for line in text.splitlines():
        escaped = False
        cut = len(line)
        for i, char in enumerate(line):
            if char == "\\":
                escaped = not escaped
                continue
            if char == "%" and not escaped:
                cut = i
                break
            escaped = False
        lines.append(line[:cut])
    return "\n".join(lines)


def find_matching_brace(text: str, open_index: int) -> int:
    depth = 0
    for i in range(open_index, len(text)):
        if text[i] == "{":
            depth += 1
        elif text[i] == "}":
            depth -= 1
            if depth == 0:
                return i
    return -1


def parse_bib_entries(path: Path) -> dict[str, dict[str, str]]:
    text = path.read_text(encoding="utf-8", errors="ignore")
    entries: dict[str, dict[str, str]] = {}
    for match in ENTRY_RE.finditer(text):
        entry_type = match.group(1).lower()
        key = match.group(2).strip()
        open_index = text.find("{", match.start())
        close_index = find_matching_brace(text, open_index)
        if close_index < 0:
            entries[key] = {"entry_type": entry_type, "_parse_error": "unclosed entry"}
            continue
        body = text[match.end() : close_index]
        fields = {"entry_type": entry_type}
        field_matches = list(FIELD_RE.finditer(body))
        for i, field_match in enumerate(field_matches):
            name = field_match.group(1).lower()
            value_start = field_match.end()
            opener = body[value_start - 1]
            if opener == "{":
                value_end = find_matching_brace(body, value_start - 1)
                if value_end < 0:
                    fields[name] = body[value_start:].strip()
                else:
                    fields[name] = " ".join(body[value_start:value_end].split())
            else:
                next_comma = body.find(",", value_start)
                if next_comma < 0:
                    next_comma = len(body)
                fields[name] = body[value_start:next_comma].strip().strip("'\"")
        entries[key] = fields
    return entries


def extract_cites(tex_files: list[Path]) -> tuple[list[str], list[tuple[Path, int, str]]]:
    keys: list[str] = []
    markers: list[tuple[Path, int, str]] = []
    for path in tex_files:
        raw = path.read_text(encoding="utf-8", errors="ignore")
        for lineno, line in enumerate(raw.splitlines(), 1):
            if MARKER_RE.search(line):
                markers.append((path, lineno, line.strip()))
        text = strip_comments(raw)
        for match in CITE_RE.finditer(text):
            for key in match.group(1).split(","):
                key = key.strip()
                if key:
                    keys.append(key)
    return keys, markers


def has_stable_identifier(fields: dict[str, str]) -> bool:
    if fields.get("doi") or fields.get("url") or fields.get("eprint"):
        return True
    joined = " ".join(fields.values())
    return bool(ARXIV_RE.search(joined) or "doi.org/" in joined.lower())


def year_value(fields: dict[str, str]) -> int | None:
    match = re.search(r"\d{4}", fields.get("year", ""))
    return int(match.group(0)) if match else None


def audit(paper_dir: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    bib_path = paper_dir / "references.bib"
    if not bib_path.exists():
        errors.append(f"missing bibliography file: {bib_path}")
        return errors, warnings

    tex_files = sorted(paper_dir.rglob("*.tex"))
    if not tex_files:
        errors.append(f"no .tex files found under {paper_dir}")
        return errors, warnings

    used_keys, markers = extract_cites(tex_files)
    entries = parse_bib_entries(bib_path)
    used = set(used_keys)
    bib_keys = set(entries)

    for path, lineno, line in markers:
        errors.append(f"unresolved citation marker: {path}:{lineno}: {line}")

    for key in sorted(used - bib_keys):
        errors.append(f"citation key missing from references.bib: {key}")

    for key in sorted(bib_keys - used):
        errors.append(f"uncited bibliography entry: {key}")

    for key in sorted(used & bib_keys):
        fields = entries[key]
        if fields.get("_parse_error"):
            errors.append(f"malformed BibTeX entry: {key}: {fields['_parse_error']}")
            continue
        for required in ("title", "author", "year"):
            if not fields.get(required):
                errors.append(f"missing required BibTeX field: {key}: {required}")

        author = fields.get("author", "")
        if PLACEHOLDER_AUTHOR_RE.search(author):
            errors.append(f"placeholder author in BibTeX: {key}: use full verified author list, no `and others`")

        year = year_value(fields)
        if year and year >= 2000 and not has_stable_identifier(fields):
            errors.append(f"modern entry lacks DOI/URL/arXiv: {key}")
        elif not has_stable_identifier(fields):
            warnings.append(f"entry lacks DOI/URL/arXiv: {key}")

        venue = " ".join(
            fields.get(name, "") for name in ("journal", "booktitle", "institution", "publisher")
        ).lower()
        if ("technical report" in venue or "arxiv preprint" in venue) and not has_stable_identifier(fields):
            errors.append(f"vague source label without stable identifier: {key}")

    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit citation and BibTeX integrity for a LaTeX paper.")
    parser.add_argument("paper_dir", nargs="?", default="paper", help="Paper directory containing references.bib")
    args = parser.parse_args()

    paper_dir = Path(args.paper_dir).resolve()
    errors, warnings = audit(paper_dir)

    print(f"Citation audit: {paper_dir}")
    if warnings:
        print("\nWarnings:")
        for item in warnings:
            print(f"- WARN: {item}")
    if errors:
        print("\nErrors:")
        for item in errors:
            print(f"- ERROR: {item}")
        print(f"\nFAIL: {len(errors)} error(s), {len(warnings)} warning(s)")
        return 1
    print(f"PASS: 0 error(s), {len(warnings)} warning(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
