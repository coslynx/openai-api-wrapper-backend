import logging
import os
from logging.handlers import RotatingFileHandler

# Configure logger for the AI Backend

# Set logging level based on environment variable
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
LOG_LEVEL = getattr(logging, LOG_LEVEL, logging.INFO)

# Create logger
logger = logging.getLogger(__name__)
logger.setLevel(LOG_LEVEL)

# Create file handler for rotating logs
formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
file_handler = RotatingFileHandler(
    "logs/backend.log", maxBytes=1024 * 1024 * 10, backupCount=5
)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# Create console handler for displaying logs in the console
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)