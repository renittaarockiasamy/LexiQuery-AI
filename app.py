import os
from pathlib import Path
import streamlit as st

# LangChain / HF
from langchain_community.document_loaders import PyPDFLoader, TextLoader, Docx2txtLoader, CSVLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings, HuggingFacePipeline
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from transformers.pipelines import pipeline

# ---------------------------
# Config
# ---------------------------
st.set_page_config(page_title="LexiQuery AI", page_icon="🧠", layout="wide")
st.title("🧠 LexiQuery AI — Multi-format Document Q&A")
st.caption("Upload PDF, DOCX, TXT, or CSV. Ask questions. Get answers grounded in your files.")

SUPPORTED_TYPES = ["pdf", "docx", "txt", "csv"]

# ---------------------------
# Helpers
# ---------------------------
def save_uploaded(uploaded_file) -> Path:
    """Save uploaded file to disk and return its path."""
    uploads_dir = Path("uploads")
    uploads_dir.mkdir(exist_ok=True)
    file_path = uploads_dir / uploaded_file.name
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return file_path

def load_documents(file_path: Path):
    """Load documents using the appropriate loader by file extension."""
    ext = file_path.suffix.lower().replace(".", "")
    if ext == "pdf":
        loader = PyPDFLoader(str(file_path))
    elif ext == "txt":
        # encoding='utf-8' avoids decode errors on plain text
        loader = TextLoader(str(file_path), encoding="utf-8")
    elif ext == "docx":
        loader = Docx2txtLoader(str(file_path))
    elif ext == "csv":
        # CSVLoader turns each row into a Document; good for lightweight QA
        loader = CSVLoader(str(file_path))
    else:
        raise ValueError(f"Unsupported file type: .{ext}")
    return loader.load()

def split_docs(documents, chunk_size=800, chunk_overlap=120):
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    return splitter.split_documents(documents)

@st.cache_resource(show_spinner=False)
def get_embeddings():
    # all-MiniLM-L6-v2 is small, fast, and accurate for semantic search
    return HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

def build_index(chunks):
    embeddings = get_embeddings()
    return FAISS.from_documents(chunks, embeddings)

@st.cache_resource(show_spinner=False)
def get_llm():
    # Small instruction model that runs on CPU. Good for Streamlit Cloud free tier.
    gen = pipeline("text2text-generation", model="google/flan-t5-small")
    return HuggingFacePipeline(pipeline=gen)

def build_qa(vectorstore, k=4):
    retriever = vectorstore.as_retriever(search_kwargs={"k": k})
    llm = get_llm()
    return RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=True,
        chain_type="stuff"
    )

def show_sources(source_docs, max_chars=400):
    with st.expander("📖 Source excerpts"):
        for i, d in enumerate(source_docs, start=1):
            meta = d.metadata.copy()
            src = meta.get("source") or meta.get("file_path") or "uploaded"
            page = meta.get("page", None)
            header = f"Chunk {i} — {src}" + (f" (page {page})" if page is not None else "")
            st.markdown(f"**{header}**")
            st.write(d.page_content[:max_chars] + ("..." if len(d.page_content) > max_chars else ""))

# ---------------------------
# Sidebar (advanced)
# ---------------------------
with st.sidebar:
    st.header("⚙️ Settings")
    chunk_size = st.slider("Chunk size (characters)", 300, 2000, 800, 50)
    chunk_overlap = st.slider("Chunk overlap (characters)", 0, 400, 120, 10)
    top_k = st.slider("Top-k chunks to retrieve", 1, 10, 4, 1)
    st.caption("Tip: Larger chunks and a small overlap often help policy/manual PDFs.")

# ---------------------------
# UI
# ---------------------------
uploaded = st.file_uploader("Upload a document", type=SUPPORTED_TYPES, help="PDF, DOCX, TXT, or CSV")

if uploaded:
    # Save
    file_path = save_uploaded(uploaded)
    st.success(f"✅ Uploaded `{uploaded.name}`")

    # Build index (once per file/settings)
    build_key = (file_path.name, chunk_size, chunk_overlap)
    if "indexes" not in st.session_state:
        st.session_state.indexes = {}

    if build_key not in st.session_state.indexes:
        with st.spinner("🔎 Reading & indexing your document..."):
            try:
                docs = load_documents(file_path)
                chunks = split_docs(docs, chunk_size=chunk_size, chunk_overlap=chunk_overlap)
                vectordb = build_index(chunks)
                st.session_state.indexes[build_key] = {
                    "vectordb": vectordb,
                    "num_chunks": len(chunks)
                }
                st.toast(f"Indexed {len(chunks)} chunks", icon="✅")
            except Exception as e:
                st.error(f"Failed to process file: {e}")
                st.stop()

    vectordb = st.session_state.indexes[build_key]["vectordb"]
    st.info(f"📚 Indexed chunks: {st.session_state.indexes[build_key]['num_chunks']}")

    # Q&A
    query = st.text_input("Ask a question about your document:")
    if query:
        with st.spinner("🤖 Thinking..."):
            qa = build_qa(vectordb, k=top_k)
            result = qa({"query": query})
        st.subheader("🔍 Answer")
        st.write(result["result"])
        show_sources(result.get("source_documents", []))

# Footer note
st.caption("Note: Scanned PDFs (images) need OCR to extract text. This app expects real text inside files.")

