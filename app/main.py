
import os
# from utils.rag_pipeline import load_to_embeddings
# from config import *
# from utils.ollama import *
# from ui import main_ui

from app.utils.rag_pipeline import load_to_embeddings
from app.config import *
from app.utils.ollama import *
from app.ui import main_ui





if __name__ == "__main__":
    # # for laod files text and embeded
    # path = "data/docs/thai_cabinet_2025_withnicknames.txt"
    # load_to_embeddings(mode="file", path=path)

    # # For response in local NO UI
    # response_answer()

    # Main usaage response with UI
    main_ui()
 