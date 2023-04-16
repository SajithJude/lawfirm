import streamlit as st
import base64
import requests
import json
import os
from pathlib import Path
from llama_index import download_loader, GPTSimpleVectorIndex, SimpleDirectoryReader

st.set_option('deprecation.showfileUploaderEncoding', False)

# Title
st.title("OCR and Search")

# OCR function
def callAPI(image):
    vision_url = 'https://vision.googleapis.com/v1/images:annotate?key='

    # Your Google Cloud Platform (GCP) API KEY. Generate one on cloud.google.com
    api_key = os.environ["GCP_KEY"] 
    # Load your image as a base64 encoded string

    # Generate a post request for GCP vision Annotation
    json_data= {
        'requests': [
            {
                'image':{
                    'content': image.decode('utf-8')
                },
                'features':[
                    {
                        'type':'TEXT_DETECTION',
                        'maxResults':5
                    }
                ]
            }
        ]
    }

    # Handle the API request
    responses = requests.post(vision_url+api_key, json=json_data)

    # Read the response in json format

    return responses.json()

# Text saver function
def save_text(text):
    os.makedirs('text', exist_ok=True)  # create directory if it doesn't exist
    file_name = f"{st.session_state.photo_name.split('.')[0]}.txt"
    file_path = os.path.join("text", file_name)
    with open(file_path, 'w') as f:
        f.write(text)
        st.write('Text saved to file:', file_path)

# Photo taker
img_file_buffer = st.camera_input("Take a picture")
if img_file_buffer is not None:
    # Get the photo name to save the text file with the same name
    st.session_state.photo_name = f"photo_{st.session_state.get('photo_counter', 0)}.jpg"
    st.session_state.photo_counter = st.session_state.get("photo_counter", 0) + 1

    # OCR and save text file
    encoded_image = base64.b64encode(img_file_buffer.read())
    result = callAPI(encoded_image)
    # try:
    info = result['responses'][0]['textAnnotations'][0]['description']
    # st.image(img_file_buffer)
    st.caption("Text Recognized")
    st.write(info)
    save_text(info)

    # Create index from text directory
    text_dir = os.path.join(os.getcwd(), "text")
    st.write(text_dir)
    # if text_dir.exists():
    index_path = text_dir
    # if not index_path.exists():
    documents = SimpleDirectoryReader(str(text_dir)).load_data()
    intax = GPTSimpleVectorIndex.from_documents(documents)
    res= intax.query("Generate 10 Questions from this documents")
    st.write(res)

    # intax.save(str(index_path))
    st.write("Index created for text directory")

        # else:
        #     intax = download_loader(str(index_path))
        #     st.write("Index loaded from file")

else:
    st.warning("Directory 'text' not found. Please save OCR output text files to 'text' directory.")

    # except: 
    #     st.write(e)
