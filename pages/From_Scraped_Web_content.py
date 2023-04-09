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


        index = GPTSimpleVectorIndex.from_documents(documents, service_context=service_context)
        # name = web_dir / url_input
        index.save_to_disk(f"url.json")
 
    # b ir / selected_index_file
llm_predictor = LLMPredictor(llm=OpenAI(temperature=0, model_name="text-davinci-003", max_tokens=1024))
service_context = ServiceContext.from_defaults(llm_predictor=llm_predictor)

index = GPTSimpleVectorIndex.load_from_disk(f"url.json", service_context=service_context)
if index:
    st.success("Index Loaded from repository successfully")

inp = st.text_input("Ask question")
ask = st.button("Submit")

if ask:
    res = index.query(inp)
    st.write(res)
    pass
