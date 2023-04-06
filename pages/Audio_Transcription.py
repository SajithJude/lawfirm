import os
import streamlit as st
from pathlib import Path
from llama_index import download_loader
AudioTranscriber = download_loader("AudioTranscriber")

# Create directory if it doesn't exist
if not os.path.exists("audio"):
    os.makedirs("audio")

# Get absolute path of "audio" directory
audio_dir = os.path.abspath("audio")

# Streamlit app code
st.title("Audio Uploader")

# Allow user to upload audio file
audio_file = st.file_uploader("Upload audio file", type=["mp3", "wav"])

# Save audio file to "audio" directory
if audio_file is not None:
    file_name = audio_file.name
    file_path = os.path.join("audio", file_name)
    with open(file_path, "wb") as f:
        f.write(audio_file.getbuffer())
    st.success(f"File saved to: {file_path}")

# Show list of available audio files
audio_files = os.listdir("audio")
if len(audio_files) > 0:
    st.write("Available audio files:")
    selected_file = st.selectbox("", audio_files)
    file_path = os.path.join("audio", selected_file)
    st.write(f"File path: {file_path}")
    loader = AudioTranscriber()
    audio = st.audio(file_path)
    st.write(f"Audio directory path: {audio_dir}")
    documents = loader.load_data(file=Path("pages/mypodcast_64kb.mp3"))

else:
    st.warning("No audio files found. Please upload.")

# Show path of "audio" directory

