import os
import streamlit as st
from llama_index import download_loader
from langchain import OpenAI
from llama_index.readers.llamahub_modules.github_repo import GithubRepositoryReader, GithubClient
from llama_index import GPTSimpleVectorIndex, Document, LLMPredictor, ServiceContext


st.title("Ask Questions from Github Repo")

download_loader("GithubRepositoryReader")

# Define Streamlit input component for repository URL
repo_url = st.text_input("Enter the URL of the GitHub repository")

# Extract owner and repository name from the URL
if repo_url:
    url_parts = repo_url.strip().split("/")
    owner = url_parts[-2]
    repo = url_parts[-1]
else:
    owner = None
    repo = None

# Define Streamlit input components for filtering options and other parameters
filter_directories = st.multiselect("Select directories to include", options=["pages", "docs"])
filter_file_extensions = st.multiselect("Select file extensions to include", options=[".py"])
verbose = st.checkbox("Verbose mode")
concurrent_requests = st.slider("Select number of concurrent requests", min_value=1, max_value=20, value=10)


loa = st.button("Create index")

if loa and owner and repo:
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
    index.save_to_disk(f"github.json")
    st.success("Index created from repository successfully")
 
llm_predictor = LLMPredictor(llm=OpenAI(temperature=0, model_name="text-davinci-003", max_tokens=1024))
service_context = ServiceContext.from_defaults(llm_predictor=llm_predictor)

index = GPTSimpleVectorIndex.load_from_disk(f"github.json", service_context=service_context)
if index:
    st.success("Index Loaded from repository successfully")

inp = st.text_input("Ask question")
ask = st.button("Submit")

if ask:
    res = index.query(inp)
    st.write(res)