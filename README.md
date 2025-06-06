# RAG Application with Ollama, FAISS, and Gradio UI Project
![Last Commit](https://img.shields.io/github/last-commit/JPP-J/DL-3_RAG?style=flat-square)
![Languages](https://img.shields.io/github/languages/count/JPP-J/DL-3_RAG?style=flat-square)

This repo is home to the code that accompanies Jidapa's *RAG Application with Ollama, FAISS, and Gradio UI Project*:

## Description  
A Retrieval-Augmented Generation (RAG) system combining Ollama LLM and FAISS vector search to answer user questions based on indexed text documents. The app features a Gradio UI for uploading documents, chatting, and saving history. Fully containerized for easy deployment with Docker.

## Features  
- Upload and index text files for vector search (FAISS)  
- Use Ollama model for context-aware answer generation  
- Persistent chat history saved as JSON logs  
- Gradio UI with Admin and User chat tabs  
- Docker-ready with volumes for data persistence  

## Libraries and Tech Used  
- **RAG & Vector Search**: `langchain`, `FAISS`, `HuggingFaceEmbeddings`  
- **LLM & API**: `ollama` Python client  
- **UI**: `gradio`  
- **Utils**: `pythainlp` for text normalization
- **DevOps**: `Docker`, `Docker Compose`, GitHub-Action
- **Embedded model**: all-MiniLM-L6-v2
- **LLM model**: gemma3:1b
  
## Features
- Upload and index text documents for vector search  
- Use Ollama LLM to generate context-aware answers  
- Save chat history with persistent logs  
- Dockerized for easy deployment  
