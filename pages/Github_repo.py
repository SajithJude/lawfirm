import os
import streamlit as st
from llama_index import download_loader
# from llama_index.readers.llamahub_modules.github_repo import GithubRepositoryReader, GithubClient
from llama_index.readers.llamahub_modules.github_repo import GithubRepositoryReader, GithubClient
from llama_index import  GPTSimpleVectorIndex , Document





download_loader("GithubRepositoryReader")

# Define Streamlit input components for each input parameter
owner = st.text_input("Enter the owner of the GitHub repository")
repo = st.text_input("Enter the name of the GitHub repository")
filter_directories = st.multiselect("Select directories to include", options=["pages", "docs"])
filter_file_extensions = st.multiselect("Select file extensions to include", options=[".py"])
verbose = st.checkbox("Verbose mode")
concurrent_requests = st.slider("Select number of concurrent requests", min_value=1, max_value=20, value=10)


loa = st.button("Create index")

if loa:
# Load data from the GitHub repository using the selected input parameters
    github_client = GithubClient(os.getenv("GITHUB_TOKEN"))
    loader = GithubRepositoryReader(
        github_client,
        owner=owner,
        repo=repo,
        filter_directories=(filter_directories, GithubRepositoryReader.FilterType.INCLUDE),
        filter_file_extensions=(filter_file_extensions, GithubRepositoryReader.FilterType.INCLUDE),
        verbose=verbose,
        concurrent_requests=concurrent_requests,
    )

    docs_branch = loader.load_data(branch="master")
    index = GPTSimpleVectorIndex.from_documents(docs_branch)
        # name = web_dir / url_input
    index.save_to_disk(f"github.json")
 
    # b ir / selected_index_file
    index = GPTSimpleVectorIndex.load_from_disk(f"github.json")

inp = st.text_input("Ask question")
ask = st.button("Submit")

if ask:
    res = index.query(inp)
    st.write(res)
    pass
    # docs_commit = loader.load_data(commit="a6c89159bf8e7086bea2f4305cff3f0a4102e370")

# # Display the extra_info for each doc
# for doc in docs:
#     st.write(doc.extra_info)
