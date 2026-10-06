"""
Build a local ChromaDB index from cleaned_data/ for the endometriosis RAG chatbot.

Replaces the old pinecone_vector.py Pinecone + Google embeddings pipeline.

Usage:
  python clean_documents.py --reset
  python chroma_vector.py
"""

from __future__ import annotations

import shutil
import sys
from pathlib import Path

from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from tqdm import tqdm

try:
    from langchain_chroma import Chroma
except ImportError:  # pragma: no cover - older installs
    from langchain_community.vectorstores import Chroma

from langchain_community.embeddings.fastembed import FastEmbedEmbeddings

CLEAN_DIR = Path("cleaned_data")
RAW_DIR = Path("data/pdfs")
CHROMA_DIR = Path("chroma_db")
COLLECTION_NAME = "endometriosis"
# ONNX via fastembed — no PyTorch / CUDA
EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
CHUNK_SIZE = 500
CHUNK_OVERLAP = 75  # ~15% of 500


def get_embeddings() -> FastEmbedEmbeddings:
    return FastEmbedEmbeddings(model_name=EMBED_MODEL)


def split_docs(documents: list[Document], chunk_size: int = CHUNK_SIZE, chunk_overlap: int = CHUNK_OVERLAP):
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    return splitter.split_documents(documents)


def _is_primary_clean_file(path: Path) -> bool:
    if "by_engine" in path.parts:
        return False
    if path.name.lower() == "readme.md":
        return False
    return path.suffix.lower() in {".md", ".pdf"}


def list_clean_sources() -> list[Path]:
    if not CLEAN_DIR.exists():
        return []
    files = sorted(p for p in CLEAN_DIR.iterdir() if p.is_file() and _is_primary_clean_file(p))
    # Prefer markdown when both .md and .pdf exist for the same stem.
    by_stem: dict[str, Path] = {}
    for path in files:
        stem = path.stem
        existing = by_stem.get(stem)
        if existing is None:
            by_stem[stem] = path
        elif path.suffix.lower() == ".md":
            by_stem[stem] = path
    return sorted(by_stem.values(), key=lambda p: p.name.lower())


def list_raw_pdf_fallback() -> list[Path]:
    if not RAW_DIR.exists():
        return []
    return sorted(p for p in RAW_DIR.glob("*.pdf") if p.is_file())


def load_documents(sources: list[Path], source_kind: str) -> list[Document]:
    documents: list[Document] = []
    for path in tqdm(sources, desc=f"Loading {source_kind}"):
        if path.suffix.lower() == ".md":
            loader = TextLoader(str(path), encoding="utf-8")
            docs = loader.load()
            for doc in docs:
                doc.metadata["source"] = path.name
                doc.metadata.setdefault("page", 0)
            documents.extend(docs)
        elif path.suffix.lower() == ".pdf":
            loader = PyPDFLoader(str(path))
            docs = loader.load()
            for doc in docs:
                doc.metadata["source"] = path.name
                # PyPDFLoader usually sets page already.
                if "page" not in doc.metadata:
                    doc.metadata["page"] = 0
            documents.extend(docs)
        else:
            print(f"Skipping unsupported file: {path}")
    return documents


def reset_chroma_dir() -> None:
    readme = CHROMA_DIR / "README.md"
    readme_text = readme.read_text(encoding="utf-8") if readme.exists() else None
    if CHROMA_DIR.exists():
        shutil.rmtree(CHROMA_DIR)
    CHROMA_DIR.mkdir(parents=True, exist_ok=True)
    if readme_text is not None:
        readme.write_text(readme_text, encoding="utf-8")


def main() -> None:
    load_dotenv()

    sources = list_clean_sources()
    source_kind = "cleaned_data"
    if not sources:
        print(
            f"No primary cleaned files found in {CLEAN_DIR.resolve()}.\n"
            "Looking for temporary fallback in data/pdfs/ ..."
        )
        sources = list_raw_pdf_fallback()
        source_kind = "data/pdfs (fallback)"
        if not sources:
            raise SystemExit(
                "Nothing to index.\n"
                "Run: python clean_documents.py --reset\n"
                f"Expected cleaned files in {CLEAN_DIR.resolve()}"
            )
        print("WARNING: indexing raw PDFs. Prefer running clean_documents.py first.")

    print(f"Indexing {len(sources)} file(s) from {source_kind}")
    for path in sources:
        print(f"  - {path.name}")

    documents = load_documents(sources, source_kind)
    if not documents:
        raise SystemExit("No document text loaded from sources.")

    chunks = split_docs(documents, chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)
    print(f"Split into {len(chunks)} chunks (size={CHUNK_SIZE}, overlap={CHUNK_OVERLAP})")

    # Per-source chunk counts for visibility
    counts: dict[str, int] = {}
    for chunk in chunks:
        src = chunk.metadata.get("source", "unknown")
        counts[src] = counts.get(src, 0) + 1
    for src, count in sorted(counts.items()):
        print(f"  {src}: {count} chunks")

    print(f"\nBuilding Chroma collection '{COLLECTION_NAME}' in {CHROMA_DIR.resolve()} ...")
    reset_chroma_dir()
    embeddings = get_embeddings()
    Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=str(CHROMA_DIR),
        collection_name=COLLECTION_NAME,
    )
    print("\nChroma vector storage complete!")
    print(f"Persist directory: {CHROMA_DIR.resolve()}")
    print("Next: streamlit run main.py  (after main.py is updated for Chroma)")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(130)
