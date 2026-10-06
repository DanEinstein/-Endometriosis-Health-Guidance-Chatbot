# cleaned_data — cleaned knowledge text

Outputs from `clean_documents.py`. These files (not the raw PDFs) are what get embedded into Chroma.

## What belongs here

| Item | Purpose |
|------|---------|
| `*.md` | Primary cleaned text used by `chroma_vector.py` |
| `*.pdf` | Text-layer cleaned PDFs (fallback / inspection) |
| `by_engine/` | Per-engine extracts for quality comparison |

## How to produce it

```bash
# Put raw PDFs in data/pdfs/ first, then:
python clean_documents.py --reset --engines pymupdf
```

Cleaning applies (by default):

- PyMuPDF extract with left→right column reading-order heuristic
- Strip References / Bibliography blocks
- Strip common in-text citations
- Light noise removal (DOI-only lines, download banners)

Use `--keep-references` if you need to keep bibliographies for a specific run.

## Rules

- Do **not** drop raw research PDFs here — use `data/pdfs/`.
- Generated `.md` / `.pdf` files are gitignored (READMEs are kept).
- Spot-check a cleaned `.md` (order + no long References dump) before indexing.

## Next step

```bash
python chroma_vector.py
```
