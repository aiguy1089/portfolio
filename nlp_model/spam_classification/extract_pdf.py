"""
Extract text from a PDF and save it as a UTF-8 text file.

Usage:
  python extract_pdf.py <input_pdf_path> <output_text_path>
If no arguments are provided, it defaults to the known repo PDF path and writes assignment_text.txt next to it.
"""
from __future__ import annotations
import sys
from pathlib import Path
from typing import Optional

try:
    from pypdf import PdfReader
except Exception as e:
    print("ERROR: pypdf is not installed. Install with: py -3 -m pip install pypdf", file=sys.stderr)
    raise

# Default paths (repository-specific)
REPO_ROOT = Path(r"c:\Users\Admin\D803 QLN1 Task 2 Developing and Evaluating the Natural Language Processing Model")
DEFAULT_INPUT = REPO_ROOT / "QLN1 Task 2 Developing and Evaluating the Natural Language Processing Model.pdf"
DEFAULT_OUTPUT = REPO_ROOT / "assignment_text.txt"


def extract_pdf_text(input_pdf: Path) -> str:
    """Extract text from all pages of the PDF with page markers."""
    reader = PdfReader(str(input_pdf))  # str() to avoid Windows path quirks
    parts = []
    for i, page in enumerate(reader.pages, start=1):
        try:
            text = page.extract_text() or ""
        except Exception as e:
            text = f"[Warning] Could not extract text from page {i}: {e}\n"
        parts.append(f"\n\n==== Page {i} ====" )
        parts.append("\n")
        parts.append(text)
    return "".join(parts)


def main(argv: list[str]) -> int:
    input_path = Path(argv[1]) if len(argv) >= 2 else DEFAULT_INPUT
    output_path = Path(argv[2]) if len(argv) >= 3 else DEFAULT_OUTPUT

    if not input_path.exists():
        print(f"ERROR: Input PDF not found: {input_path}", file=sys.stderr)
        return 2

    try:
        text = extract_pdf_text(input_path)
    except Exception as e:
        print(f"ERROR: Failed to read PDF: {e}", file=sys.stderr)
        return 3

    try:
        output_path.write_text(text, encoding="utf-8")
    except Exception as e:
        print(f"ERROR: Failed to write output file {output_path}: {e}", file=sys.stderr)
        return 4

    print(f"Extracted text written to: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))