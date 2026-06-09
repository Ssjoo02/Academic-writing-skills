#!/usr/bin/env python3
"""Static draft-hygiene audit for academic-writing LaTeX drafts.

This checks the *mechanical* writing rules the skill already mandates so that
adherence does not depend on the agent remembering them. It does NOT judge
writing quality, claim support, or section-writing method (those need semantic
review). Run it before describing a draft as clean, alongside audit_citations.py.

Checks (errors block; warnings inform):
- no \\footnote{...} anywhere in prose
- no file/code artifacts in prose (\\texttt{...ext}, \\verb, \\path)
- no local filesystem paths in prose (/mnt/, /home/, /Users/, /root/, ~/)
- no leftover missing-support markers (% CITATION_NEEDED / EVIDENCE_NEEDED /
  FIGURE_NEEDED / TABLE_NEEDED)
- subsection budget: at most 4 \\subsection per main section
- table hygiene: no \\hline in tables (use booktabs); booktabs loaded when any
  table exists; warn on vertical rules and \\textsc{lowercase} names
- appendix starts on a fresh page (\\clearpage before \\appendix)
- salience: warn on taxonomy/inventory enumeration and per-category count dumps in body prose
  (full lists belong in a table or the appendix)
- wide tables: warn when a many-column plain tabular sits in a single-column float (body or
  appendix) and will overflow; suggest table*/rotate/split
- no duplicate \\label{...}
- \\input/\\include consistency between main.tex and section files
- compile-log signals when main.log exists (undefined refs/citations, multiply
  defined labels, overfull boxes)
"""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path


SUBSECTION_BUDGET = 4

FOOTNOTE_RE = re.compile(r"\\footnote\b")
ARTIFACT_RE = re.compile(
    r"\\(?:texttt|verb|path|lstinline)\b[^\n]*?"
    r"\.(?:json|py|csv|tsv|tex|sh|bash|yaml|yml|ipynb|cfg|ini|log|pkl|pt|ckpt|npy|md|txt)\b",
    re.I,
)
PATH_RE = re.compile(r"(?:/mnt/|/home/|/Users/|/root/|/tmp/|(?<![\w.])~/)")
MARKER_RE = re.compile(r"%\s*(CITATION_NEEDED|EVIDENCE_NEEDED|FIGURE_NEEDED|TABLE_NEEDED)\b")
SUBSECTION_RE = re.compile(r"\\subsection\b\s*\{")
SECTION_RE = re.compile(r"\\section\b\s*\{")
LABEL_RE = re.compile(r"\\label\s*\{([^}]*)\}")
INPUT_RE = re.compile(r"\\(?:input|include)\s*\{([^}]*)\}")
HLINE_RE = re.compile(r"\\hline\b")
TABULAR_BEGIN_RE = re.compile(r"\\begin\{(tabular\*?|tabularx)\}")
TEXTSC_LOWER_RE = re.compile(r"\\textsc\s*\{\s*[a-z]")
APPENDIX_RE = re.compile(r"\\appendix\b")
CLEARPAGE_RE = re.compile(r"\\(?:clearpage|newpage|cleardoublepage)\b")
BOOKTABS_RE = re.compile(r"\\usepackage(?:\[[^\]]*\])?\{[^}]*\bbooktabs\b[^}]*\}")
REFERENCE_HEADING_RE = re.compile(r"(?m)^\s*(References|Bibliography)\s*$")
LIST_ENV_RE = re.compile(r"\\begin\{(itemize|enumerate)\}(.*?)\\end\{\1\}", re.S)
ITEM_RE = re.compile(r"\\item\b")
COUNT_RE = re.compile(
    r"\b\d+\s+(?:tasks|samples|examples|instances|images|cases|items|tokens|queries|prompts)\b",
    re.I,
)
# a parenthetical quantity: "(27 tasks)", "(50%)", or a multi-digit "(142)" — but NOT a bare
# single-digit list marker like "(1)" / "(4)" used for enumerating contributions or steps.
PAREN_COUNT_RE = re.compile(
    r"\(\s*\d[\d,]*\s*(?:tasks|samples|examples|instances|%)\s*\)|\(\s*\d{2,}[\d,]*\s*\)"
)

# files that hold macros / config, not prose
SKIP_PROSE = {"math_commands.tex", "preamble.tex"}

# enumeration of a taxonomy/inventory belongs in a table/appendix, not the body
ENUM_MIN_ITEMS = 5
ENUM_MIN_COUNTS = 3
PROSE_COUNT_MIN = 4

