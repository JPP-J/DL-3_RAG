
import os
from utils.rag_pipeline import load_to_embeddings
from config import *
from utils.ollama import *
from ui import main_ui



if __name__ == "__main__":
    # path = "docs/thai_cabinet_2025_withnicknames.txt"
    # load_to_embeddings(mode="file", path=path)
    # response_answer(language='thai')
    main_ui()
    # history_from_file = load_all_chat_histories()
    # print(history_from_file)
    # demo()
    # print(LLM_MODEL_NAME)