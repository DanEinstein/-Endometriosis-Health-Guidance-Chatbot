"""
Clean raw PDFs from data/pdfs/ into cleaned_data/ for embedding.

Engines (used when installed; missing ones are skipped):
  - pymupdf: native/block extract + text-only cleaned PDF
  - tesseract: OCR for low-text pages
  - docling / docline: structured markdown (preferred for IEEE two-column)
  - marker: alternate academic extract
  - unstructured: hi_res layout partition

Primary outputs used by chroma_vector.py:
  cleaned_data/<stem>.md
  cleaned_data/<stem>.pdf
"""

from __future__ import annotations

import argparse
import re
import shutil
import sys
from pathlib import Path

import pymupdf
from tqdm import tqdm

# Keep the old name used throughout this module.
fitz = pymupdf

RAW_DIR = Path("data/pdfs")
CLEAN_DIR = Path("cleaned_data")
BY_ENGINE_DIR = CLEAN_DIR / "by_engine"

MIN_TEXT_CHARS = 40
MIN_USEFUL_CHARS = 80

REF_HEADING_RE = re.compile(
    r"(?im)^\s*(?:\d+\.?\s*)?(references|bibliography|works cited|"
    r"literature cited|reference list)\s*$"
)
OPTIONAL_TRAILING_RE = re.compile(
    r"(?im)^\s*(?:\d+\.?\s*)?(acknowledgements?|acknowledgment|appendix(\s+[a-z0-9]+)?)\s*$"
)

# In-text citation patterns (applied carefully on body text).
PAREN_AUTHOR_YEAR_RE = re.compile(
    r"\((?:[A-Z][A-Za-z'`\-]+(?:\s+et\s+al\.)?(?:\s*&\s*[A-Z][A-Za-z'`\-]+)?(?:,\s*)?)+"
    r"(?:\d{4}[a-z]?(?:\s*;\s*)?)+\)"
)
NUMERIC_BRACKET_RE = re.compile(r"\[(?:\d+\s*[-–—,]\s*)*\d+\]")
MULTI_SPACE_RE = re.compile(r"[ \t]{2,}")


def list_raw_pdfs() -> list[Path]:
    if not RAW_DIR.exists():
        raise SystemExit(f"Raw PDF folder not found: {RAW_DIR.resolve()}")
    pdfs = sorted(p for p in RAW_DIR.glob("*.pdf") if p.is_file())
    if not pdfs:
        raise SystemExit(f"No PDFs found in {RAW_DIR.resolve()}. Add source PDFs there first.")
    return pdfs


def slugify_stem(path: Path) -> str:
    stem = path.stem.strip()
    stem = re.sub(r"[^\w\-]+", "_", stem, flags=re.UNICODE)
    stem = re.sub(r"_+", "_", stem).strip("_")
    return stem or "document"


def ensure_clean_dirs(reset: bool) -> None:
    if reset and CLEAN_DIR.exists():
        # Keep folder READMEs if present by recreating structure after wipe.
        readme = CLEAN_DIR / "README.md"
        engine_readme = BY_ENGINE_DIR / "README.md"
        readme_text = readme.read_text(encoding="utf-8") if readme.exists() else None
        engine_readme_text = (
            engine_readme.read_text(encoding="utf-8") if engine_readme.exists() else None
        )
        shutil.rmtree(CLEAN_DIR)
        CLEAN_DIR.mkdir(parents=True, exist_ok=True)
        BY_ENGINE_DIR.mkdir(parents=True, exist_ok=True)
        if readme_text is not None:
            readme.write_text(readme_text, encoding="utf-8")
        if engine_readme_text is not None:
            engine_readme.write_text(engine_readme_text, encoding="utf-8")
    else:
        CLEAN_DIR.mkdir(parents=True, exist_ok=True)
        BY_ENGINE_DIR.mkdir(parents=True, exist_ok=True)


def ocr_page(page: fitz.Page) -> str:
    try:
        import pytesseract
        from PIL import Image
    except ImportError:
        return ""

    try:
        pix = page.get_pixmap(matrix=fitz.Matrix(2, 2), alpha=False)
        image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        return pytesseract.image_to_string(image) or ""
    except Exception as exc:  # noqa: BLE001
        print(f"  OCR failed on page {page.number + 1}: {exc}")
        return ""


def _blocks_to_reading_order(page: fitz.Page) -> str:
    """Sort text blocks left-column then right-column for two-column pages."""
    blocks = page.get_text("dict").get("blocks", [])
    text_blocks = []
    for block in blocks:
        if block.get("type") != 0:
            continue
        bbox = block.get("bbox") or [0, 0, 0, 0]
        lines = []
        for line in block.get("lines", []):
            spans = "".join(span.get("text", "") for span in line.get("spans", []))
            if spans.strip():
                lines.append(spans)
        content = "\n".join(lines).strip()
        if content:
            x0, y0, x1, y1 = bbox
            text_blocks.append({"x0": x0, "y0": y0, "x1": x1, "text": content})

    if not text_blocks:
        return ""

    page_mid = page.rect.width / 2
    left = [b for b in text_blocks if ((b["x0"] + b["x1"]) / 2) < page_mid]
    right = [b for b in text_blocks if ((b["x0"] + b["x1"]) / 2) >= page_mid]
    left.sort(key=lambda b: b["y0"])
    right.sort(key=lambda b: b["y0"])
    ordered = left + right
    return "\n\n".join(b["text"] for b in ordered)


