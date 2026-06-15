import base64
import io
import importlib.util
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills" / "academic-figure" / "scripts" / "render_picture_api.py"


def load_module():
    spec = importlib.util.spec_from_file_location("render_picture_api", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class RenderPictureApiTest(unittest.TestCase):
    def test_extracts_direct_image_prompt(self):
        module = load_module()
        markdown = """# Picture Brief: fig_test

## Evidence Boundary
- Labels allowed in the image:
- Encoder
- Loss
- Labels or claims forbidden in the image:
- Accuracy
- Extra dataset

## Direct Image Prompt
A clean flat vector academic illustration with the label "Encoder".

## Renderer Route
- Output path: paper/figures/fig_test.png
- PDF output path: paper/figures/fig_test.pdf
"""
        self.assertEqual(
            module.extract_section(markdown, "Direct Image Prompt"),
            'A clean flat vector academic illustration with the label "Encoder".',
        )
        self.assertEqual(module.extract_allowed_labels(markdown), ["Encoder", "Loss"])
        self.assertEqual(module.extract_pdf_output_path(markdown), "paper/figures/fig_test.pdf")

    def test_decodes_gemini_inline_data(self):
        module = load_module()
        image = b"\x89PNG\r\n\x1a\n" + b"0" * 80
        response = {
            "candidates": [
                {"content": {"parts": [{"inlineData": {"mimeType": "image/png", "data": base64.b64encode(image).decode()}}]}}
            ]
        }
        self.assertEqual(module.decode_image_from_response(response), image)

    def test_dry_run_selects_gemini_without_calling_network(self):
        with tempfile.TemporaryDirectory() as tmp:
            brief = Path(tmp) / "brief.md"
            brief.write_text(
                """# Picture Brief: fig_test

## Direct Image Prompt
A flat vector academic figure with legible labels "Encoder" and "Loss".

## Renderer Route
- Output path: paper/figures/fig_test.png
""",
                encoding="utf-8",
            )
            env = os.environ.copy()
            env["GEMINI_API_KEY"] = "test-key"
            env.pop("OPENAI_API_KEY", None)
            result = subprocess.run(
                [sys.executable, str(SCRIPT), "--brief", str(brief), "--dry-run"],
                cwd=tmp,
                env=env,
                text=True,
                capture_output=True,
                check=True,
            )
            self.assertIn('"renderer": "gemini"', result.stdout)
            self.assertIn('"prompt_chars":', result.stdout)

    def test_postprocess_trims_and_pads_to_banner_aspect(self):
        module = load_module()
        try:
            from PIL import Image, ImageDraw
        except ImportError:
            self.skipTest("Pillow is required for image postprocessing")

        image = Image.new("RGB", (120, 120), "white")
        draw = ImageDraw.Draw(image)
        draw.rectangle((30, 52, 90, 68), fill="black")
        raw = io.BytesIO()
        image.save(raw, format="PNG")

        processed = module.postprocess_image_bytes(
            raw.getvalue(),
            trim_whitespace=True,
            trim_threshold=5,
            trim_pad=4,
            pad_aspect="3:1",
            overlay_labels=["Input", "Output"],
            overlay_layout="horizontal-bottom",
        )
        with Image.open(io.BytesIO(processed)) as opened:
            ratio = opened.width / opened.height
            self.assertAlmostEqual(ratio, 3.0, delta=0.04)
            self.assertLess(opened.height, 120)

    def test_writes_pdf_copy(self):
        module = load_module()
        try:
            from PIL import Image
        except ImportError:
            self.skipTest("Pillow is required for PDF export")

        with tempfile.TemporaryDirectory() as tmp:
            image = Image.new("RGB", (80, 30), "white")
            raw = io.BytesIO()
            image.save(raw, format="PNG")
            pdf_path = Path(tmp) / "figure.pdf"
            module.write_pdf(pdf_path, raw.getvalue())
            self.assertTrue(pdf_path.exists())
            self.assertTrue(pdf_path.read_bytes().startswith(b"%PDF"))


if __name__ == "__main__":
    unittest.main()