# a wide table in a single-column float overflows; many columns need table*/rotate/split
TABLE_FLOAT_RE = re.compile(r"\\begin\{table(\*?)\}(.*?)\\end\{table\1\}", re.S)
PLAIN_TABULAR_RE = re.compile(
    r"\\begin\{tabular\}\s*(?:\[[^\]]*\])?\s*\{((?:[^{}]|\{[^{}]*\})*)\}"
)
WIDE_SINGLE_COL_COLS = 6   # >= this many columns in a single-column float likely overflows
VERY_WIDE_COLS = 10        # >= this many columns usually needs rotation or splitting


def count_columns(colspec: str) -> int:
    """Count column slots in a tabular colspec, tolerant of p{..}/>{..}/@{..} groups."""
    spec = re.sub(r"[><@!]\{(?:[^{}]|\{[^{}]*\})*\}", "", colspec)  # drop >{} <{} @{} !{}
    spec = re.sub(r"[pmb]\{(?:[^{}]|\{[^{}]*\})*\}", "p", spec)      # p{..}->one column
    return len(re.findall(r"[lcrpXYZS]", spec))


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


def prose_tex_files(paper_dir: Path) -> list[Path]:
    files = []
    for path in sorted(paper_dir.rglob("*.tex")):
        if path.name in SKIP_PROSE:
            continue
        files.append(path)
    return files


def rel(path: Path, base: Path) -> str:
    try:
        return str(path.relative_to(base))
    except ValueError:
        return str(path)


def check_prose(path: Path, base: Path, errors: list[str], warnings: list[str]) -> None:
    raw = path.read_text(encoding="utf-8", errors="ignore")
    name = rel(path, base)
    for lineno, line in enumerate(raw.splitlines(), 1):
        if MARKER_RE.search(line):
            errors.append(f"unresolved missing-support marker: {name}:{lineno}: {line.strip()}")
    text = strip_comments(raw)
    for lineno, line in enumerate(text.splitlines(), 1):
        if FOOTNOTE_RE.search(line):
            errors.append(f"footnote in prose (banned): {name}:{lineno}")
        m = ARTIFACT_RE.search(line)
        if m:
            errors.append(f"file/code artifact in prose: {name}:{lineno}: {m.group(0).strip()}")
        m = PATH_RE.search(line)
        if m:
            start = max(0, m.start() - 20)
            errors.append(f"local path in prose: {name}:{lineno}: ...{line[start:m.end() + 20].strip()}...")


def check_subsection_budget(path: Path, base: Path, errors: list[str]) -> None:
    text = strip_comments(path.read_text(encoding="utf-8", errors="ignore"))
    name = rel(path, base)
    sections = list(SECTION_RE.finditer(text))
    if len(sections) <= 1:
        count = len(SUBSECTION_RE.findall(text))
        if count > SUBSECTION_BUDGET:
            errors.append(
                f"subsection budget exceeded: {name} has {count} subsections (max {SUBSECTION_BUDGET})"
            )
        return
    # multiple \section in one file: count subsections per section span
    bounds = [m.start() for m in sections] + [len(text)]
    for i in range(len(sections)):
        span = text[bounds[i] : bounds[i + 1]]
        count = len(SUBSECTION_RE.findall(span))
        if count > SUBSECTION_BUDGET:
            label = text[sections[i].start() : sections[i].start() + 60].replace("\n", " ")
            errors.append(
                f"subsection budget exceeded: {name} section '{label.strip()}' has {count} "
                f"subsections (max {SUBSECTION_BUDGET})"
            )


def check_tables(path: Path, base: Path, errors: list[str], warnings: list[str]) -> None:
    text = strip_comments(path.read_text(encoding="utf-8", errors="ignore"))
    name = rel(path, base)
    for lineno, line in enumerate(text.splitlines(), 1):
        if HLINE_RE.search(line):
            errors.append(f"\\hline in table (use booktabs \\toprule/\\midrule/\\bottomrule): {name}:{lineno}")
        if TEXTSC_LOWER_RE.search(line):
            warnings.append(f"\\textsc{{...}} on a lowercase name renders poorly: {name}:{lineno}")
    for m in re.finditer(r"\\begin\{(tabular\*?|tabularx)\}\s*(?:\{[^}]*\}\s*)?\{([^}]*)\}", text):
        colspec = m.group(2)
        if "|" in colspec:
            lineno = text.count("\n", 0, m.start()) + 1
            warnings.append(f"vertical rule (|) in table column spec; booktabs uses none: {name}:{lineno}")


