import streamlit as st
from pathlib import Path
import llama_index
from llama_index import download_loader, GPTSimpleVectorIndex, Document
import os

GoogleDriveReader = download_loader("GoogleDriveReader")

web_dir = Path("Web")
web_dir.mkdir(exist_ok=True)

# Create directory if it doesn't exist
# Streamlit app code
st.title("Chat with Knowledge from Google Drive Content")

with st.expander("Input Google Drive folder or file IDs"):

    # Input field for the folder or file IDs to be loaded in the data
    id_input = st.text_input("Enter the Google Drive folder or file IDs to load data from")
    id_type = st.radio("ID type", ["Folder", "File"])
    load_data = st.button("Load data")

    if load_data:
        loader = GoogleDriveReader()

        if id_type == "Folder":
            documents = loader.load_data(folder_id=id_input)
        else:
            documents = loader.load_data(file_ids=[id_input])

        st.success(f"Data loaded successfully!")

        index = GPTSimpleVectorIndex.from_documents(documents)
        index.save_to_disk(f"data.json")

try:
    index = GPTSimpleVectorIndex.load_from_disk(f"data.json")
except FileNotFoundError:
    st.warning("No data files found. Please enter a Google Drive folder or file ID above and click 'Load data' to index its contents.")

inp = st.text_input("Ask question")
ask = st.button("Submit")

if ask:
    res = index.query(inp)
    st.write(res)
