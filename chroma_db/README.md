# chroma_db — local vector store

This folder holds the **ChromaDB** index used by `main.py` for retrieval.

## How it is created

```bash
# 1) Clean raw PDFs first
python clean_documents.py --reset --engines pymupdf

# 2) Build / rebuild this index from cleaned_data/
python chroma_vector.py
```

## Details

| Setting | Value |
|--------|--------|
| Collection name | `endometriosis` |
| Source files | `cleaned_data/*.md` (preferred) or `cleaned_data/*.pdf` |
| Chunk size / overlap | 500 / 75 (~15%) |
| Embeddings | FastEmbed (`sentence-transformers/all-MiniLM-L6-v2`, ONNX — no PyTorch) |

## Rules

- Do **not** put raw PDFs here.
- Index files under this folder are **generated** and gitignored (only this README is tracked).
- After adding or changing knowledge PDFs: re-run clean → `python chroma_vector.py`.
- Safe to delete the generated DB files and rebuild anytime.

## Used by

`streamlit run main.py` loads this store and answers with local **Ollama**.
