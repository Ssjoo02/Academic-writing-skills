#!/usr/bin/env python3
"""Minimal paper-figure MCP helper.

This server is deliberately narrow: it classifies figure ideas and writes
simple FigureSpec JSON skeletons under a caller-provided workspace. It does
not create paper claims, results, citations, or prose.
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from typing import Any


sys.stdout = os.fdopen(sys.stdout.fileno(), "wb", buffering=0)
sys.stdin = os.fdopen(sys.stdin.fileno(), "rb", buffering=0)

SERVER_NAME = "paper-figure"
PROTOCOL_VERSION = "2024-11-05"
_use_ndjson = False


def send_response(response: dict[str, Any]) -> None:
    global _use_ndjson
    payload = json.dumps(response, ensure_ascii=True, separators=(",", ":")).encode("utf-8")
    if _use_ndjson:
        sys.stdout.write(payload + b"\n")
    else:
        header = f"Content-Length: {len(payload)}\r\n\r\n".encode("utf-8")
        sys.stdout.write(header + payload)
    sys.stdout.flush()


def read_message() -> dict[str, Any] | None:
    global _use_ndjson
    line = sys.stdin.readline()
    if not line:
        return None
    text = line.decode("utf-8").rstrip("\r\n")
    if text.lower().startswith("content-length:"):
        try:
            length = int(text.split(":", 1)[1].strip())
        except ValueError:
            return None
        while True:
            header_line = sys.stdin.readline()
            if not header_line:
                return None
            if header_line in {b"\r\n", b"\n"}:
                break
        body = sys.stdin.read(length)
        try:
            return json.loads(body.decode("utf-8"))
        except json.JSONDecodeError:
            return None
    if text.startswith("{"):
        _use_ndjson = True
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            return None
    return None


def tool_result(request_id: Any, text: str) -> dict[str, Any]:
    return {
        "jsonrpc": "2.0",
        "id": request_id,
        "result": {"content": [{"type": "text", "text": text}]},
    }


def tool_error(request_id: Any, message: str) -> dict[str, Any]:
    return {
        "jsonrpc": "2.0",
        "id": request_id,
        "error": {"code": -32000, "message": message},
    }


def classify_figure(args: dict[str, Any]) -> dict[str, Any]:
    figure_id = str(args.get("figure_id", "<figure-id>"))
    figure_type = str(args.get("type_hint", "")).lower()
    message = str(args.get("message", "")).lower()
    source = str(args.get("source", "")).lower()

    route = "current-agent drawing"
    section = args.get("section") or "TBD"
    output = f"paper/figures/{figure_id}.png"

    plot_terms = ["result", "metric", "accuracy", "rate", "curve", "ablation", "scaling", "csv", "json"]
    diagram_terms = ["architecture", "pipeline", "workflow", "system", "component", "taxonomy", "overview"]
    picture_terms = ["teaser", "illustration", "picture", "concept", "visual summary", "qualitative"]
    table_terms = ["table", "comparison", "baseline", "benchmark statistics"]

    haystack = " ".join([figure_type, message, source])
    if any(term in haystack for term in table_terms):
        route = "LaTeX table"
        output = "paper/figures/tables/<figure-id>.tex"
    elif any(term in haystack for term in plot_terms) or source.endswith((".csv", ".json", ".tsv")):
        route = "reproducible plot script"
        output = f"paper/figures/{figure_id}.pdf"
    elif any(term in haystack for term in diagram_terms):
        route = "FigureSpec MCP"
        output = "JSON spec + SVG/PDF under paper/figures/"
    elif any(term in haystack for term in picture_terms):
        route = "AI picture generation"
        output = f"Picture Brief + paper/figures/{figure_id}.png"
    elif "screenshot" in haystack or "example" in haystack or "qualitative" in haystack:
        route = "existing asset"
        output = "copied asset under paper/figures/"

    return {
        "route": route,
        "section": section,
        "recommended_output": output,
        "caption_policy": "State the figure message, the comparison or mechanism, and the supported claim.",
    }


def safe_output_path(cwd: str, relpath: str) -> Path:
    root = Path(cwd).expanduser().resolve()
    path = (root / relpath).resolve()
    if root != path and root not in path.parents:
        raise ValueError("output path must stay under cwd")
    return path


def write_figurespec_skeleton(args: dict[str, Any]) -> dict[str, Any]:
    cwd = str(args.get("cwd", "."))
    figure_id = str(args.get("figure_id", "fig_overview"))
    output_relpath = str(args.get("output_relpath", f"paper/figures/specs/{figure_id}.json"))
    title = str(args.get("title", figure_id))
    nodes = args.get("nodes") or [
        {"id": "input", "label": "Input", "x": 120, "y": 160, "shape": "rounded"},
        {"id": "method", "label": "Method", "x": 320, "y": 160, "shape": "rounded"},
        {"id": "evidence", "label": "Evidence", "x": 520, "y": 160, "shape": "rounded"},
    ]
    edges = args.get("edges") or [
        {"from": "input", "to": "method", "label": "feeds"},
        {"from": "method", "to": "evidence", "label": "supports"},
    ]

    spec = {
        "canvas": {"width": 700, "height": 320},
        "title": title,
        "nodes": nodes,
        "edges": edges,
        "groups": args.get("groups", []),
        "metadata": {
            "figure_id": figure_id,
            "note": "Generated skeleton. Verify semantic accuracy before rendering.",
        },
    }
    output_path = safe_output_path(cwd, output_relpath)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(spec, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return {"path": str(output_path), "spec": spec}


def normalize_lines(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    text = str(value).strip()
    if not text:
        return []
    return [line.strip() for line in text.splitlines() if line.strip()]


def markdown_bullets(items: list[str], fallback: str = "TBD") -> str:
    if not items:
        return f"- {fallback}"
    return "\n".join(f"- {item}" for item in items)


def write_picture_brief(args: dict[str, Any]) -> dict[str, Any]:
    cwd = str(args.get("cwd", "."))
    figure_id = str(args.get("figure_id", "fig_picture"))
    output_relpath = str(args.get("output_relpath", f"paper/figures/prompts/{figure_id}.md"))
    title = str(args.get("title", figure_id))
    section = str(args.get("section", "TBD"))
    figure_type = str(args.get("figure_type", "AI picture generation"))
    message = str(args.get("message", "TBD"))
    supported_claim = str(args.get("supported_claim", "TBD"))
    renderer = str(args.get("renderer", "host image-generation tool or Gemini-compatible API"))
    output_image = str(args.get("output_image", f"paper/figures/{figure_id}.png"))

    source_files = normalize_lines(args.get("source_files"))
    confirmed_concepts = normalize_lines(args.get("confirmed_concepts"))
    allowed_labels = normalize_lines(args.get("allowed_labels"))
    forbidden_labels = normalize_lines(args.get("forbidden_labels"))
    visual_elements = normalize_lines(args.get("visual_elements"))
    relationships = normalize_lines(args.get("relationships"))
    style = str(args.get("style", "clean white background, restrained academic palette, readable English labels"))
    avoid = normalize_lines(args.get("avoid")) or [
        "unsupported numbers",
        "invented modules",
        "decorative clip art",
        "rainbow gradients",
        "tiny unreadable text",
    ]

    direct_image_prompt = "\n".join(
        [
            "Create a publication-quality academic figure for a research paper.",
            "",
            f"Message: {message}",
            "Show exactly these visual elements:",
            markdown_bullets(visual_elements),
            "Use exactly these labels:",
            markdown_bullets(allowed_labels),
            "Relationships and arrows:",
            markdown_bullets(relationships),
            f"Style constraints: {style}.",
            "Avoid:",
            markdown_bullets(avoid),
            "Do not add claims, modules, datasets, numbers, or labels that are not listed above.",
        ]
    )

    brief = f"""# Picture Brief: {figure_id}

