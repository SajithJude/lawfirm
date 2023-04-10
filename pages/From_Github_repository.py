import os
import streamlit as st
from llama_index import download_loader
from langchain import OpenAI
from llama_index import GPTSimpleVectorIndex, Document, LLMPredictor, ServiceContext

st.title("Ask Questions from Github Repo")

st.caption("This App interacts with GitHub repositories and allows you to ask questions related to those repositories. you can choose from my personal existing repositories or provide a custom external repository URL, select the branch they want to ask questions from, and ask their own custom questions related to the repository. The app can retrieve information related to the frameworks used in the repository or any other relevant information and provide users with the answers.")


download_loader("GithubRepositoryReader")
from llama_index.readers.llamahub_modules.github_repo import GithubRepositoryReader, GithubClient





# with col1.expander("Select Repository"):
    # Define Streamlit input components for repository selection and custom URL input
repository_selection = st.radio("How do you wanna start", ["Select on of my existing Repositories", "Custom Repository URL"])
if repository_selection == "Custom Repository URL":
    repo_url = st.text_input("Enter the URL of the GitHub repository")
else:
    repolist = ['https://github.com/SajithJude/ideagen',
            'https://github.com/SajithJude/coursebot',
            'https://github.com/SajithJude/DocuBOT',
            'https://github.com/SajithJude/quickbomAI',
            'https://github.com/SajithJude/portfolioweb',
            'https://github.com/SajithJude/flipick',
            'https://github.com/SajithJude/flipick-chat',
            'https://github.com/SajithJude/FlipickReports',
            'https://github.com/SajithJude/SCORM-GPT',
            'https://github.com/SajithJude/GKwebgen',
            'https://github.com/SajithJude/SCORMGPT',
            'https://github.com/SajithJude/demoupworknlp',
            'https://github.com/SajithJude/modfied-chat-doc',
            'https://github.com/SajithJude/pdf2bs4',
            'https://github.com/SajithJude/langchain',
            'https://github.com/SajithJude/ELC-accessibility',
            'https://github.com/SajithJude/MoraRPGobi',
            'https://github.com/SajithJude/QUICKBOM',
            'https://github.com/SajithJude/pdfopenai',
            'https://github.com/SajithJude/streamlitUi',
            'https://github.com/SajithJude/writeforme',
            'https://github.com/SajithJude/HATCH-HudsonAlpha-Tech-Challenge-2023',
            'https://github.com/SajithJude/text-Image-Chatbot',
            'https://github.com/SajithJude/hacktech-2023',
            'https://github.com/SajithJude/jobreveiw',
            'https://github.com/SajithJude/AccessibleBeautyAI',
            'https://github.com/SajithJude/streamlitMLpred',
            'https://github.com/SajithJude/bipolarTweetdetection',
            'https://github.com/SajithJude/vehiclediagnostics',
            'https://github.com/SajithJude/GAN_environment']

    repo_url = st.selectbox("Select one my existing repositories", repolist)

# Extract owner and repository name from the URL or set to None if not provided
if repo_url:
    url_parts = repo_url.strip().split("/")
    owner = url_parts[-2]
    repo = url_parts[-1]
    if 'repo' not in st.session_state:
        st.session_state['repo'] = repo


else:
    owner = None
    repo = None

# Define Streamlit input components for filtering options and other parameters
# filter_directories = st.multiselect("Select directories to include(Optional)", options=["pages", "docs"])
# filter_file_extensions = st.multiselect("Select file extensions to include(optional)", options=[".py"])
branch = st.text_input("Input Branch Name")
# verbose = st.checkbox("Verbose mode")
# concurrent_requests = st.slider("Select number of concurrent requests", min_value=1, max_value=20, value=10)

# Create index from selected repository
loa = st.button("Fetch Repo")

col1, col2 = st.columns(2)

if loa and owner and repo:
    # Load data from the GitHub repository using the selected input parameters
    github_client = GithubClient(os.getenv("GITHUB_TOKEN"))
    loader = GithubRepositoryReader(
        github_client,
        owner=owner,
        repo=repo,
        # filter_directories=(filter_directories, GithubRepositoryReader.FilterType.INCLUDE),
        # filter_file_extensions=(filter_file_extensions, GithubRepositoryReader.FilterType.INCLUDE),
        verbose=True,
        concurrent_requests=10,
    )

    docs_branch = loader.load_data(branch=branch)
    # Load index from saved file
    llm_predictor = LLMPredictor(llm=OpenAI(temperature=0, model_name="text-davinci-003", max_tokens=1024))
    service_context = ServiceContext.from_defaults(llm_predictor=llm_predictor)

    index = GPTSimpleVectorIndex.from_documents(docs_branch,service_context=service_context)
    with col2.expander("FAQ Questions and responses",expanded=True):
        about = index.query("What does this application do")
        tech = index.query("What are the technologies and libraries used in this repo")
        st.markdown("### What does this application do?")
        st.write(about.response)
        st.markdown("### What are the technologies and libraries used in this repo ?")
        st.write(tech.response)

   
    # with col1.expander("Ask your own Questions",expanded=True):
        # Query the index with user input
    inp = st.text_input("Ask question")
    ask = st.button("Submit")

    if ask:
        res = index.query(inp)
        st.write(res)
        pass
