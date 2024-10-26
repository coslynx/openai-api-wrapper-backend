import pytest
from src.services.openai import OpenAIService
from unittest.mock import patch, MagicMock

# Constants and Configurations
API_KEY = "YOUR_OPENAI_API_KEY"  # Replace with your actual API key
MODEL = "text-davinci-003"

# Data for Testing
TEST_TEXT = "This is a test text."
TEST_PROMPT = "Summarize this text: " + TEST_TEXT
TEST_PARAMETERS = {"max_tokens": 100}
EXPECTED_RESPONSE = "This is a summary of the test text."  # Expected output from the model

# Mock Responses
MOCK_OPENAI_RESPONSE = {
    "choices": [{"text": EXPECTED_RESPONSE}],
}


@pytest.fixture
def openai_service():
    """
    Fixture to create an instance of the OpenAIService for testing.
    """
    service = OpenAIService(api_key=API_KEY)
    return service


# Test Cases for the OpenAI Service
@patch("openai.Completion.create")
def test_generate_text(mock_create_completion, openai_service):
    """
    Test the generate_text function with a valid prompt and parameters.
    """
    mock_create_completion.return_value = MagicMock(data=MOCK_OPENAI_RESPONSE)
    response = openai_service.generate_text(
        prompt=TEST_PROMPT, model=MODEL, parameters=TEST_PARAMETERS
    )
    assert response == EXPECTED_RESPONSE


@patch("openai.Completion.create")
def test_generate_text_invalid_model(mock_create_completion, openai_service):
    """
    Test the generate_text function with an invalid model.
    """
    mock_create_completion.side_effect = Exception("Invalid model")
    with pytest.raises(Exception) as exc_info:
        openai_service.generate_text(
            prompt=TEST_PROMPT, model="invalid-model", parameters=TEST_PARAMETERS
        )
    assert "Invalid model" in str(exc_info.value)


@patch("openai.Completion.create")
def test_generate_text_api_error(mock_create_completion, openai_service):
    """
    Test the generate_text function when the OpenAI API call fails.
    """
    mock_create_completion.side_effect = Exception("API Error")
    with pytest.raises(Exception) as exc_info:
        openai_service.generate_text(
            prompt=TEST_PROMPT, model=MODEL, parameters=TEST_PARAMETERS
        )
    assert "API Error" in str(exc_info.value)