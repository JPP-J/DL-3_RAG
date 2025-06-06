import pytest
from unittest.mock import patch, MagicMock
from app.utils.ollama import response_answer_gr

@pytest.mark.asyncio
@patch("app.utils.ollama.stream_ollama_response")
@patch("app.utils.ollama.load_or_create_vectorstore")
def test_response_answer_gr_mocked(mock_load_vectorstore, mock_stream):
    # Mock the vectorstore loader to avoid file loading or vector logic
    mock_load_vectorstore.return_value = MagicMock()

    # Mock the stream function to yield a fixed response string (simulate streaming)
    mock_stream.return_value = iter(["This is a mock response."])

    query = "What is AI?"

    # Call the function under test
    result = "".join(response_answer_gr(query))

    # Assert the mocked response appears in the result
    assert "mock response" in result
