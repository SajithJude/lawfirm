import streamlit as st
from pathlib import Path
import llama_index
from llama_index import download_loader, GPTSimpleVectorIndex, Document
import os
AudioTranscriber = download_loader("AudioTranscriber")
import sys
import subprocess

# Create directory if it doesn't exist
audio_dir = Path("audio")
audio_dir.mkdir(exist_ok=True)

# Streamlit app code
st.title("Query Audio Files")

with st.expander("Upload Audio"):
    # Allow user to upload audio file
    audio_file = st.file_uploader("Upload audio file", type=["mp3", "wav"])

    # Save audio file to "audio" directory
    if audio_file is not None:
        file_name = audio_file.name
        file_path = audio_dir / file_name
        with open(file_path, "wb") as f:
            f.write(audio_file.getbuffer())
        st.success(f"File saved to: {file_path}")

    # Show list of available audio files
    audio_files = [file.name for file in audio_dir.glob("*")]
    if len(audio_files) > 0:
        st.write("Available audio files:")
        selected_file = st.selectbox("", audio_files)
        create = st.button("Create index")
        if create:
            file_path = audio_dir / selected_file
            st.write(f"File path: {file_path}")
            loader = AudioTranscriber()
            audio = st.audio(f"{file_path}")
            pat = Path(f"{str(file_path)}")
            # st.write(pat.name)
            # Transcribe audio file
            documents = loader.load_data(file=pat)
            index = GPTSimpleVectorIndex.from_documents(documents)
            index_file_path = audio_dir / f"{selected_file}.json"
                
                # Save the index to the data directory with the same name as the PDF
            index.save_to_disk(index_file_path)
        st.success(f"{selected_file} 's Index created successfully!")
    else:
        st.warning("No audio files found. Please upload.")

try:
    index_files = [file.name for file in audio_dir.glob(f"{selected_file}.json")]
    # len(index_files) > 0:
    # st.write("Select an indexed Audio To ask questions:")
    selected_index_file = st.selectbox("Select An Audio Index to ask questions ", index_files)
    index_file_path = audio_dir / selected_index_file
    # st.write(f"Index file path: {index_file_path}")
    index = GPTSimpleVectorIndex.load_from_disk(index_file_path)
    # st.success("index loaded")
except NameError:
    st.warning("No index files found for this audio file. Please transcribe the audio file first.")

inp = st.text_input("ask question")
ask = st.button("submit")
if ask:
    res = index.query(inp)
    st.write(res)
    pass

# Show path of "audio" directory
# st.write(f"Audio directory path: {audio_dir}")



