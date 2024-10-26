import os
import uvicorn
from fastapi import FastAPI
from src.api.routes.openai import router as openai_router
from src.services.openai import OpenAIService
from src.utils.logger import logger
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env

# Create the FastAPI application
app = FastAPI(
    title="AI Backend for OpenAI Queries",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Register the OpenAI API routes
app.include_router(openai_router)

# Create dependencies for injecting the OpenAI service and logger
@app.on_event("startup")
async def startup_event():
    app.state.openai_service = OpenAIService()  # Initialize OpenAI service
    app.state.logger = logger  # Inject the logger

# Start the server using uvicorn
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8000)),
        reload=True,  # Enable hot reloading for development
    )