def extract_with_pymupdf(pdf_path: Path) -> tuple[str, list[str]]:
    doc = fitz.open(pdf_path)
    pages: list[str] = []
    for page in doc:
        text = _blocks_to_reading_order(page).strip()
        if len(text) < MIN_TEXT_CHARS:
            simple = (page.get_text("text") or "").strip()
            if len(simple) > len(text):
                text = simple
        if len(text) < MIN_TEXT_CHARS:
            ocr_text = ocr_page(page).strip()
            if len(ocr_text) > len(text):
                text = ocr_text
        pages.append(text)
    doc.close()

    parts = [f"## Page {idx}\n\n{page_text.strip()}\n" for idx, page_text in enumerate(pages, start=1)]
    return "\n".join(parts).strip() + "\n", pages


def write_text_pdf(pages: list[str], out_pdf: Path) -> None:
    out = fitz.open()
    for page_text in pages:
        page = out.new_page(width=595, height=842)
        rect = fitz.Rect(40, 40, 555, 802)
        # insert_textbox truncates if too long; split roughly for long pages.
        text = page_text or " "
        chunk_size = 3500
        if len(text) <= chunk_size:
            page.insert_textbox(rect, text, fontsize=10, fontname="helv")
        else:
            page.insert_textbox(rect, text[:chunk_size], fontsize=10, fontname="helv")
            remaining = text[chunk_size:]
            while remaining:
                page = out.new_page(width=595, height=842)
                page.insert_textbox(rect, remaining[:chunk_size], fontsize=10, fontname="helv")
                remaining = remaining[chunk_size:]
    out.save(out_pdf)
    out.close()


def extract_with_docling(pdf_path: Path) -> str | None:
    try:
        from docling.document_converter import DocumentConverter
    except ImportError:
        print("  docling not installed — skipping (pip install docling)")
        return None

    try:
        converter = DocumentConverter()
        result = converter.convert(str(pdf_path))
        if hasattr(result.document, "export_to_markdown"):
            return result.document.export_to_markdown()
        if hasattr(result, "render_as_markdown"):
            return result.render_as_markdown()
        return str(result.document)
    except Exception as exc:  # noqa: BLE001
        print(f"  docling failed: {exc}")
        return None


def extract_with_marker(pdf_path: Path) -> str | None:
    try:
        from marker.converters.pdf import PdfConverter
        from marker.models import create_model_dict
        from marker.output import text_from_rendered
    except ImportError:
        print("  marker not installed — skipping (pip install marker-pdf)")
        return None

    try:
        converter = PdfConverter(artifact_dict=create_model_dict())
        rendered = converter(str(pdf_path))
        text, _, _ = text_from_rendered(rendered)
        return text
    except Exception as exc:  # noqa: BLE001
        print(f"  marker failed: {exc}")
        return None


def extract_with_unstructured(pdf_path: Path) -> str | None:
    try:
        from unstructured.partition.pdf import partition_pdf
    except ImportError:
        print("  unstructured not installed — skipping (pip install 'unstructured[pdf]')")
        return None

    try:
        elements = partition_pdf(filename=str(pdf_path), strategy="hi_res")
        return "\n\n".join(str(el).strip() for el in elements if str(el).strip())
    except Exception as exc:  # noqa: BLE001
        print(f"  unstructured failed: {exc}")
        return None


def write_engine_output(engine: str, stem: str, content: str) -> Path:
    engine_dir = BY_ENGINE_DIR / engine
    engine_dir.mkdir(parents=True, exist_ok=True)
    out = engine_dir / f"{stem}.md"
    out.write_text(content.strip() + "\n", encoding="utf-8")
    return out


def choose_primary_markdown(candidates: dict[str, str]) -> tuple[str, str]:
    preferred_order = ["docling", "marker", "unstructured", "pymupdf"]
    for name in preferred_order:
        text = candidates.get(name, "").strip()
        if len(text) >= MIN_USEFUL_CHARS:
            return name, text
    best_name = max(candidates, key=lambda k: len(candidates[k]))
    return best_name, candidates[best_name]


def strip_bibliography(text: str) -> str:
    lines = text.splitlines()
    cut_at = None
    for i, line in enumerate(lines):
        if REF_HEADING_RE.match(line.strip()):
            cut_at = i
    if cut_at is None:
        return text
    # If Acknowledgements/Appendix appear after References heading, still cut at References.
    return "\n".join(lines[:cut_at]).rstrip() + "\n"


def strip_intext_citations(text: str) -> str:
    text = PAREN_AUTHOR_YEAR_RE.sub("", text)
    text = NUMERIC_BRACKET_RE.sub("", text)
    text = MULTI_SPACE_RE.sub(" ", text)
    text = re.sub(r"\s+([,.;:])", r"\1", text)
    return text


