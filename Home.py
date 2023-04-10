import streamlit as st

st.title('OpenAI-powered Chatbot Demo Apps')

st.write('Build custom chatbots with my OpenAI-powered demo apps that connect to various data sources, including PDFs, PPTX files, audio files, and scraped internet data. Respond to users in a conversational manner, allowing you to engage with your customers and provide them with the information they need. Explore my portfolio of easy-to-use demo apps today!')

st.write('You will be able to connect data from the following sources:')

# Adding image cards for each data source
col1, col2, col3 = st.columns(3)
with col1:
    st.image('images/drive.png', width=100)
    st.write('Google Drive')
with col2:
    st.image('images/drive.png', width=100)
    st.write('Gmail')
with col3:
    st.image('images/drive.png', width=100)
    st.write('Google Calander Loader')

col4, col5, col6 = st.columns(3)
with col4:
    st.image('images/drive.png', width=100)
    st.write('Confluence ')
with col5:
    st.image('images/drive.png', width=100)
    st.write('MongoDB Connector')
with col6:
    st.image('images/drive.png', width=100)
    st.write('PostgreSQL ')

col7, col8, col9 = st.columns(3)
with col7:
    st.image('images/drive.png', width=100)
    st.write('MySQL ')
with col8:
    st.image('images/drive.png', width=100)
    st.write('BigQuery ')
with col9:
    st.image('images/drive.png', width=100)
    st.write('Redshift ')

col10, col11, col12 = st.columns(3)
with col10:
    st.image('images/drive.png', width=100)
    st.write('Snowflake ')
with col11:
    st.image('images/drive.png', width=100)
    st.write('Oracle ')
with col12:
    st.image('images/drive.png', width=100)
    st.write('SQLite ')

col13, col14 ,col15 = st.columns(3)
with col13:
    st.image('images/drive.png', width=100)
    st.write('Notion ')
with col14:
    st.image('images/drive.png', width=100)
    st.write('DynamoDB ')
with col15:
    st.image('images/drive.png', width=100)
    st.write('AWS S3 ')