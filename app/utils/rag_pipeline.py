# rag_pipeline.py

from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
from langchain.schema import LLMResult
from app.config import *
import os
import re

def load_folder_documents(doc_folder="docs"):
    docs = []
    for filename in os.listdir(doc_folder):
        with open(os.path.join(doc_folder, filename), "r", encoding="utf-8") as f:
            text = f.read()
            docs.append(Document(page_content=text))
    return docs

def load_text_file(file_path):
    """Read and split text file into chunks."""
    if not file_path or not os.path.exists(file_path):
        return "Invalid file path or no file uploaded"
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()
            docs = Document(page_content=text)
        return docs
    except Exception as e:
        return f"Error reading file: {str(e)}"
        
def split_documents(docs):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=[".", "!", "?"]
    )
    chunks = splitter.split_documents(docs)
    return chunks

def split_text(doc):
    """Split text into chunks."""
    splitter = RecursiveCharacterTextSplitter(
    chunk_size=CHUNK_SIZE,
    chunk_overlap=CHUNK_OVERLAP,
    separators=[".", "!", "?"]
)
    chunks = splitter.split_documents([doc])    # Note: pass as a list
    return chunks

def embed_documents(chunks):
    embedder = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)
    db = FAISS.from_documents(chunks, embedder)
    
    if not os.path.exists(VECTOR_DB_PATH):
        os.makedirs(VECTOR_DB_PATH)

    db.save_local(VECTOR_DB_PATH)
    return db

def load_to_embeddings(mode="file", path=None):
    
    if mode == "folder":
        docs = load_folder_documents(doc_folder=path)
        chunks = split_documents(docs)
        return embed_documents(chunks)

    elif mode == "file":
        doc = load_text_file(file_path=path)
        chunk = split_text(doc)
        return embed_documents(chunk)
    else:
        raise ValueError("Invalid mode. Use 'folder' or 'file'.")

def load_or_create_vectorstore():
    if os.path.exists(f"{VECTOR_DB_PATH}/index.faiss"):
        return FAISS.load_local(VECTOR_DB_PATH, HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME), allow_dangerous_deserialization=True)
    else:
        docs = load_folder_documents()
        chunks = split_documents(docs)
        return embed_documents(chunks)
