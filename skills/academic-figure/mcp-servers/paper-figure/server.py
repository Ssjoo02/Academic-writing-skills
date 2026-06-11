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
import xml.etree.ElementTree as ET
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
    picture_terms = ["teaser", "illustration", "picture", "concept", "visual summary"]
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


def render_figurespec(args: dict[str, Any]) -> dict[str, Any]:
    """Render a FigureSpec JSON file or inline spec to SVG.

    Reads nodes (with x, y, label, shape) and edges (from, to, label) and
    produces a clean academic-style SVG suitable for paper inclusion.
    """
    cwd = str(args.get("cwd", "."))
    spec_path = args.get("spec_path")
    spec_inline = args.get("spec")
    figure_id = str(args.get("figure_id", "fig_diagram"))
    output_relpath = str(args.get("output_relpath", f"paper/figures/{figure_id}.svg"))

    # Load spec
    if spec_path is not None:
        spec_path_resolved = safe_output_path(cwd, str(spec_path))
        spec = json.loads(spec_path_resolved.read_text(encoding="utf-8"))
    elif spec_inline is not None:
        spec = spec_inline
    else:
        raise ValueError("render_figurespec requires spec_path or spec")

    canvas = spec.get("canvas", {"width": 700, "height": 320})
    width = int(canvas.get("width", 700))
    height = int(canvas.get("height", 320))
    title = str(spec.get("title", figure_id))
    nodes = spec.get("nodes", [])
    edges = spec.get("edges", [])
    groups = spec.get("groups", [])

    # SVG namespace
    NS = "http://www.w3.org/2000/svg"
    ET.register_namespace("", NS)
    svg = ET.Element(
        "svg",
        {
            "xmlns": NS,
            "viewBox": f"0 0 {width} {height}",
            "width": str(width),
            "height": str(height),
            "font-family": "Arial, Helvetica, DejaVu Sans, sans-serif",
            "font-size": "11",
        },
    )

    # Style
    style = ET.SubElement(svg, "style")
    style.text = """
    .node-rect { fill: #f0f4f8; stroke: #3a6b99; stroke-width: 1.5; rx: 6; ry: 6; }
    .node-rect-highlight { fill: #e8f0e8; stroke: #2e7d32; stroke-width: 2; rx: 6; ry: 6; }
    .node-text { fill: #1a1a1a; font-size: 11px; text-anchor: middle; dominant-baseline: central; }
    .node-title { fill: #3a6b99; font-size: 10px; text-anchor: middle; font-weight: bold; }
    .edge-line { stroke: #666666; stroke-width: 1.2; fill: none; marker-end: url(#arrowhead); }
    .edge-text { fill: #666666; font-size: 9px; text-anchor: middle; }
    .group-rect { fill: #f8f8f8; stroke: #cccccc; stroke-width: 1; stroke-dasharray: 4 4; rx: 4; ry: 4; }
    .group-label { fill: #888888; font-size: 10px; font-style: italic; }
    .bg { fill: #ffffff; }
    """

    # Defs for arrowhead marker
    defs = ET.SubElement(svg, "defs")
    marker = ET.SubElement(
        defs,
        "marker",
        {
            "id": "arrowhead",
            "markerWidth": "8",
            "markerHeight": "6",
            "refX": "8",
            "refY": "3",
            "orient": "auto",
        },
    )
    ET.SubElement(marker, "path", {"d": "M0,0 L8,3 L0,6 Z", "fill": "#666666"})

    # Background
    ET.SubElement(svg, "rect", {"class": "bg", "x": "0", "y": "0", "width": str(width), "height": str(height)})

    # Groups (background regions)
    for group in groups:
        gx = int(group.get("x", 0))
        gy = int(group.get("y", 0))
        gw = int(group.get("width", 100))
        gh = int(group.get("height", 100))
        glabel = str(group.get("label", ""))
        ET.SubElement(
            svg,
            "rect",
            {"class": "group-rect", "x": str(gx), "y": str(gy), "width": str(gw), "height": str(gh)},
        )
        if glabel:
            ET.SubElement(
                svg,
                "text",
                {"class": "group-label", "x": str(gx + 6), "y": str(gy + 14)},
            )
            ET.SubElement(svg, "text")  # placeholder — text set below
            # Find the text element we just added and set its text
            svg[-1].text = glabel

    # Edges (drawn before nodes so nodes sit on top)
    node_positions: dict[str, tuple[float, float, float, float]] = {}
    for node in nodes:
        nid = str(node.get("id", ""))
        nx = float(node.get("x", 0))
        ny = float(node.get("y", 0))
        nw = float(node.get("width", 120))
        nh = float(node.get("height", 48))
        node_positions[nid] = (nx, ny, nw, nh)

    for edge in edges:
        src_id = str(edge.get("from", ""))
        tgt_id = str(edge.get("to", ""))
        elabel = str(edge.get("label", ""))

        if src_id in node_positions and tgt_id in node_positions:
            sx, sy, sw, sh = node_positions[src_id]
            tx, ty, tw, th = node_positions[tgt_id]

            # Start from right edge of source, end at left edge of target
            x1 = sx + sw
            y1 = sy + sh / 2
            x2 = tx
            y2 = ty + th / 2

            ET.SubElement(
                svg,
                "line",
                {"class": "edge-line", "x1": str(x1), "y1": str(y1), "x2": str(x2), "y2": str(y2)},
            )
            if elabel:
                mx = (x1 + x2) / 2
                my = (y1 + y2) / 2 - 8
                ET.SubElement(svg, "text", {"class": "edge-text", "x": str(mx), "y": str(my)})
                svg[-1].text = elabel

    # Nodes
    for node in nodes:
        nid = str(node.get("id", ""))
        nlabel = str(node.get("label", nid))
        nx = float(node.get("x", 0))
        ny = float(node.get("y", 0))
        nw = float(node.get("width", 120))
        nh = float(node.get("height", 48))
        nshape = str(node.get("shape", "rounded"))
        nhighlight = bool(node.get("highlight", False))

        rect_class = "node-rect-highlight" if nhighlight else "node-rect"
        if nshape == "rounded":
            ET.SubElement(
                svg,
                "rect",
                {
                    "class": rect_class,
                    "x": str(nx),
                    "y": str(ny),
                    "width": str(nw),
                    "height": str(nh),
                },
            )
        else:
            ET.SubElement(
                svg,
                "rect",
                {
                    "class": rect_class,
                    "x": str(nx),
                    "y": str(ny),
                    "width": str(nw),
                    "height": str(nh),
                    "rx": "0",
                    "ry": "0",
                },
            )

        # Title (node id as small label above)
        title_y = ny - 6
        ET.SubElement(svg, "text", {"class": "node-title", "x": str(nx + nw / 2), "y": str(title_y)})
        svg[-1].text = nid

        # Label (main text inside node)
        ET.SubElement(svg, "text", {"class": "node-text", "x": str(nx + nw / 2), "y": str(ny + nh / 2)})
        svg[-1].text = nlabel

    # Title at top
    if title:
        ET.SubElement(svg, "text", {"class": "node-text", "x": str(width / 2), "y": "16", "font-size": "13", "font-weight": "bold"})
        svg[-1].text = title

    # Serialize
    svg_bytes = ET.tostring(svg, encoding="unicode", xml_declaration=False)
    # Pretty-print: add XML declaration and ensure newline
    svg_output = '<?xml version="1.0" encoding="UTF-8"?>\n' + svg_bytes + "\n"

    output_path = safe_output_path(cwd, output_relpath)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(svg_output, encoding="utf-8")

    return {
        "path": str(output_path),
        "width": width,
        "height": height,
        "node_count": len(nodes),
        "edge_count": len(edges),
        "group_count": len(groups),
    }


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


