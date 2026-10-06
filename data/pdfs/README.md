# Raw PDF drop zone

Put **all** source PDFs for the RAG knowledge base directly in this folder:

- Patient guides / clinical handbooks
- Research papers / journal articles
- Any other endometriosis-related PDFs

No subfolders required. Use clear filenames, e.g. `endo_pain_review_2023.pdf`.

**Do not** put cleaned files here — cleaning writes to `../../cleaned_data/`.

**After you add PDFs**
1. Run the cleaner → `cleaned_data/`
2. Run Chroma ingest → `chroma_db/`
3. Start the Streamlit chat app
