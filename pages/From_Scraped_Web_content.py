import streamlit as st
from pathlib import Path
import llama_index
from llama_index import download_loader, GPTSimpleVectorIndex, Document
import os

AudioTranscriber = download_loader("AudioTranscriber")
BeautifulSoupWebReader = download_loader("BeautifulSoupWebReader")

web_dir = Path("Web")
web_dir.mkdir(exist_ok=True)

# Create directory if it doesn't exist
# Streamlit app code
st.title("Chat with Knowledge from Scraped Web Content")

with st.expander("Input URL"):

# Input field for the URL to be loaded in the data
    url_input = st.text_input("Enter the URL to be scraped")
    scrape_url = st.button("Scrape URL")

    if scrape_url:
        loader = BeautifulSoupWebReader()
        documents = loader.load_data(urls=[url_input])
        st.success(f"URL content scraped successfully!")

        index = GPTSimpleVectorIndex.from_documents(documents)
        # name = web_dir / url_input
        index.save_to_disk(f"url.json")
 
    # b ir / selected_index_file
index = GPTSimpleVectorIndex.load_from_disk(f"url.json")

    # except NameError:
    #     st.warning("No index files found, Input a URL above and Scrape content to index the website.")

inp = st.text_input("Ask question")
ask = st.button("Submit")

if ask:
    res = index.query(inp)
    st.write(res)
    pass
