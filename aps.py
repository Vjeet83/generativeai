# from dotenv import load_dotenv
# load_dotenv()   ## loading all the enviroment variable

import streamlit as st
import  os 
import google.generativeai as genai 

# genai.configure(api_key=os.getenv("KEY"))   ## here i call api from .env file
#

## FUNCTION TO LOAD GEMINI PRO MODEL AND GET RESPONCE
genai.configure(api_key="AIzaSyA12-XH6TnsussCErMQJkO22O12XkvaQrs") 
# (here i direct use api insted of call api from .env)
model = genai.GenerativeModel("gemini-pro")



def get_gemini_response(question): 
    response = model.generate_content(question) 
    return response.text

## initialize our streamlit app

st.set_page_config(page_title="Q $ Ans Demo")
st.header("our LLm generative model")
input = st.text_input("input :",key = "input")
submit  = st.button("ask question")
## when submit is click
if submit:
     response = get_gemini_response(input)
     st.subheader("the Response is :")
     st.write(response)

