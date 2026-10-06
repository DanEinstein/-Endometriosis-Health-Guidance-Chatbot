# Cleaned data (do not drop raw PDFs here)

This folder will hold **cleaned** outputs produced by `clean_documents.py`:

- `*.md` — primary text used for embedding
- `*.pdf` — text-layer cleaned PDFs
- `by_engine/` — per-engine extracts for comparison

Leave this empty until the cleaning script runs. Collect new sources under `data/pdfs/` instead.
