# ollama.py

import gradio as gr
from chromadb.config import Settings
from chromadb.utils import embedding_functions
import ollama
import os
from config import *
import requests
from utils.rag_pipeline import load_or_create_vectorstore
import json
from datetime import datetime
from pythainlp.util import normalize

# NO USE
def setting_ollama_embedding_function():
    """Initialize Ollama embedding function."""
    ollama_embedded = embedding_functions.OllamaEmbeddingFunction(
        url="http://localhost:11434/api/embeddings",
        model_name="nomic-embed-text"
    )
    return ollama_embedded

def stream_ollama_response(prompt, temperature=TEMPERATURE):
    stream = ollama.generate(
        model=LLM_MODEL_NAME,
        prompt=prompt,
        stream=True,
        options={"temperature": float(temperature)}
    )

    for chunk in stream:
        yield chunk["response"]  # Stream partial chunks live


# def build_prompt(query, context_chunks, language="thai"):
#     # Clean and filter the context
#     cleaned_chunks = [
#         doc.page_content.strip() for doc in context_chunks if doc.page_content.strip()
#     ]
#     context = "\n".join(cleaned_chunks)

#     if language == "thai":
#         instruction = ""
#         # instruction = "กรุณาตอบคำถามต่อไปนี้เป็นภาษาไทย:"
#     else:
#         instruction = "Please answer the question in English:"
#     # return f"""Answer the following question as best you can, and using the context below if relevant.:
#     return f"""{instruction}
        
# Context:
# {context}

# Question:
# {query}

# Answer:"""


# def build_prompt(query, context_chunks=None, language="thai"):
#     if language == "thai":
#         instruction = "ตอบคำถามต่อไปนี้เป็นภาษาไทย ถ้ามีข้อมูลในบริบทให้ใช้ แต่ถ้าไม่มีให้ตอบตามความรู้ทั่วไป"
#     elif language == "en":
#         instruction = "Answer the following question in English using the context if available, otherwise use general knowledge."
#     else:
#         instruction = ""

#     context = ""
#     if context_chunks:
#         cleaned = [doc.page_content.strip() for doc in context_chunks if doc.page_content.strip()]
#         if cleaned:
#             context = "\n".join(cleaned)

#     prompt = f"""{instruction}

# """
#     if context:
#         prompt += f"""Context:
# {context}

# """

#     prompt += f"""Question: {query}

# Answer:"""

#     return prompt

def load_all_chat_histories(folder="chat_history", max_files=5):
    """Load and return the latest N chat logs from a folder."""
    chat_logs = []
    if not os.path.exists(folder):
        return []

    # Get list of chat files sorted by most recent
    files = sorted(
        [f for f in os.listdir(folder) if f.endswith(".json")],
        key=lambda x: os.path.getmtime(os.path.join(folder, x)),
        reverse=True
    )

    for file_name in files[:max_files]:
        path = os.path.join(folder, file_name)
        with open(path, "r", encoding="utf-8") as f:
            try:
                chat = json.load(f)
                chat_logs.extend(chat)
            except Exception as e:
                print(f"⚠️ Could not read {file_name}: {e}")
    return chat_logs


# def build_prompt(query, context_chunks=None, messages=None, language="thai"):
#     if language == "thai":
#         instruction = ""
#     elif language == "en":
#         instruction = "Answer the question below in English using the provided context if available, otherwise use general knowledge."
#     else:
#         instruction = ""

#     # Prepare context
#     context = ""
#

def build_prompt(query, context_chunks=None, messages=None):
    # Clean context
    cleaned_chunks = [
        doc.page_content.strip()
        for doc in (context_chunks or [])
        if doc.page_content.strip()
    ]
    
    # Format past messages
    formatted_history = ""
    if messages:
        for m in messages:
            if m["role"] == "user":
                formatted_history += f"Q: {m['content']}\n"
            elif m["role"] == "assistant":
                formatted_history += f"A: {m['content']}\n"

    prompt = ""
    if cleaned_chunks:
        prompt += f"Context:\n{'\n'.join(cleaned_chunks)}\n\n"
    if formatted_history:
        prompt += f"Chat History:\n{formatted_history}\n"
    
    prompt += f"Question:\n{query}\n\nAnswer:"
    
    return prompt




