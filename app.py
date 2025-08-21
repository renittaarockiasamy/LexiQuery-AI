

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
chunks = split_docs(
docs, chunk_size=chunk_size, chunk_overlap=chunk_overlap
)
vectordb = build_index(chunks)
st.session_state.indexes[build_key] = {
"vectordb": vectordb,
"num_chunks": len(chunks),
}
st.toast(f"Indexed {len(chunks)} chunks", icon="✅")
except Exception as e:
st.error(f"Failed to process file: {e}")
st.stop()


vectordb = st.session_state.indexes[build_key]["vectordb"]
st.info(
f"📚 Indexed chunks: {st.session_state.indexes[build_key]['num_chunks']} | Retrieval: {search_type.upper()} | Embeddings: all-mpnet-base-v2 | LLM: flan-t5-base"
)


# Q&A
query = st.text_input("Ask a question about your document:")
if query:
with st.spinner("🤖 Thinking..."):
qa = build_qa(vectordb, k=top_k, search_type=search_type)
result = qa({"query": query})
st.subheader("🔍 Answer")
st.write(result["result"]) # model's final answer
show_sources(result.get("source_documents", []))


# Footer note
st.caption(
"Note: Scanned PDFs (images) need OCR to extract text. This app expects real text inside files."
)
