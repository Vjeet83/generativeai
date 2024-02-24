import streamlit as st
import google.generativeai as genai

genai.configure(api_key= "AIzaSyA12-XH6TnsussCErMQJkO22O12XkvaQrs")

## function to load Gemini Pro model and get response
model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=[])
 
def get_gemini_response(question):
    response=chat.send_message(question,stream = True)
    return response 
 

st.set_page_config(page_title ="Q&A Demo")

st.header("Gemini LLM Application")
st.subheader("hello it is subheader ")

if "chat_history " not in st.session_state:
    st.session_state['chat_history'] = []

input  =st.text_input("Input:",key = "input")

submit = st.button("ask the question")

if submit and input:
    response = get_gemini_response(input)
    ## Add user quary and response to session chat history
    st.session_state['chat_history'].append(("you :" ,input))
    st.subheader("The Response is")
    for chunk in response:
        st.write(chunk.text)
        st.session_state['chat_history'].append(("Bot :" ,chunk.text))
st.subheader("The Chat History is")

for role, text in st.session_state["chat_history"]:
    st.write(f"{role}: {text}")

