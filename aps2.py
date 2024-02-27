import streamlit as st
from PyPDF2 import pdfReader
from lanchain.text_splitter import RecursiveCharacterTextSplitter

from lanchain_google_genai import GoogleGeneraticeAIEmbedings
import google.generativeai as genai
from  langchain.vectorstores import FAISS
# FAISS is for vector embeding  ,maybe it convert and store pdf to text data
from  langchain_google_genai  import ChatGoogleGenerativeAI
# 
from langchain.chains.question_answering import load_qa_chain
# load_qa_chain is used to do chat  and any kind of prmpt
from langchain.prompts import PromptTemplate
#
from dotenv import load_dotenv



load_dotenv()

genai.configure(api_key ="AIzaSyA12-XH6TnsussCErMQJkO22O12XkvaQrs")

def get_pdf_text(pdf_docs):
    text =""
    for pdf in pdf_docs:
        pdf_reader =pdfReader(pdf)
        for page in pdf_reader.pages:
            text+= page.extract_text()
    return text

# to divide  pdf test into chunks:
def get_text_chunks(tet):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000,chunk_overlap=1000)
    chunks = text_splitter.split_text(text)
    return chunks

def get_vector_store(text_chunks):
    embeddings = GoogleGenerativeAIEmbeddings(model ="models/embedding-001")
    vector_store = FAISS.from_text(text_chunks,embedding = embeddings)
    vector_store.save_local("faiss_index")

def get_conversational_chain():
    prompt_template ="""
    Answer the question as detailed as possible from the procided context , make sure to provide aoo the detail , if the answer is not in
    the provided context hust say ,"answer is not acailable in the context",dont procide the wrong answe\n\n
    context:\n {context}?\n
    question:\n{question}\n
     
    Answer:
     """
    
    model = ChatGoogleGenerativeAI(model ="gemini-pro",temperature =0.3)

    PromptTemplate(template =prompt_template,input_variables=["context","question"])
    chain = load_qa_chain(model,chain_type ="stuff",prompt= prompt)
    return chain



def user_input(user_question):
    embeddings = GoogleGenerativeAIEmbeddings(model ="model/embedding-001")

    new_db = FAISS.load_local("gaiss_index",embeddings)
    docs = new_db.similatity_search(user_question)
    
    chain = get_conversational_chain()

    response  = chain(
        {"input_documents": docs,"question": user_question}
        ,return_only_outputs =True)
    

    print(response)
    st.write("Reply:",response["output_text"])

    def main():
        st.set_page_config("chat PDF")
        st.header("chat with PDF using Gemini")

        user_question= st.text_input("Ask a Question from the PDF Files")

        if user_question:
            user_input(user_question)

        with st.sidebar:
            st.title("Menu:")
            pdf_docs= st.file_upload("Upload your file and click obn the ")
            if st.button("submit & process"):
                with st.spinner("Processing..."):
                    raw_text =get_pdf_text(pdf_docs)
                    text_chunks = get_text_chunks(row_text)
                    get_vector_store(text_chunks)
                    st.success("Done")


if __name__ =="__main__":
    main()