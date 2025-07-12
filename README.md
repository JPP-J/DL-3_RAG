# RAG Application with Ollama, FAISS, and Gradio UI Project
![Last Commit](https://img.shields.io/github/last-commit/JPP-J/DL-3_RAG?style=flat-square)
![Languages](https://img.shields.io/github/languages/count/JPP-J/DL-3_RAG?style=flat-square)

This repo is home to the code that accompanies Jidapa's *RAG Application with Ollama, FAISS, and Gradio UI Project*:

## 📌 Overview

This project implements a **Retrieval-Augmented Generation (RAG)** system that combines vector-based document search with large language model (LLM) generation to provide accurate, context-aware answers to user queries. The system leverages **Ollama LLM** for generative responses and **FAISS** for fast semantic search on indexed text documents.

### 🧩 Problem Statement

Users often need to find precise information from large collections of text documents. Traditional search methods can miss context or nuance, and purely generative models may hallucinate or lack grounding. This project addresses these challenges by augmenting LLM generation with retrieval over relevant document passages, improving answer accuracy and reliability.

### 🔍 Approach

- Use **FAISS** for efficient vector search over document embeddings (using `all-MiniLM-L6-v2`).
- Generate responses with **Ollama's LLM** (`gemma3:1b`), grounded by retrieved document context.
- Provide a user-friendly **Gradio UI** to upload documents, interact via chat, and view/save conversation history.
- Fully containerize the application with **Docker** for easy deployment and data persistence.

### 🎢 Processes

1. Upload and preprocess text documents.
2. Generate embeddings with HuggingFace models.
3. Index embeddings with FAISS for fast retrieval.
4. Query with user input, retrieve relevant documents.
5. Generate context-aware answers using Ollama LLM.
6. Save chat history as JSON logs for session continuity.
7. Deploy with Docker and Docker Compose.

### 🎯 Results & Impact

- Enables interactive, context-aware question answering over custom documents.
- Reduces manual search effort and improves user productivity.
- Provides a scalable and portable solution suitable for enterprise or research applications.

### ⚙️ Development Challenges

- Efficient embedding and indexing of diverse document formats.
- Integrating vector search results seamlessly with LLM generation.
- Managing persistent chat history and ensuring data integrity.
- Containerizing complex dependencies for smooth deployment across environments.


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
  

## Provides
- [`CODE DEMO V.1 NOTEBOOK & Python Files Details in project`](DEMO_RAG.ipynb)
- [`DEMO_PROJECT_EXAMPLE1`](https://drive.google.com/file/d/1RT2TAWfUH7-CnTr7oNyb4ZSWbTKF1omP/view?usp=sharing)
- [`DEMO_PROJECT_EXAMPLE2`](https://drive.google.com/file/d/1iuttgnk7uVmzI5tzOH01yVddA610XHOa/view?usp=sharing)

## Usage
### Docker image-container 
1. Build the Docker image:

    ```bash
    docker build -t rag-ollama-app .
    ```

2. Run the container (make sure Ollama is running on your host):

    ```bash
    docker run -p 7860:7860 -p 11434:11434 \
      -v $(pwd)/faiss_index:/app/faiss_index \
      -v $(pwd)/chat_history:/app/chat_history \
      -v $(pwd)/docs:/app/docs \
      rag-ollama-app
    ```

3. Open your browser at `http://localhost:7860`.

### Docker-compose 
1. Build docker-compose to create containers 
   
    ```bash
    docker-compose up --build
    ```

2. When going to stop containers 

   ``` bash
   docker-compose stop
   ```
3. Then later restart containers  with

   ``` bash
   docker-compose start
   ```
  
4. After usage containers, going to shutdown and cleanup
    ```bash
    docker-compose down
    ```
    

