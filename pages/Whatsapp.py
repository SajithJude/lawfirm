import streamlit as st
from pathlib import Path
from llama_index import download_loader, GPTSimpleVectorIndex
from tempfile import NamedTemporaryFile

st.set_option('deprecation.showfileUploaderEncoding', False)

# Title
st.title("WhatsApp Chat Analyzer")

# File uploader
uploaded_file = st.file_uploader("Upload your WhatsApp chat .txt file", type="txt")

if uploaded_file is not None:
    with NamedTemporaryFile(delete=False, suffix=".txt") as tmp:
        tmp.write(uploaded_file.getvalue())
        tmp_path = Path(tmp.name)

    # Load and process the data
    WhatsappChatLoader = download_loader("WhatsappChatLoader")
    loader = WhatsappChatLoader(path=str(tmp_path))
    documents = loader.load_data()

    # Display the results
    st.write("Loaded chat data:")
    # st.write(documents)
    intax = GPTSimpleVectorIndex.from_documents(documents)
    if index not in st.session_state:
        st.session_state.index = intax
        st.success("session state added index")

    

    # Clean up temporary file
else:
    st.warning("Please upload a .txt file to analyze WhatsApp chats.")


inp= st.text_input("Input a query")
send = st.button("Submit")
clear = st.button("clear sessionstate")
if send:
    resp= st.session_state.intax.query(inp)
    st.write(resp.response)
    pass

if clear:
    tmp_path.unlink()
