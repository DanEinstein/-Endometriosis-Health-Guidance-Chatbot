# by_engine — extraction comparison copies

Filled automatically by `clean_documents.py` when an engine runs.

Typical subfolders:

- `pymupdf/` — always available in the lightweight stack
- `docling/`, `marker/`, `unstructured/` — only if those optional packages are installed

These files are for **comparing extract quality**.  
`chroma_vector.py` does **not** read this folder; it uses the primary files in `cleaned_data/`.
