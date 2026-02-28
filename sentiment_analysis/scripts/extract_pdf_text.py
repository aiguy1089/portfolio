import sys
from pathlib import Path
from pypdf import PdfReader


def extract_pdf_to_text(pdf_path: Path, out_path: Path) -> None:
    reader = PdfReader(str(pdf_path))
    parts = []
    for i, page in enumerate(reader.pages):
        try:
            text = page.extract_text() or ""
        except Exception as e:
            text = f"\n[Error extracting page {i+1}: {e}]\n"
        parts.append(f"\n\n===== Page {i+1} =====\n\n{text}\n")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("".join(parts), encoding="utf-8")


def main():
    if len(sys.argv) < 3:
        print("Usage: python extract_pdf_text.py <pdf_path> <out_txt_path>")
        sys.exit(1)
    pdf_path = Path(sys.argv[1])
    out_path = Path(sys.argv[2])
    if not pdf_path.exists():
        print(f"PDF not found: {pdf_path}")
        sys.exit(2)
    extract_pdf_to_text(pdf_path, out_path)
    print(f"Extracted text to: {out_path}")


if __name__ == "__main__":
    main()