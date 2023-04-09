import streamlit as st
from pathlib import Path
import llama_index
from llama_index import download_loader, GPTSimpleVectorIndex, Document
import os

AudioTranscriber = download_loader("AudioTranscriber")

# Replace the web scraper with PPTX upload functionality
PptxReader = download_loader("PptxReader")

web_dir = Path("Web")
web_dir.mkdir(exist_ok=True)

# Streamlit app code
st.title("Chat with Knowledge from Uploaded PPTX Content")

with st.expander("Upload PPTX"):
    # Upload field for the PPTX file
    pptx_file = st.file_uploader("Upload a PPTX file")

    # Button to initiate the PPTX upload process
    upload_pptx = st.button("Upload PPTX")

    if upload_pptx:
        if pptx_file is not None:
            loader = PptxReader()
            documents = loader.load_data(file=pptx_file)
            st.success(f"PPTX content uploaded successfully!")
            
            index = GPTSimpleVectorIndex.from_documents(documents)
            index.save_to_disk(f"pptx.json")

inp = st.text_input("Ask question")
ask = st.button("Submit")

if ask:
    # Load the index file from disk if it exists
    if os.path.isfile(f"pptx.json"):
        index = GPTSimpleVectorIndex.load_from_disk(f"pptx.json")
        res = index.query(inp)
        st.write(res)
    else:
        st.warning("No index files found. Please upload a PPTX file above and wait for it to finish processing to create the index.")
