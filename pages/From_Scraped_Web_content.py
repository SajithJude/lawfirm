import streamlit as st
from pathlib import Path
import llama_index
from langchain import OpenAI
from llama_index import download_loader, GPTSimpleVectorIndex, Document,  LLMPredictor, ServiceContext
import os

# AudioTranscriber = download_loader("AudioTranscriber")
BeautifulSoupWebReader = download_loader("BeautifulSoupWebReader")

web_dir = Path("Web")
web_dir.mkdir(exist_ok=True)

if "scrapeIndex" not in st.session_state:
    st.session_state.scrapeIndex = ""
# Create directory if it doesn't exist
# Streamlit app code
st.title("Chat with Knowledge from Scraped Web Content")
st.caption("This app allows users to input a URL from the internet and scrape content from it. The app uses web scraping techniques to extract relevant information from the webpage and can identify and retrieve data such as article titles, text content, and images. Users can then ask custom questions related to the scraped content, and the app will provide them with the answers. The app can also provide users with additional information related to the content, such as the author's name, publication date, or any relevant keywords. The app is designed to make it easy for users to gather information from the internet and quickly find the answers they need.")
with st.expander("Input URL"):

# Input field for the URL to be loaded in the data
    url_input = st.text_input("Enter the URL to be scraped")
    scrape_url = st.button("Scrape URL")

    if scrape_url:
        loader = BeautifulSoupWebReader()
        documents = loader.load_data(urls=[url_input])
        st.success(f"URL content scraped successfully!")
        llm_predictor = LLMPredictor(llm=OpenAI(temperature=0, model_name="text-davinci-003", max_tokens=1024))
        service_context = ServiceContext.from_defaults(llm_predictor=llm_predictor)


        scrapeIndex = GPTSimpleVectorIndex.from_documents(documents, service_context=service_context)
        st.session_state.scrapeIndex = scrapeIndex
        # name = web_dir / url_input
        # index.save_to_disk(f"url.json")
 
    # b ir / selected_index_file

# index = GPTSimpleVectorIndex.load_from_disk(f"url.json", service_context=service_context)
# if index:
#     st.success("Index Loaded from repository successfully")

inp = st.text_input("Ask question")
ask = st.button("Submit")

if ask:
    res = st.session_state.scrapeIndex.query(inp)
    st.write(res)
    pass


if "file_paths" not in st.session_state:
    st.session_state.file_paths = []

# Select directory to download files from
dir_path = st.selectbox("Select directory", os.listdir())
if dir_path:
    # Check if selected path is a directory
    if os.path.isdir(dir_path):
        # Get list of files in directory
        file_names = os.listdir(dir_path)
        file_paths = [os.path.join(dir_path, file_name) for file_name in file_names if file_name.endswith(".txt")]

        if not file_paths:
            st.warning("No .txt files found in directory!")
        else:
            st.success(f"{len(file_paths)} .txt files found in directory.")
            st.session_state.file_paths = file_paths

# Display download button if files are selected
if st.session_state.file_paths:
    download_button = st.button("Download Files")
    if download_button:
        with st.spinner("Downloading..."):
            for file_path in st.session_state.file_paths:
                with open(file_path, "rb") as file:
                    file_content = file.read()
                    st.download_button(label=file_path, data=file_content, file_name=os.path.basename(file_path))