def is_context_relevant(context_docs, min_length=20):
    total_len = sum(len(doc.page_content.strip()) for doc in context_docs)
    return total_len >= min_length


def save_chat(messages, folder_path="data/chat_history"):
    # Ensure the folder exists
    os.makedirs(folder_path, exist_ok=True)

    # Create a timestamped file name
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
    file_name = f"chat_{timestamp}.json"

    # Full path to save the file in the folder
    file_path = os.path.join(folder_path, file_name)

    # Save the chat log
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(messages, f, indent=2, ensure_ascii=False)

    # print(f"💾 Chat saved to {file_path}")

def limit_history(messages, max_turns=6):
    """Keep only the last N message pairs (user + assistant)."""
    return messages[-max_turns*2:]


def response_answer():
    db = load_or_create_vectorstore()
    messages = []

    print("🧠 Ask me anything! (type 'exit' or 'quit' to stop)\n")
    
    while True:
        try:
            query = input("🔎 Ask a question: ").strip()
            if query.lower() in ("exit", "quit"):
                print("👋 Exiting. Goodbye!")
                break

            if not query:
                answer = "⚠️  Please enter a valid question."
                messages.append({"role": "assistant", "content": answer})
            else:
                messages.append({"role": "user", "content": query})

            # Vector similarity search (RAG)
            context_docs = db.similarity_search(query, k=K)

            # scored_docs = db.similarity_search_with_score(query, k=K)
            # context_docs = [doc for doc, score in scored_docs]
            # context_docs = [doc for doc, score in scored_docs if score < SIMILARITY_THRESHOLD]
            # for doc, score in scored_docs:
            #     print(f"Score: {score:.4f} | Preview: {doc.page_content[:60]}")

            if not is_context_relevant(context_docs):
                context_docs = []  # skip context, use base model prompt

            # Prompt building with context fallback
            query = normalize(query)
            history_from_file = load_all_chat_histories()
            combined_history = limit_history(history_from_file + messages)
            prompt = build_prompt(query, context_chunks=context_docs, messages=combined_history)
            print("\n🧠 Ollama is thinking...\n")
            
            response_parts = []
            # Stream live output
            for part in stream_ollama_response(prompt):
                response_parts.append(part)
                print(part, end="", flush=True)
            
            print("\n" + "-"*40 + "\n")  # Divider between responses

            full_answer = "".join(response_parts)
            messages.append({"role": "assistant", "content": full_answer})

            save_chat(messages)  # save after full response

        except KeyboardInterrupt:
            print("\n👋 Interrupted. Exiting.")
            break

        except Exception as e:
            print(f"\n❌ An error occurred: {e}\n")

def response_answer_gr(query):
    db = load_or_create_vectorstore()
    messages = []

    if not query:
        answer = "⚠️  Please enter a valid question."
        messages.append({"role": "user", "content": query})
        messages.append({"role": "assistant", "content": answer})
        save_chat(messages)
        return answer
    
    # Vector similarity search (RAG)
    context_docs = db.similarity_search(query, k=K)

    if not is_context_relevant(context_docs):
        context_docs = []  # skip context, use base model prompt

    # Prompt building with context fallback
    query = normalize(query)
    history_from_file = load_all_chat_histories()
    combined_history = limit_history(history_from_file + messages)
    prompt = build_prompt(query, context_chunks=context_docs, messages=combined_history)

    messages.append({"role": "user", "content": query})
    
    response_parts = []
    # Stream live output
    for part in stream_ollama_response(prompt):
        response_parts.append(part)
        yield part
    
    full_answer = "".join(response_parts)
    messages.append({"role": "assistant", "content": full_answer})

    save_chat(messages)  # save after full response
    




