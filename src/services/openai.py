"""
This module provides an interface for interacting with the OpenAI API, handling various AI tasks 
like text generation, translation, summarization, and question answering.

This service adheres to the following principles:

- **Robust Error Handling**: Ensures graceful management of API errors and unexpected responses.
- **Efficient Performance**: Optimizes API call usage and response processing for fast results.
- **Security**: Implements best practices for data security and API key handling.
- **Scalability**:  Designed to handle increasing traffic and demand as user needs grow.

This module integrates with other components of the MVP:

- `src/api/routes/openai.py`: Defines API routes for user requests and calls OpenAI service functions.
- `src/utils/logger.py`: Handles logging events, providing insights into API calls and errors. 

"""

import os
import openai
from typing import Dict, Optional
from src.utils.logger import logger  # Import the logger for logging events

# Retrieve API Key from Environment Variables (Ensure security by not hardcoding)
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Error handling for missing API key
if not OPENAI_API_KEY:
    raise ValueError('OpenAI API Key not found in environment variables. Please set OPENAI_API_KEY.')

# Initialize OpenAI Client
openai.api_key = OPENAI_API_KEY

class OpenAIService:
    """
    A class that encapsulates the logic for interacting with the OpenAI API. 
    Provides functions for performing various AI tasks like text generation, translation, 
    summarization, and question answering.
    """

    def __init__(self):
        """
        Initializes the OpenAIService.
        """
        pass

    def generate_text(self, prompt: str, model: str = 'text-davinci-003', parameters: Optional[Dict] = None) -> str:
        """
        Generates text using the specified OpenAI model based on the provided prompt.

        Args:
            prompt (str): The text prompt for the AI model to process.
            model (str, optional): The OpenAI model to use. Defaults to 'text-davinci-003'.
            parameters (Optional[Dict], optional): Additional parameters for the OpenAI API call.
                Refer to OpenAI documentation for available parameters. Defaults to None.

        Returns:
            str: The generated text response from the OpenAI API.

        Raises:
            Exception: Raises an exception if the OpenAI API call fails or if there are issues with the response.
        """
        try:
            logger.info(f'Generating text using OpenAI model: {model}')  # Log the API call
            response = openai.Completion.create(
                engine=model,
                prompt=prompt,
                max_tokens=1000,  # Adjust max_tokens as needed
                temperature=0.7,  # Control randomness and creativity
                top_p=1,  # Control the diversity of generated text
                frequency_penalty=0,  # Adjust frequency penalty for repetitive text
                presence_penalty=0,  # Adjust presence penalty for repetitive text
                **parameters  # Include any additional parameters from the user request
            )
            # Log successful API call and return response 
            logger.info(f'OpenAI API call successful for model: {model}') 
            return response.choices[0].text 
        except Exception as e:
            logger.error(f'Error during OpenAI API call: {e}')  # Log the error 
            raise  # Re-raise the exception

    def translate_text(self, text: str, source_language: str, target_language: str) -> str:
        """
        Translates text from one language to another using OpenAI's translation capabilities.

        Args:
            text (str): The text to be translated.
            source_language (str): The source language of the text.
            target_language (str): The target language for translation.

        Returns:
            str: The translated text.

        Raises:
            Exception: Raises an exception if the OpenAI API call fails or if there are issues with the response.
        """
        try:
            logger.info(f'Translating text from {source_language} to {target_language}')
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "user", "content": f'Translate the following from {source_language} to {target_language}: {text}'}
                ]
            )
            logger.info(f'OpenAI API call successful for translation')
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f'Error during OpenAI translation API call: {e}')
            raise 

    def summarize_text(self, text: str, max_tokens: Optional[int] = None) -> str:
        """
        Summarizes the provided text using OpenAI's summarization capabilities.

        Args:
            text (str): The text to be summarized.
            max_tokens (Optional[int], optional): The maximum number of tokens for the summary. 
                Defaults to None, which automatically determines the optimal length.

        Returns:
            str: The summarized text.

        Raises:
            Exception: Raises an exception if the OpenAI API call fails or if there are issues with the response.
        """
        try:
            logger.info(f'Summarizing text with max_tokens: {max_tokens}')
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "user", "content": f'Summarize the following text: {text}'}
                ]
            )
            logger.info(f'OpenAI API call successful for summarization')
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f'Error during OpenAI summarization API call: {e}')
            raise 

    def answer_question(self, question: str, context: Optional[str] = None) -> str:
        """
        Answers a question using OpenAI's question answering capabilities.

        Args:
            question (str): The question to be answered.
            context (Optional[str], optional): Optional context to provide for the question.
                Defaults to None, which will use the question itself as context.

        Returns:
            str: The answer to the question.

        Raises:
            Exception: Raises an exception if the OpenAI API call fails or if there are issues with the response.
        """
        try:
            logger.info(f'Answering question: {question} with context: {context}')
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "user", "content": f'Answer the following question: {question}. Context: {context}'}
                ]
            )
            logger.info(f'OpenAI API call successful for question answering')
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f'Error during OpenAI question answering API call: {e}')
            raise 

# Example Usage (For testing and demonstration)
if __name__ == '__main__':
    openai_service = OpenAIService()
    print(openai_service.generate_text(prompt='Write a short story about a cat.'))
    print(openai_service.translate_text(text='Hello world!', source_language='english', target_language='spanish'))
    print(openai_service.summarize_text(text='This is a long text to be summarized.'))
    print(openai_service.answer_question(question='What is the capital of France?'))