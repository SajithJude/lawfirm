import streamlit as st

st.title('OpenAI-powered Chatbot Demo Apps')

st.write('Build custom chatbots with my LLM + OpenAI-powered demo apps that connect to various data sources, including PDFs, PPTX files, audio/video files, and scraped internet data. Respond to users in a conversational manner, allowing you to engage with your customers and provide them with the information they need, or extract data from any structured or Unstructured format to create reports. Explore my portfolio of easy-to-use demo apps today!')

st.markdown('For a sample demo I have connected data **:green[From Github Repository]** in this app, but I will be able to connect data from the following sources as well:')

# Adding image cards for each data source
col1, col2, col3 = st.columns(3)
with col1:
    # st.image('images/drive.png', width=100)
    st.subheader('Google Drive')
with col2:
    # st.image('images/drive.png', width=100)
    st.subheader('Gmail')
with col3:
    # st.image('images/drive.png', width=100)
    st.subheader('GoogleCalander')

col4, col5, col6 = st.columns(3)
with col4:
    # st.image('images/drive.png', width=100)
    st.subheader('Confluence ')
with col5:
    # st.image('images/drive.png', width=100)
    st.subheader('MongoDB ')
with col6:
    # st.image('images/drive.png', width=100)
    st.subheader('PostgreSQL ')

col7, col8, col9 = st.columns(3)
with col7:
    # st.image('images/drive.png', width=100)
    st.subheader('MySQL ')
with col8:
    # st.image('images/drive.png', width=100)
    st.subheader('BigQuery ')
with col9:
    # st.image('images/drive.png', width=100)
    st.subheader('Redshift ')

col10, col11, col12 = st.columns(3)
with col10:
    # st.image('images/drive.png', width=100)
    st.subheader('Snowflake ')
with col11:
    # st.image('images/drive.png', width=100)
    st.subheader('Elastic Search ')
with col12:
    # st.image('images/drive.png', width=100)
    st.subheader('WordPress ')

col13, col14 ,col15 = st.columns(3)
with col13:
    # st.image('images/drive.png', width=100)
    st.subheader('Notion ')
with col14:
    # st.image('images/drive.png', width=100)
    st.subheader('DynamoDB ')
with col15:
    # st.image('images/drive.png', width=100)
    st.subheader('AWS S3 ')