import streamlit as st

from pdf_processor import extract_pages, chunk_pages
from vector_store import add_chunks, reset, list_sources
from rag import answer

st.set_page_config(page_title="ResearchMate", page_icon="📄")
st.title("📄 ResearchMate")

with st.sidebar:
    st.header("Papers")
    files = st.file_uploader("Upload PDF(s)", type="pdf", accept_multiple_files=True)
    if st.button("Index papers") and files:
        with st.spinner("Indexing..."):
            for f in files:
                add_chunks(chunk_pages(extract_pages(f), f.name))
        st.success(f"Indexed {len(files)} paper(s)")
    if st.button("Clear all"):
        reset()
        st.info("Index cleared")

    indexed = list_sources()
    if indexed:
        st.subheader("Indexed")
        for name in indexed:
            st.caption(f"• {name}")

    st.divider()
    simple = st.toggle("Explain like I'm new to this", value=False)

question = st.text_input("Ask a question about your papers")
if question:
    with st.spinner("Thinking..."):
        reply, hits = answer(question, simple=simple)
    st.markdown(reply)
    with st.expander("Sources used"):
        for h in hits:
            st.caption(
                f"{h['source']} | page {h['page']} | {h['section']} | score {h['score']}"
            )
            st.write(h["text"][:400] + "...")
