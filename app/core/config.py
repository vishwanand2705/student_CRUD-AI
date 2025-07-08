import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

OLLAMA_MODEL = os.getenv("OLLAMA_MODEL")
OLLAMA_API = os.getenv("OLLAMA_API")
