"""
Endometriosis Health Guidance Chatbot — Streamlit UI.

Retrieval: local ChromaDB (built by chroma_vector.py from cleaned_data/)
Embeddings: FastEmbed (ONNX, no PyTorch)
LLM: local Ollama (default gemma3:1b)
"""

from __future__ import annotations

import os
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

try:
    from langchain_chroma import Chroma
except ImportError:  # pragma: no cover
    from langchain_community.vectorstores import Chroma

from llm_router import invoke_llm

load_dotenv()

CHROMA_DIR = Path("chroma_db")
COLLECTION_NAME = "endometriosis"
EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
TOP_K = 4
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "gemma3:1b")

SYSTEM_PROMPT_TEMPLATE = """
Your name is Endometriosis Health Guidance Chatbot. You are a health advisor specializing in Endometriosis.
Answer questions very briefly and accurately.
Use the following retrieved knowledge-base information to answer the user's question.
If the context is insufficient, say you are not sure and suggest consulting a healthcare professional.

Important response rules:
- Give a direct answer only.
- Do NOT mention sources, documents, PDFs, pages, citations, references, or that you used retrieved context.
- Do NOT include phrases like "according to the document", "based on the source", or "[Source ...]".
- Do not invent medical claims beyond the context.

Context (for your use only; never cite it aloud):
{doc_content}
"""


@st.cache_resource(show_spinner="Loading knowledge base...")
def load_vectorstore() -> Chroma:
    if not CHROMA_DIR.exists():
        raise FileNotFoundError(
            f"Chroma directory not found: {CHROMA_DIR.resolve()}. "
            "Run: python clean_documents.py --reset --engines pymupdf && python chroma_vector.py"
        )

    embeddings = FastEmbedEmbeddings(model_name=EMBED_MODEL)
    store = Chroma(
        persist_directory=str(CHROMA_DIR),
        embedding_function=embeddings,
        collection_name=COLLECTION_NAME,
    )
    try:
        count = store._collection.count()  # noqa: SLF001
    except Exception:
        count = None
    if count == 0:
        raise RuntimeError(
            "Chroma collection is empty. Run: python chroma_vector.py after cleaning PDFs."
        )
    return store


def format_docs(docs) -> str:
    """Join retrieved chunk text only (no source labels for the LLM)."""
    parts = [doc.page_content.strip() for doc in docs if doc.page_content.strip()]
    return "\n\n".join(parts) if parts else "No additional information found."


def generate_response(question: str, vectorstore: Chroma) -> str:
    """Retrieve from Chroma and answer via local Ollama."""
    docs = vectorstore.similarity_search(question, k=TOP_K)

    print("\n" + "=" * 50)
    print(f"RETRIEVED DOCUMENTS FOR: '{question}'")
    for i, doc in enumerate(docs, start=1):
        print(f"\nDOCUMENT {i} ({doc.metadata.get('source', '?')}):\n{doc.page_content}\n")
    print("=" * 50 + "\n")

    doc_content = format_docs(docs).replace("{", "{{").replace("}", "}}")
    system_text = SYSTEM_PROMPT_TEMPLATE.format(doc_content=doc_content)

    history_messages = []
    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            history_messages.append(HumanMessage(content=msg["content"]))
        elif msg["role"] == "assistant":
            history_messages.append(AIMessage(content=msg["content"]))

    prompt = ChatPromptTemplate.from_messages(
        [
            SystemMessage(content=system_text),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{question}"),
        ]
    )
    prompt_value = prompt.invoke({"chat_history": history_messages, "question": question})
    answer, _provider = invoke_llm(prompt_value)
    return answer


# --- Streamlit UI ---
st.title("Endometriosis Health Guidance Assistant")
st.write(
    "Ask endometriosis-related health questions. Answers are grounded in the local "
    "cleaned PDF knowledge base (ChromaDB) and generated locally with Ollama."
)

try:
    vectorstore = load_vectorstore()
except Exception as exc:
    st.error(str(exc))
    st.stop()

st.caption(
    f"Retrieval: Chroma `{COLLECTION_NAME}` · Embeddings: FastEmbed · "
    f"LLM: Ollama `{OLLAMA_MODEL}` (local)"
)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {
            "role": "assistant",
            "content": (
                "Hello! I'm your Endometriosis Health Guidance Assistant. "
                "How can I assist you today?"
            ),
        }
    ]

for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

user_input = st.chat_input("Ask your health question:")
if user_input:
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.chat_history.append({"role": "user", "content": user_input})

    with st.spinner("Thinking..."):
        try:
            response = generate_response(user_input, vectorstore)
        except Exception as exc:
            response = (
                f"Sorry — I could not generate an answer ({exc}). "
                "Check that Chroma is built and that Ollama is running "
                f"(e.g. `ollama pull {OLLAMA_MODEL}` and `ollama serve`)."
            )

    with st.chat_message("assistant"):
        st.markdown(response)
    st.session_state.chat_history.append({"role": "assistant", "content": response})
