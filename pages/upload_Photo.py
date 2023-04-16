import streamlit as st
import base64
import requests
import json
import os


st.title('Optical Character Recognition')
cam = st.radio('Please select an option',('Open Webcam', 'Upload Image'))
# upload = st.checkbox('Upload an Image')

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


if cam =='Open Webcam':
    img_file_buffer = st.camera_input("Take a picture")
    if img_file_buffer is not None:
        encoded_image = base64.b64encode(img_file_buffer.read())
        result = callAPI(encoded_image)
        try:
            info = result['responses'][0]['textAnnotations'][0]['description']
            st.image(img_file_buffer)
            st.caption("Text Recognized")
            st.write(info)

            # write output to a file
            os.makedirs('text', exist_ok=True)  # create directory if it doesn't exist
            with open('text/output.txt', 'w') as f:
                f.write(info)
                st.write('Output written to file: text/output.txt')

        except:
            st.write("An exception occurred")

