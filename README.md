# Endometriosis Health Guidance Chatbot

A local RAG chatbot that answers endometriosis-related health questions using a cleaned PDF knowledge base, ChromaDB for retrieval and Ollama for generation. The interface is built with Streamlit.

This project is open source. You can fork it, expand the knowledge base, change the local model or improve the cleaning and retrieval pipeline.

---

## Origin and credit

This work started from the Tambua Women in Tech chatbot built by **[GRACENGARI](https://github.com/GRACENGARI)**:

- Original repository: [https://github.com/GRACENGARI/TAMBUA-WOMENINTECH-CHATBOT](https://github.com/GRACENGARI/TAMBUA-WOMENINTECH-CHATBOT)

We appreciate Grace and the original contributors for creating a clear beginner-friendly starting point that showed how to connect a medical PDF, a vector store and a Streamlit chat UI. This fork keeps that learning spirit while moving the stack fully local so more people can run and extend it without cloud API lock-in.

---

## What the original project was

The upstream version was an Endometriosis Health Guidance Chatbot that:

- Loaded a single PDF guide
- Chunked text and stored embeddings in **Pinecone**
- Used **Google Gemini** for answers and Google embeddings for vectors
- Served a conversational UI with **Streamlit**
- Needed `PINECONE_API_KEY` and `GOOGLE_API_KEY`

That design worked well as a cloud-backed demo. This fork rebuilds the same product idea for offline-friendly use.

---

## What this fork changes

| Area | Original | This fork |
|------|----------|-----------|
| Vector store | Pinecone (cloud) | **ChromaDB** on disk (`chroma_db/`) |
| Embeddings | Google `embedding-001` | **FastEmbed** (ONNX MiniLM, no PyTorch/CUDA) |
| LLM | Google Gemini | **Ollama** locally (default `gemma3:1b`) |
| Knowledge base | One PDF | Multiple PDFs in `data/pdfs/` |
| Preprocessing | Direct PDF load | `clean_documents.py` cleans text first into `cleaned_data/` |
| Chunking | 1500 / 100 | **500 / 75** (~15% overlap) |
| Ingest script | `pinecone_vector.py` | `chroma_vector.py` |

Other practical changes:

- Flat `data/pdfs/` drop zone for guides and research papers
- Reference and citation stripping for research PDFs
- Column-aware PyMuPDF reading-order heuristic for split-page layouts
- Answers are brief and do not mention document sources to the user
- Secrets stay in `.env` (gitignored). Use `.env.example` as a template

---

## Project layout

```text
.
├── data/pdfs/              # Put raw PDFs here
├── cleaned_data/           # Cleaned .md / .pdf from the cleaner
├── chroma_db/              # Local Chroma index (generated)
├── clean_documents.py      # PDF cleaning pipeline
├── chroma_vector.py        # Embed cleaned files into Chroma
├── llm_router.py           # Ollama chat helper
├── main.py                 # Streamlit chatbot
├── requirements.txt
├── .env.example
└── README.md
```

Folder READMEs inside `data/pdfs/`, `cleaned_data/` and `chroma_db/` explain each stage in more detail.

---

## Prerequisites

1. **Python 3.10+**
2. **Git**
3. **Ollama** installed and running  
   - Install from [https://ollama.com](https://ollama.com)  
   - Pull the default model: `ollama pull gemma3:1b`
4. Optional for OCR on scanned pages: system package `tesseract-ocr`

---

## Setup

```bash
git clone https://github.com/DanEinstein/-Endometriosis-Health-Guidance-Chatbot.git
cd -Endometriosis-Health-Guidance-Chatbot   # or your local folder name

python3 -m venv venv
source venv/bin/activate                   # Windows: venv\Scripts\activate

pip install --upgrade pip
pip install --default-timeout=1000 -r requirements.txt

cp .env.example .env
# Edit .env if you want a different Ollama model or base URL
```

Example `.env`:

```bash
OLLAMA_MODEL=gemma3:1b
OLLAMA_BASE_URL=http://localhost:11434
```

---

## Add knowledge (PDFs)

1. Place PDF files in `data/pdfs/` (flat folder, clear filenames).
2. Clean them:

```bash
python clean_documents.py --reset --engines pymupdf
```

3. Spot-check one or two files in `cleaned_data/*.md` (reading order looks sane and long References sections are gone).
4. Build the vector index:

```bash
python chroma_vector.py
```

To grow the knowledge base later: add more PDFs to `data/pdfs/`, then re-run clean and `chroma_vector.py`.

---

## Run the chatbot

```bash
# Terminal 1: make sure Ollama is available
ollama serve          # if it is not already running
ollama pull gemma3:1b

# Terminal 2: app
source venv/bin/activate
streamlit run main.py
```

Open the local URL Streamlit prints (usually `http://localhost:8501`).

---

## How a question is answered

1. Your question is embedded with FastEmbed.
2. Chroma returns the top matching chunks from `cleaned_data/`.
3. Ollama writes a short answer using that context.
4. The UI does not show PDF filenames or citation labels to the user.

This is educational guidance grounded in the supplied documents. It is **not** a substitute for professional medical care.

---

## Useful commands

```bash
# Rebuild cleaned text only
python clean_documents.py --reset --engines pymupdf

# Keep bibliographies (rare; mostly for non-paper guides)
python clean_documents.py --reset --engines pymupdf --keep-references

# Rebuild Chroma after cleaning
python chroma_vector.py

# Chat UI
streamlit run main.py
```

---

## Improving the project (open source)

You are welcome to fork and improve this project. Ideas that help the community:

- Add more high-quality endometriosis guides or open-access papers to `data/pdfs/`
- Tune chunk size / overlap or retrieval `k` in `chroma_vector.py` and `main.py`
- Try a stronger Ollama model via `OLLAMA_MODEL` (for example a larger Gemma or Llama build)
- Improve cleaning heuristics for two-column IEEE layouts
- Add evaluation questions and expected answer notes
- Translate the UI or knowledge base for more communities

If you publish improvements please keep credit to the original Tambua / GRACENGARI work and document your changes so others can learn from them.

---

## Troubleshooting

| Issue | What to try |
|-------|-------------|
| Chroma missing / empty | Run `clean_documents.py` then `chroma_vector.py` |
| Ollama errors | Confirm `ollama serve` is running and `ollama pull gemma3:1b` succeeded |
| Slow or timed-out `pip install` | Retry with `pip install --default-timeout=1000 -r requirements.txt` |
| Odd reading order in cleaned text | Inspect `cleaned_data/*.md`. Optional heavier layout tools (Docling/Marker) exist but are not required and may pull large ML stacks |
| Secrets in git | Never commit `.env`. Only `.env.example` should be public |

---

## License and courtesy

Follow the license of the upstream repository and respect the licenses of any PDFs you add. Prefer open-access materials you are allowed to redistribute when you publish a public fork.

**Thanks again to [GRACENGARI](https://github.com/GRACENGARI)** for the original Endometriosis Health Guidance Chatbot that made this local rebuild possible.