def strip_light_noise(text: str) -> str:
    cleaned_lines = []
    for line in text.splitlines():
        stripped = line.strip()
        if re.fullmatch(r"https?://doi\.org/\S+", stripped, flags=re.I):
            continue
        if re.fullmatch(r"doi:\s*\S+", stripped, flags=re.I):
            continue
        if re.search(r"downloaded from", stripped, flags=re.I) and len(stripped) < 120:
            continue
        cleaned_lines.append(line)
    return "\n".join(cleaned_lines)


def clean_text_for_embedding(text: str, strip_references: bool) -> str:
    if not strip_references:
        return text.strip() + "\n"
    text = strip_bibliography(text)
    text = strip_intext_citations(text)
    text = strip_light_noise(text)
    return text.strip() + "\n"


def pages_from_markdown(md: str) -> list[str]:
    parts = re.split(r"(?im)^##\s+Page\s+\d+\s*$", md)
    pages = [p.strip() for p in parts if p.strip()]
    return pages or [md]


def clean_one(
    pdf_path: Path,
    engines: set[str],
    strip_references: bool,
    warn_layout: bool = True,
) -> None:
    stem = slugify_stem(pdf_path)
    print(f"\nCleaning: {pdf_path.name}")
    candidates: dict[str, str] = {}
    page_texts: list[str] = []

    if "pymupdf" in engines:
        md, page_texts = extract_with_pymupdf(pdf_path)
        candidates["pymupdf"] = md
        write_engine_output("pymupdf", stem, md)
        print(f"  pymupdf: {len(md)} chars")

    if "docling" in engines or "docline" in engines:
        md = extract_with_docling(pdf_path)
        if md:
            candidates["docling"] = md
            write_engine_output("docling", stem, md)
            print(f"  docling: {len(md)} chars")

    if "marker" in engines:
        md = extract_with_marker(pdf_path)
        if md:
            candidates["marker"] = md
            write_engine_output("marker", stem, md)
            print(f"  marker: {len(md)} chars")

    if "unstructured" in engines:
        md = extract_with_unstructured(pdf_path)
        if md:
            candidates["unstructured"] = md
            write_engine_output("unstructured", stem, md)
            print(f"  unstructured: {len(md)} chars")

    if not candidates:
        raise RuntimeError(f"No extraction engine produced output for {pdf_path.name}")

    winner, primary = choose_primary_markdown(candidates)
    layout_engines_requested = bool(engines & {"docling", "docline", "marker", "unstructured"})
    if (
        warn_layout
        and layout_engines_requested
        and winner == "pymupdf"
        and not any(k in candidates for k in ("docling", "marker"))
    ):
        print(
            "  WARNING: layout engines were requested but only pymupdf succeeded. "
            "IEEE two-column order may be imperfect."
        )

    cleaned = clean_text_for_embedding(primary, strip_references=strip_references)
    primary_md = CLEAN_DIR / f"{stem}.md"
    primary_md.write_text(cleaned, encoding="utf-8")
    print(f"  primary markdown: {primary_md.name} (from {winner}, strip_refs={strip_references})")

    if not page_texts:
        page_texts = pages_from_markdown(cleaned)
    else:
        # Apply the same stripping to page texts used for cleaned PDF.
        page_texts = [
            clean_text_for_embedding(p, strip_references=strip_references).strip() for p in page_texts
        ]

    primary_pdf = CLEAN_DIR / f"{stem}.pdf"
    write_text_pdf(page_texts, primary_pdf)
    print(f"  cleaned PDF: {primary_pdf.name}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Clean raw PDFs into cleaned_data/")
    parser.add_argument(
        "--engines",
        default="pymupdf,docling,unstructured,marker",
        help="Comma-separated engines: pymupdf,docling,docline,marker,unstructured",
    )
    parser.add_argument(
        "--reset",
        action="store_true",
        help="Delete cleaned_data/ outputs before writing new ones",
    )
    parser.add_argument(
        "--strip-references",
        dest="strip_references",
        action="store_true",
        default=True,
        help="Strip bibliography and in-text citations (default: on)",
    )
    parser.add_argument(
        "--keep-references",
        dest="strip_references",
        action="store_false",
        help="Keep references/citations (for non-paper guides)",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    engines = {e.strip().lower() for e in args.engines.split(",") if e.strip()}
    ensure_clean_dirs(reset=args.reset)
    pdfs = list_raw_pdfs()
    print(f"Found {len(pdfs)} raw PDF(s) in {RAW_DIR}")
    print(f"Engines requested: {', '.join(sorted(engines))}")
    print(f"Strip references: {args.strip_references}")

    for pdf in tqdm(pdfs, desc="Cleaning PDFs"):
        clean_one(pdf, engines, strip_references=args.strip_references)

    print(f"\nDone. Cleaned {len(pdfs)}/{len(pdfs)} PDFs (100%).")
    print(f"Outputs: {CLEAN_DIR.resolve()}")
    print("Next: python chroma_vector.py")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(130)
