import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

OLLAMA_API_URL = os.getenv("OLLAMA_API_URL")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL")
OLLAMA_VERSION_URL = os.getenv("OLLAMA_VERSION_URL")
