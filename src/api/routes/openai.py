from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, Dict
from src.services.openai import OpenAIService  # Import OpenAI service for handling tasks
from src.utils.logger import logger  # Import logger for logging events

# Define the router for OpenAI routes
router = APIRouter(prefix="/openai", tags=["OpenAI"])

# Define the request model for OpenAI tasks
class OpenAIRequest(BaseModel):
    task: str = Field(..., description="The OpenAI task to perform (e.g., 'generate_text', 'translate_text')")
    text: str = Field(..., description="The input text for the OpenAI task")
    model: str = Field('text-davinci-003', description="The OpenAI model to use. Defaults to 'text-davinci-003'.")
    parameters: Optional[Dict] = Field(None, description="Additional parameters for the OpenAI API call. Refer to OpenAI documentation for available parameters.")


# Define the response model for OpenAI responses
class OpenAIResponse(BaseModel):
    result: str = Field(..., description="The result of the OpenAI task")


# Create a dependency for injecting the OpenAI service
@Depends
def get_openai_service():
    return OpenAIService()


# Define the endpoint for processing OpenAI requests
@router.post("/query")
async def process_openai_query(request: Request, openai_service: OpenAIService = Depends(get_openai_service)):
    """
    Handles OpenAI API requests and returns processed responses.
    """
    try:
        # Parse the request body and validate input
        data = await request.json()
        openai_request = OpenAIRequest(**data)

        # Process the OpenAI request based on the task
        if openai_request.task == 'generate_text':
            result = openai_service.generate_text(openai_request.text, openai_request.model, openai_request.parameters)
        elif openai_request.task == 'translate_text':
            result = openai_service.translate_text(openai_request.text, openai_request.parameters.get('source_language'), openai_request.parameters.get('target_language'))
        elif openai_request.task == 'summarize_text':
            result = openai_service.summarize_text(openai_request.text, openai_request.parameters.get('max_tokens'))
        elif openai_request.task == 'answer_question':
            result = openai_service.answer_question(openai_request.text, openai_request.parameters.get('context'))
        else:
            raise HTTPException(status_code=400, detail="Invalid OpenAI task specified")

        # Return a successful response
        return JSONResponse(OpenAIResponse(result=result).dict())

    except HTTPException as e:
        # Handle invalid requests
        logger.error(f"Invalid OpenAI request: {e}")
        raise

    except Exception as e:
        # Handle unexpected errors
        logger.error(f"Error during OpenAI API call: {e}")
        raise HTTPException(status_code=500, detail="An error occurred during the OpenAI API call")