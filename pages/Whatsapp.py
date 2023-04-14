import streamlit as st
from pathlib import Path
from llama_index import download_loader, GPTSimpleVectorIndex, SimpleDirectoryReader
from tempfile import NamedTemporaryFile

st.set_option('deprecation.showfileUploaderEncoding', False)

# Title
st.title("WhatsApp Chat Analyzer")

# File uploader
# File uploader
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

    # Display the results
    st.write("Loaded chat data:")
    # st.write(documents)
    intax = GPTSimpleVectorIndex.from_documents(documents)
    if intax not in st.session_state:
        st.session_state.intax = intax
        st.success("session state added index")

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
