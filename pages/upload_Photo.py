import streamlit as st
from pathlib import Path
from llama_index import download_loader, GPTSimpleVectorIndex, SimpleDirectoryReader
import os

st.set_option('deprecation.showfileUploaderEncoding', False)

# Title
st.title("WhatsApp Chat Analyzer")

# File uploader
uploaded_file = st.file_uploader("Upload your WhatsApp chat .txt file", type="txt")

if uploaded_file is not None:
    # Check if "whatsapp" directory exists, and create it if it doesn't
    data_dir = Path("whatsapp")
    if not data_dir.exists():
        data_dir.mkdir()

    # Save the uploaded file to the "whatsapp" directory
    data_path = data_dir / uploaded_file.name
    with open(data_path, "wb") as f:
        f.write(uploaded_file.getvalue())

    # Load and process the data
    documents = SimpleDirectoryReader(str(data_dir)).load_data()

    # Create an index from the text directory
    text_dir = Path("text")
    if text_dir.exists():
        index_path = text_dir / "index"
        if not index_path.exists():
            intax = GPTSimpleVectorIndex.from_documents(documents)
            intax.save(str(index_path))
            st.write("Index created for text directory")

        else:
            intax = download_loader(str(index_path))
            st.write("Index loaded from file")

    else:
        st.warning("Directory 'text' not found. Please save OCR output text files to 'text' directory.")

else:
    st.warning("Please upload a .txt file to analyze WhatsApp chats.")

inp = st.text_input("Input a query")
send = st.button("Submit")
clear = st.button("Clear session state")

if send:
    if "intax" not in st.session_state:
        st.error("Index not found. Please upload a text file and create an index first.")
    else:
        resp = st.session_state.intax.query(inp)
        st.write(resp.response)

if clear:
    if "intax" in st.session_state:
        del st.session_state.intax
        st.success("Session state cleared.")
    else:
        st.warning("Session state already empty.")
