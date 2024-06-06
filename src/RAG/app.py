import os
import streamlit as st
from streamlit_chat import message
import base64

from ingest import create_vectordb
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain_community.vectorstores import FAISS
from langchain.llms import OpenAI
from langchain_community.embeddings import OpenAIEmbeddings

# from dotenv import load_dotenv
# load_dotenv()

#api key
key=os.getenv("OPENAI_API_KEY")

st.title("Chat with pdf using OpenAI")
st.sidebar.title("File Details")

custom_prompt_template="""
use the following piece of information to answer user questions.
if you dont know the answer ,you just say dont know answer,dont try to make up answer.

Context:{context}
Question:{question}

Only help full answer below and nothing else:
Helpfull answer:

"""

# Handling the pdf files
def display_pdf(file):
    with open(file,"rb") as file_obj:
        base64_pdf=base64.b64encode(file_obj.read()).decode("utf-8")
    pdf_display = f'<iframe  src="data:application/pdf;base64,{base64_pdf}" width="100%" height="500"  type="application/pdf"></iframe>'
    st.markdown(pdf_display,unsafe_allow_html=True)


# Prompt

def custom_prompt():
    prompt=PromptTemplate(template=custom_prompt_template,
                          input_variables=["context", "question"])
    return prompt
#llm pipeline
def llmpipeline():
    llm=OpenAI(api_key=key)
    return llm

#build chain
def retrival_qa_chain(prompt,llm,db):
    chain=RetrievalQA.from_chain_type(
        llm=llm,
        chain_type='stuff',
        return_source_documents=True,
        retriever=db.as_retriever(search_kwargs={"k":2}),
        chain_type_kwargs={"prompt":prompt}
    )
    return chain
#builded qa llm
def qa_bot():
    DB_FAISS_PATH="vectorstores/db_faiss/"
    embeddings=OpenAIEmbeddings()
    vector_db=FAISS.load_local(DB_FAISS_PATH,embeddings,allow_dangerous_deserialization=True)
    llm=llmpipeline()
    prompt=custom_prompt()
    qa=retrival_qa_chain(prompt,llm,vector_db)
    return qa

def process_question(prompt):
    qa_result=qa_bot()
    final_answer=qa_result({"query":prompt})
    # final_answer=response["result"]
    return final_answer

def display_conversation(history):
    for i in range(len(history["generated"])):
        message(history["past"][i], is_user=True, key=str(i) + "_user")
        message(history["generated"][i],key=str(i))


def main():
    file_upload=st.sidebar.file_uploader("Upload file...",type=["pdf","docx"])
    if file_upload:

        st.sidebar.success("File Uploaded successfully",icon="✅")
        file_name=file_upload.name # file name
        file_size=len(file_upload.read()) # get file size in bytes

        st.sidebar.markdown("<h3 style=text-align:center>File Details</h3>",unsafe_allow_html=True)
        file_details={
            "file_name":file_name,
            "file_size":file_size
        }
        st.sidebar.json(file_details) 

        #save locally
        file_dir="docs"
        os.makedirs(file_dir,exist_ok=True)
        file_path="docs/"+file_upload.name
        with open(file_path,"wb") as f:
            f.write(file_upload.getbuffer())

        #Col divide
        col1,col2=st.columns([1,2])


        with col1:
            st.markdown("<h3 style=text-align:center> PDF Preview</h3>",unsafe_allow_html=True)
                    #Display files
            display_pdf(file_path)

        with col2:
            st.markdown("<h2 style=text-aligh:center> QA-Bot</h2>",unsafe_allow_html=True)
            with st.spinner("Embedding are in process.."):
                create_vectordb()
            st.success("Embeddings successfully done")
            st.markdown("<h4 style color:black;'>Chat Here</h4>", unsafe_allow_html=True)
            
            
            user_input=st.text_input("Prompt",key="input")

            if "generated" not in st.session_state:
                st.session_state["generated"]=["I am ready to help you"]
            if "past" not in st.session_state:
                st.session_state["past"]=["hey there"]

            if user_input:
                answer=process_question(user_input)
                st.session_state["past"].append(user_input)

                response=answer["result"]
                # source=answer["source_documents"]
                st.session_state["generated"].append(response)
                # st.session_state["generated"].append(source)

                   # Display conversation history using Streamlit messages
            if st.session_state["generated"]:
                display_conversation(st.session_state)


if __name__=="__main__":
    main()
                