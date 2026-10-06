# data/pdfs — raw source PDFs

Drop **all** knowledge-base PDFs here (flat folder):

- Patient guides / clinical handbooks
- Research papers / journal articles
- Other endometriosis-related PDFs

Use clear filenames, e.g. `endo_pain_review_2023.pdf`.

## Rules

- This is the **raw** drop zone only.
- Do not put cleaned files here — cleaning writes to `cleaned_data/`.
- No category subfolders required.

## Pipeline after adding PDFs

```bash
python clean_documents.py --reset --engines pymupdf
python chroma_vector.py
streamlit run main.py
```

Chat answers use local Chroma retrieval + **Ollama** (see project `.env.example`).
