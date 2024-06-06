"""
In this file implementation which is help to store vectors in FAISS DB

"""

from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFLoader,DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
from dotenv import load_dotenv

load_dotenv()

DIR_PATH="docs/"
DB_FAISS_PATH="vectorstores/db_faiss/"

os.makedirs(DIR_PATH,exist_ok=True)
os.makedirs(DB_FAISS_PATH,exist_ok=True)
def create_vectordb():
    #Load file
    loader=DirectoryLoader(DIR_PATH,glob="*.pdf",loader_cls=PyPDFLoader)
    documents=loader.load()

    #split chunks of documents
    text_splitter=RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap=200)
    docs=text_splitter.split_documents(documents)

    #embedding
    key=os.getenv("OPENAI_API_KEY")
    embeddings=OpenAIEmbeddings()

    #vectorstore
    vector_store_db=FAISS.from_documents(docs,embeddings)
    vector_store_db.save_local(DB_FAISS_PATH)

# if __name__ == "__main__":
#     create_vectordb()