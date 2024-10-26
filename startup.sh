#!/bin/bash

# Startup script for AI Backend for OpenAI Queries MVP

set -e

echo "Starting AI Backend for OpenAI Queries..."

# Source environment variables
if [ -f .env ]; then
  source .env
fi

# Start the backend server
echo "Starting backend server..."
uvicorn main:app --host 0.0.0.0 --port $PORT --reload &

# Check if backend server is running
sleep 2
if ps aux | grep -q "uvicorn main:app"; then
  echo "Backend server started successfully."
else
  echo "Backend server failed to start."
  exit 1
fi

echo "AI Backend for OpenAI Queries started successfully."