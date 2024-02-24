import streamlit as st
# import os 
import google.generativeai as genai
from PIL import Image 

# genai.configure(api_key=os.getenv(KEY = "AIzaSyA12-XH6TnsussCErMQJkO22O12XkvaQrs"))
# (here i call api from  .env file )

genai.configure (api_key = "AIzaSyA12-XH6TnsussCErMQJkO22O12XkvaQrs")
model = genai.GenerativeModel("gemini-pro-vision")

def get_gemini_response(input,image):
    if input!="":
        response = model.generate_content([input,image])
    else:
        response = model.generate_content(image)
    return response.text

## initialize our streamlit app

st.set_page_config(page_title = "google gemini image demo")

st.header("gemini Aplication")
input = st.text_input("input Prompt: ",key="input")

upload_file = st.file_uploader("chose an image..." , type =["jpg","jpeg","png"])
image = ""
if upload_file is not None:
    image = Image.open(upload_file)
    st.image(image,caption="Upload image" , use_column_width= True)

submit = st.button("tell me about the image")

## if submit  is clicked
if submit:
    response = get_gemini_response(input,image)
    st.subheader("the Response is ")
    st.write(response)