## Figure Identity
- Figure ID: {figure_id}
- Title: {title}
- Section: {section}
- Figure type: {figure_type}
- One-sentence message: {message}
- Supported claim: {supported_claim}

## Evidence Boundary
- Source files:
{markdown_bullets(source_files)}
- Confirmed concepts:
{markdown_bullets(confirmed_concepts)}
- Labels allowed in the image:
{markdown_bullets(allowed_labels)}
- Labels or claims forbidden in the image:
{markdown_bullets(forbidden_labels)}

## Visual Plan
- Canvas: publication figure, single-column or double-column as selected by the Paper Framework
- Layout: use the section and figure message above; avoid clutter and ambiguous flow
- Main visual elements:
{markdown_bullets(visual_elements)}
- Data flow or relationships:
{markdown_bullets(relationships)}
- Style: {style}
- Accessibility: readable at paper scale, colorblind-safe, grayscale-friendly

## Direct Image Prompt
{direct_image_prompt}

## Renderer Route
- Preferred renderer: {renderer}
- Renderer status: not run by this MCP tool
- Output path: {output_image}
- API prompt source: use the exact `Direct Image Prompt` block above
- Review notes: inspect generated image for invented content, wrong labels, unreadable text, and wrong arrow direction before accepting it.
"""

    output_path = safe_output_path(cwd, output_relpath)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(brief, encoding="utf-8")
    return {"path": str(output_path), "output_image": output_image, "direct_image_prompt": direct_image_prompt}


def handle_request(request: dict[str, Any]) -> dict[str, Any] | None:
    method = request.get("method", "")
    params = request.get("params", {})
    request_id = request.get("id")

    if request_id is None:
        return None

    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "protocolVersion": PROTOCOL_VERSION,
                "capabilities": {"tools": {}},
                "serverInfo": {"name": SERVER_NAME, "version": "0.1.0"},
            },
        }
    if method == "ping":
        return {"jsonrpc": "2.0", "id": request_id, "result": {}}
    if method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "tools": [
                    {
                        "name": "classify_figure",
                        "description": "Classify a paper figure/table idea into a generation route.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "figure_id": {"type": "string"},
                                "type_hint": {"type": "string"},
                                "section": {"type": "string"},
                                "message": {"type": "string"},
                                "source": {"type": "string"},
                            },
                        },
                    },
                    {
                        "name": "write_figurespec_skeleton",
                        "description": "Write a simple FigureSpec JSON skeleton under cwd.",
                        "inputSchema": {
                            "type": "object",
                            "required": ["cwd", "figure_id"],
                            "properties": {
                                "cwd": {"type": "string"},
                                "figure_id": {"type": "string"},
                                "output_relpath": {"type": "string"},
                                "title": {"type": "string"},
                                "nodes": {"type": "array"},
                                "edges": {"type": "array"},
                                "groups": {"type": "array"},
                            },
                        },
                    },
                    {
                        "name": "write_picture_brief",
                        "description": "Write a Markdown Picture Brief for an AI-generated paper picture under cwd.",
                        "inputSchema": {
                            "type": "object",
                            "required": ["cwd", "figure_id"],
                            "properties": {
                                "cwd": {"type": "string"},
                                "figure_id": {"type": "string"},
                                "output_relpath": {"type": "string"},
                                "title": {"type": "string"},
                                "section": {"type": "string"},
                                "figure_type": {"type": "string"},
                                "message": {"type": "string"},
                                "supported_claim": {"type": "string"},
                                "renderer": {"type": "string"},
                                "output_image": {"type": "string"},
                                "source_files": {"type": "array"},
                                "confirmed_concepts": {"type": "array"},
                                "allowed_labels": {"type": "array"},
                                "forbidden_labels": {"type": "array"},
                                "visual_elements": {"type": "array"},
                                "relationships": {"type": "array"},
                                "style": {"type": "string"},
                                "avoid": {"type": "array"},
                            },
                        },
                    },
                ]
            },
        }
    if method == "tools/call":
        name = params.get("name")
        args = params.get("arguments", {})
        try:
            if name == "classify_figure":
                return tool_result(request_id, json.dumps(classify_figure(args), indent=2, ensure_ascii=False))
            if name == "write_figurespec_skeleton":
                return tool_result(request_id, json.dumps(write_figurespec_skeleton(args), indent=2, ensure_ascii=False))
            if name == "write_picture_brief":
                return tool_result(request_id, json.dumps(write_picture_brief(args), indent=2, ensure_ascii=False))
            return tool_error(request_id, f"unknown tool: {name}")
        except Exception as exc:
            return tool_error(request_id, str(exc))
    return tool_error(request_id, f"unsupported method: {method}")


def main() -> None:
    while True:
        request = read_message()
        if request is None:
            break
        response = handle_request(request)
        if response is not None:
            send_response(response)


if __name__ == "__main__":
    main()
