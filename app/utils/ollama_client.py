"""
Ollama client utility functions.

- Builds prompt for AI summary
- Handles Ollama API requests and errors
"""

import logging
import requests
from app.models.student import StudentOut
from app.core.config import OLLAMA_API_URL, OLLAMA_MODEL, OLLAMA_VERSION_URL

logger = logging.getLogger("ollama_client")

def check_ollama_version() -> bool:
    """
    Check if the Ollama API server is reachable and running.
    """
    try:
        resp = requests.get(OLLAMA_VERSION_URL, timeout=5)

        resp.raise_for_status()
        return True
    except Exception:
        return False

def build_prompt(student: StudentOut) -> str:
    """
    Build a prompt string for the Ollama model based on student details.
    """
    return (
        f"""
        Create a professional student profile summary for:
        
        Name: {student.name}
        Age: {student.age}
        Email: {student.email}
        
        Generate a brief, professional summary (2-3 sentences) that highlights:
        - Their academic potential
        - Communication readiness
        - Any relevant observations based on their profile
        
        Keep it positive and professional.
        """
    )


def generate_student_summary(student: StudentOut) -> str:
    """
    Generate an AI summary for a student using the Ollama API.
    Handles connection, timeout, and server errors gracefully.
    """
    if not check_ollama_version():
        return "Ollama API is not reachable or not running."

    prompt = build_prompt(student)
    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt.strip(),
        "stream": False
    }

    try:
        response = requests.post(OLLAMA_API_URL, json=payload, timeout=10)
        if response.status_code == 500:
            logger.error(f"Ollama API returned status {response.status_code}: {response.text}")
            return f"Ollama API returned status {response.status_code}"
        response.raise_for_status()
        result = response.json()
        return result.get("response", "No summary returned.")
    except requests.exceptions.Timeout as e:
        logger.error(f"Ollama request timed out: {e}")
        return "Ollama request timed out."
    except requests.exceptions.RequestException as e:
        logger.error(f"Ollama request error: {e}")
        return f"Ollama error: {str(e)}"
    except Exception as e:
        logger.error(f"Unexpected error from Ollama: {e}")
        return f"Unexpected error: {str(e)}"