def configured_picture_renderer() -> tuple[str, str]:
    """Auto-detect picture API from standard environment variables.

    Priority: Gemini if GEMINI_API_KEY is set, else GPT-image if OPENAI_API_KEY
    is set, else current-agent drawing. No custom-prefix env vars needed.
    """
    gemini_key = os.environ.get("GEMINI_API_KEY", "").strip()
    openai_key = os.environ.get("OPENAI_API_KEY", "").strip()

    if gemini_key:
        model = os.environ.get("GEMINI_IMAGE_MODEL", "").strip() or "gemini-2.5-flash-image"
        base_url = os.environ.get("GEMINI_BASE_URL", "").strip()
        route = f"Gemini-compatible API ({model})"
        if base_url:
            route = f"{route} via {base_url}"
        return route, "configured from environment; render step should use the image API"

    if openai_key:
        model = os.environ.get("OPENAI_IMAGE_MODEL", "").strip() or "gpt-image-1.5"
        base_url = os.environ.get("OPENAI_BASE_URL", "").strip()
        route = f"GPT-image-compatible API ({model})"
        if base_url:
            route = f"{route} via {base_url}"
        return route, "configured from environment; render step should use the image API"

    return "current executing agent", "no picture API configured; render step should use the current agent fallback"


def write_picture_brief(args: dict[str, Any]) -> dict[str, Any]:
    cwd = str(args.get("cwd", "."))
    figure_id = str(args.get("figure_id", "fig_picture"))
    output_relpath = str(args.get("output_relpath", f"paper/figures/prompts/{figure_id}.md"))
    title = str(args.get("title", figure_id))
    section = str(args.get("section", "TBD"))
    figure_type = str(args.get("figure_type", "AI picture generation"))
    message = str(args.get("message", "TBD"))
    supported_claim = str(args.get("supported_claim", "TBD"))
    configured_renderer, renderer_status = configured_picture_renderer()
    renderer = str(args.get("renderer") or configured_renderer)
    renderer_status = str(args.get("renderer_status") or renderer_status)
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
- Renderer status: {renderer_status}
- Output path: {output_image}
- API prompt source: use the exact `Direct Image Prompt` block above
- Review notes: inspect generated image for invented content, wrong labels, unreadable text, and wrong arrow direction before accepting it.
"""

    output_path = safe_output_path(cwd, output_relpath)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(brief, encoding="utf-8")
    return {
        "path": str(output_path),
        "output_image": output_image,
        "direct_image_prompt": direct_image_prompt,
        "renderer": renderer,
        "renderer_status": renderer_status,
    }


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
                "serverInfo": {"name": SERVER_NAME, "version": "0.2.0"},
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
                    {
                        "name": "render_figurespec",
                        "description": "Render a FigureSpec JSON (from write_figurespec_skeleton or hand-written) to an editable SVG diagram. Reads nodes, edges, groups, and canvas; produces a clean academic-style SVG suitable for paper inclusion.",
                        "inputSchema": {
                            "type": "object",
                            "required": ["cwd"],
                            "properties": {
                                "cwd": {"type": "string"},
                                "figure_id": {"type": "string"},
                                "spec_path": {"type": "string", "description": "Path to a FigureSpec JSON file to render"},
                                "spec": {"type": "object", "description": "Inline FigureSpec object (alternative to spec_path)"},
                                "output_relpath": {"type": "string", "description": "Output SVG path relative to cwd"},
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
            if name == "render_figurespec":
                return tool_result(request_id, json.dumps(render_figurespec(args), indent=2, ensure_ascii=False))
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
