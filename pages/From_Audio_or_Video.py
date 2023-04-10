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

if "audioIndex" not in st.session_state:
    st.session_state.audioIndex = ""
# Streamlit app code
st.title("Query Audio/Video Files")
st.caption("This app enables users to upload audio/Video files, and Users can then ask custom questions related to the audio's content, and the app will provide them with the answers. The app can also identify and extract relevant information from the audio, such as names, dates, or locations, summaries, key points to provide more accurate answers. The app is designed to make it easy for users to gather information from audio content and quickly find the answers they need.")

with st.expander("Upload Audio/Video"):
    # Allow user to upload audio file
    audio_file = st.file_uploader("Upload audio/Video file", type=["mp3", "wav","mp4"])

    # Save audio file to "audio" directory
    if audio_file is not None:
        file_name = audio_file.name
        file_path = audio_dir / file_name
        with open(file_path, "wb") as f:
            f.write(audio_file.getbuffer())
        st.success(f"File saved to: {file_path}")

        # Create index directly from uploaded file
        loader = AudioTranscriber()
        audio = st.audio(f"{file_path}")
        pat = Path(f"{str(file_path)}")
        documents = loader.load_data(file=pat)
        audioIndex = GPTSimpleVectorIndex.from_documents(documents)
        st.session_state.audioIndex = audioIndex

        # index_file_path = audio_dir / f"{file_name}.json"

        # # Save the index to the data directory with the same name as the PDF
        # index.save_to_disk(index_file_path)
        # st.success(f"{file_name} 's Index created successfully!")
    else:
        st.warning("No audio files found. Please upload.")

# try:
#     index_files = [file.name for file in audio_dir.glob(f"{file_name}.json")]
#     selected_index_file = index_files[0]  # Select the first index file
#     index_file_path = audio_dir / selected_index_file
#     index = GPTSimpleVectorIndex.load_from_disk(index_file_path)
# except (NameError, IndexError):
#     st.warning("No index files found for this audio file. Please transcribe the audio file first.")

inp = st.text_input("ask question")
ask = st.button("submit")
if ask:
    res = st.session_state.audioIndex.query(inp)
    st.write(res.response)
