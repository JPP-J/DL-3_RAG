from unittest.mock import patch
from app.utils.ollama import response_answer_gr


from unittest.mock import patch

@patch("utils.ollama.stream_ollama_response")
@patch("utils.rag_pipeline.load_folder_documents", return_value=["Fake doc"])
def test_response_answer_gr_mocked(mock_docs, mock_stream):
    mock_stream.return_value = iter(["This is a mock response."])
    query = "What is AI?"
    result = "".join(response_answer_gr(query))
    assert "mock response" in result
