"""
Main entry point for the Student Details FastAPI application.

- Creates FastAPI instance
- Adds logging middleware
- Includes student routes
"""

from fastapi import FastAPI
from app.routes import student_routes
from app.core.middleware import LoggingMiddleware 
from fastapi.middleware.cors import CORSMiddleware

# Initialize FastAPI app
app = FastAPI(title="Student API with Ollama")

# Allow all origins (for development)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add custom logging middleware
app.add_middleware(LoggingMiddleware)

# Register student-related routes
app.include_router(student_routes.router)

# Health check endpoint
@app.get("/ping", tags=["Health Check"])
def ping():
    return {"message": "Server is up and running!"}