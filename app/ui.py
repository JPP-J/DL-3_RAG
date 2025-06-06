# ui.py

import gradio as gr
from config import *
from utils.rag_pipeline import *
from utils.ollama import response_answer_gr

# UI
# Admin interface for uploading files 
def admin_interface(file_paths):
    """Admin interface for uploading and indexing multiple text files."""
    results = []
    for file_path in file_paths:
        result = load_to_embeddings("file", file_path)
        results.append(f"{file_path.name}: {result}")
    return "\n".join(results)

def response(message, history):
    output = ""
    for part in response_answer_gr(message):
        output += part
    return output  # Return a final full string


# Create Gradio interfaces
with gr.Blocks() as admin_app:
    gr.Markdown("# Admin Interface")
    gr.Markdown("Upload a text file to vectorstore its content for the chatbot.")
    file_input = gr.File(label="Upload Text Files", file_types=[".txt"], file_count="multiple")
    output = gr.Textbox(label="Indexing Result")
    upload_btn = gr.Button("Upload and Index")
    upload_btn.click(fn=admin_interface, inputs=file_input, outputs=output)

# ChatBot
# with gr.Blocks() as chat_app:
#     gr.Markdown("# Chatbot Interface")
#     gr.Markdown("Ask anythings or ask questions based on the indexed text file content.")
#     gr.ChatInterface(fn=response, type="messages")

with gr.Blocks() as chat_app:
    gr.Markdown("# Chatbot Interface")
    gr.Markdown("Ask anything or ask questions based on the indexed text file content.")

    # with gr.Row():
    #     language_selector = gr.Dropdown(
    #         choices=["thai", "en"],
    #         value="thai",
    #         label="Language",
    #         scale=1
    #     )

    chatbot = gr.ChatInterface(
        fn=lambda message, history: response(message, history),
        type="messages"
    )

    # language_selector.change(
    #     fn=lambda lang: None,  # no-op to trigger re-evaluation of fn
    #     inputs=language_selector,
    #     outputs=[]
    # )


# main function
def main_ui():
    """Main function to launch the Gradio interfaces."""
    # Launch both interfaces
    gr.TabbedInterface(
        [admin_app, chat_app],
        ["Admin Upload", "User Chat"],
        title="RAG Application with Ollama and Faiss"
    ).launch()