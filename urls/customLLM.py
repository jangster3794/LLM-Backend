import json
from flask import Blueprint, request
from flask_cors import cross_origin
from dotenv import load_dotenv
from PyPDF2 import PdfReader

from langchain.llms import OpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.memory import ConversationBufferMemory

custom_llm_bp = Blueprint('/custom-llm', __name__)

# Load environment variables
load_dotenv()

llm = OpenAI(temperature=0.9)

vectorstore = None

# Convert PDF to raw text
def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

# Text Splitter to create chunks of data
def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks

# Use FAISS-cpu to create a vector store database to query inputs from custom PDF file
def get_vectorstore(text_chunks):
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    return vectorstore

def get_conversation_chain_from_vectorstore(vectorstore):
    memory = ConversationBufferMemory(
        memory_key='chat_history', return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory
    )
    return conversation_chain

# Create a vector store from a PDF file to communicate with
@custom_llm_bp.route("/create-store", methods=["POST"])
@cross_origin()
def single_query():
    files = request.files.getlist('file')  # 'file' corresponds to the name attribute in the HTML file input element
    raw_text = ""
    for file in files:
        if file.filename.endswith('.pdf'):
            pdf_reader = PdfReader(file)
            for page in pdf_reader.pages:
                raw_text += page.extract_text()
        else:
            return {"success": False, "message": "Invalid file format. Please upload PDF files only."}

    # get the text chunks
    text_chunks = get_text_chunks(raw_text)

    # create vector store
    global vectorstore
    vectorstore = get_vectorstore(text_chunks)
    return {"success": True, "message": "Stored succesfully"}

# Query Input to the custom vectorstore created from create-store API
@custom_llm_bp.route("/query", methods=["POST"])
def handle_query():
    user_question = json.loads(request.data).get('question')
    conversation_chain = get_conversation_chain_from_vectorstore(vectorstore)
    resp = conversation_chain(user_question)
    answer = resp['answer']
    return {"success": True, "data": answer}