def check_booktabs_loaded(paper_dir: Path, files: list[Path], errors: list[str]) -> None:
    has_table = any(
        TABULAR_BEGIN_RE.search(strip_comments(p.read_text(encoding="utf-8", errors="ignore")))
        for p in files
    )
    if not has_table:
        return
    preamble = ""
    for cand in (paper_dir / "main.tex", paper_dir / "preamble.tex"):
        if cand.exists():
            preamble += cand.read_text(encoding="utf-8", errors="ignore")
    if not BOOKTABS_RE.search(preamble):
        errors.append("tables present but \\usepackage{booktabs} is not loaded in the preamble")


def check_appendix_page(paper_dir: Path, warnings: list[str]) -> None:
    main = paper_dir / "main.tex"
    if not main.exists():
        return
    text = strip_comments(main.read_text(encoding="utf-8", errors="ignore"))
    m = APPENDIX_RE.search(text)
    if not m:
        return
    preceding = text[:m.start()]
    tail = preceding.rstrip().splitlines()[-3:] if preceding.strip() else []
    if not any(CLEARPAGE_RE.search(line) for line in tail):
        warnings.append("\\appendix is not preceded by \\clearpage; appendix may not start on a fresh page")


def check_enumeration(path: Path, base: Path, warnings: list[str]) -> None:
    """Heuristic: flag taxonomy/inventory enumeration and per-category count dumps in body prose.

    Skips appendix files (the appendix is the correct home for full lists). Warnings only.
    """
    name = rel(path, base)
    if "appendix" in path.name.lower():
        return
    text = strip_comments(path.read_text(encoding="utf-8", errors="ignore"))
    for m in LIST_ENV_RE.finditer(text):
        body = m.group(2)
        items = len(ITEM_RE.findall(body))
        counts = len(COUNT_RE.findall(body))
        if items >= ENUM_MIN_ITEMS and counts >= ENUM_MIN_COUNTS:
            lineno = text.count("\n", 0, m.start()) + 1
            warnings.append(
                f"taxonomy/inventory enumeration in body ({items} items, {counts} per-category "
                f"counts): {name}:{lineno}; mention in one stroke and move the full list to a "
                f"table or appendix"
            )
    for lineno, line in enumerate(text.splitlines(), 1):
        hits = len(COUNT_RE.findall(line)) + len(PAREN_COUNT_RE.findall(line))
        if hits >= PROSE_COUNT_MIN:
            warnings.append(
                f"per-category count enumeration in prose ({hits} counts on one line): "
                f"{name}:{lineno}; move the breakdown to a table and cite only load-bearing numbers"
            )


def check_wide_tables(path: Path, base: Path, warnings: list[str]) -> None:
    """Heuristic: flag wide plain-`tabular` tables in single-column floats (likely overflow).

    Applies to body and appendix alike. Warnings only.
    """
    text = strip_comments(path.read_text(encoding="utf-8", errors="ignore"))
    name = rel(path, base)
    for fm in TABLE_FLOAT_RE.finditer(text):
        starred = fm.group(1) == "*"
        body = fm.group(2)
        lineno = text.count("\n", 0, fm.start()) + 1
        for tm in PLAIN_TABULAR_RE.finditer(body):
            ncols = count_columns(tm.group(1))
            if not starred and ncols >= WIDE_SINGLE_COL_COLS:
                warnings.append(
                    f"wide table ({ncols} columns) in a single-column float: {name}:{lineno}; "
                    f"use table* (fill \\textwidth), rotate, or split — it will overflow the column"
                )
            if ncols >= VERY_WIDE_COLS:
                warnings.append(
                    f"very wide table ({ncols} columns): {name}:{lineno}; even table* may overflow "
                    f"\\textwidth — rotate (sidewaystable) or split by column groups"
                )


def check_labels(files: list[Path], base: Path, errors: list[str]) -> None:
    seen: dict[str, str] = {}
    for path in files:
        text = strip_comments(path.read_text(encoding="utf-8", errors="ignore"))
        for lineno, line in enumerate(text.splitlines(), 1):
            for m in LABEL_RE.finditer(line):
                key = m.group(1).strip()
                loc = f"{rel(path, base)}:{lineno}"
                if key in seen:
                    errors.append(f"duplicate \\label: {key} ({seen[key]} and {loc})")
                else:
                    seen[key] = loc


def check_input_consistency(paper_dir: Path, errors: list[str], warnings: list[str]) -> None:
    main = paper_dir / "main.tex"
    if not main.exists():
        warnings.append("no main.tex found; skipped input-consistency check")
        return
    text = strip_comments(main.read_text(encoding="utf-8", errors="ignore"))
    inputs = set()
    for m in INPUT_RE.finditer(text):
        target = m.group(1).strip()
        if not target.endswith(".tex"):
            target += ".tex"
        inputs.add((paper_dir / target).resolve())
    for target in sorted(inputs):
        if not target.exists():
            errors.append(f"\\input references missing file: {rel(target, paper_dir)}")
    sec_dir = paper_dir / "sections"
    if sec_dir.is_dir():
        for path in sorted(sec_dir.glob("*.tex")):
            if path.resolve() not in inputs:
                warnings.append(f"orphan section file not \\input by main.tex: {rel(path, paper_dir)}")


