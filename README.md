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

## Provides
- [CODE DEMO V.1 NOTEBOOK & Python Files Details in project](DEMO_RAG.ipynb)
- [DEMO_PROJECT_EXAMPLE1](https://drive.google.com/file/d/1RT2TAWfUH7-CnTr7oNyb4ZSWbTKF1omP/view?usp=sharing)
- [DEMO_PROJECT_EXAMPLE2](https://drive.google.com/file/d/1iuttgnk7uVmzI5tzOH01yVddA610XHOa/view?usp=sharing)

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
    