def check_log(paper_dir: Path, warnings: list[str]) -> None:
    log = paper_dir / "main.log"
    if not log.exists():
        return
    text = log.read_text(encoding="utf-8", errors="ignore")
    if "There were undefined references" in text or re.search(r"Reference `[^']+' on page", text):
        warnings.append("compile log: undefined references present")
    if re.search(r"Citation `[^']+' (?:on page .*?)?undefined", text):
        warnings.append("compile log: undefined citations present")
    if "multiply defined" in text:
        warnings.append("compile log: multiply-defined labels present")
    overfull = len(re.findall(r"Overfull \\hbox", text))
    if overfull:
        warnings.append(f"compile log: {overfull} overfull hbox warning(s)")


def content_pages_before_references(text_pages: list[str]) -> int:
    """Return the last page counted as main content.

    If references start midway down a page, that page still counts against a
    content-page limit because main text reached it.
    """

    for index, page_text in enumerate(text_pages, 1):
        if REFERENCE_HEADING_RE.search(page_text):
            return index
    return len(text_pages)


def pdf_page_count(pdf_path: Path) -> int | None:
    if shutil.which("pdfinfo") is None:
        return None
    proc = subprocess.run(
        ["pdfinfo", str(pdf_path)],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    if proc.returncode != 0:
        return None
    for line in proc.stdout.splitlines():
        if line.lower().startswith("pages:"):
            try:
                return int(line.split(":", 1)[1].strip())
            except ValueError:
                return None
    return None


def pdf_text_pages(pdf_path: Path, page_count: int) -> list[str] | None:
    if shutil.which("pdftotext") is None:
        return None
    pages: list[str] = []
    for page in range(1, page_count + 1):
        proc = subprocess.run(
            ["pdftotext", "-f", str(page), "-l", str(page), str(pdf_path), "-"],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            check=False,
        )
        if proc.returncode != 0:
            return None
        pages.append(proc.stdout.replace("\f", ""))
    return pages


def check_page_budget(
    paper_dir: Path,
    max_content_pages: int | None,
    errors: list[str],
    warnings: list[str],
) -> None:
    if max_content_pages is None:
        return
    pdf_path = paper_dir / "main.pdf"
    if not pdf_path.exists():
        errors.append("--max-content-pages was set, but paper/main.pdf is missing")
        return
    page_count = pdf_page_count(pdf_path)
    if page_count is None:
        errors.append("cannot check content-page budget because pdfinfo is unavailable or failed")
        return
    pages = pdf_text_pages(pdf_path, page_count)
    if pages is None:
        errors.append("cannot check content-page budget because pdftotext is unavailable or failed")
        return
    content_pages = content_pages_before_references(pages)
    if content_pages > max_content_pages:
        errors.append(
            f"content-page budget exceeded: main text reaches page {content_pages} "
            f"(limit {max_content_pages}; references page counts if main text reaches it)"
        )
    else:
        warnings.append(f"content-page budget ok: main text reaches page {content_pages}/{max_content_pages}")


def audit(paper_dir: Path, max_content_pages: int | None = None) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    files = prose_tex_files(paper_dir)
    if not files:
        errors.append(f"no .tex files found under {paper_dir}")
        return errors, warnings

    for path in files:
        check_prose(path, paper_dir, errors, warnings)
        check_subsection_budget(path, paper_dir, errors)
        check_tables(path, paper_dir, errors, warnings)
        check_enumeration(path, paper_dir, warnings)
        check_wide_tables(path, paper_dir, warnings)
    check_booktabs_loaded(paper_dir, files, errors)
    check_appendix_page(paper_dir, warnings)
    check_labels(files, paper_dir, errors)
    check_input_consistency(paper_dir, errors, warnings)
    check_log(paper_dir, warnings)
    check_page_budget(paper_dir, max_content_pages, errors, warnings)
    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit mechanical draft-hygiene rules for a LaTeX paper.")
    parser.add_argument("paper_dir", nargs="?", default="paper", help="Paper directory containing main.tex")
    parser.add_argument(
        "--max-content-pages",
        type=int,
        default=None,
        help="Fail if compiled main text reaches beyond this page before references.",
    )
    args = parser.parse_args()

    paper_dir = Path(args.paper_dir).resolve()
    errors, warnings = audit(paper_dir, max_content_pages=args.max_content_pages)

    print(f"Draft hygiene audit: {paper_dir}")
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
