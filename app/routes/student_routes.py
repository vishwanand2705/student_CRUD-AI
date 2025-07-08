"""
All /students endpoints

Delegates logic to service layer
"""

from fastapi import APIRouter, HTTPException, Path, status, Response
from typing import List
from app.models.student import StudentCreate, StudentUpdate, StudentOut
from app.services import student_service
from app.utils.ollama_client import generate_student_summary

router = APIRouter(
    prefix="/students",
    tags=["Students"]
)

# Dummy route just for setup testing
@router.get("/test")
def test_route():
    """Test if student router is working."""
    return {"message": "Student router is working!"}

@router.post("/", response_model=StudentOut, status_code=status.HTTP_201_CREATED)
def create_student(student: StudentCreate):
    """
    Create a new student. Returns 409 if email already exists.
    """
    try:
        return student_service.create_student(student)
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))

@router.get("/", response_model=List[StudentOut])
def get_all_students():
    """
    Retrieve all students.
    """
    return student_service.get_all_students()

@router.get("/{id}", response_model=StudentOut)
def get_student(id: int = Path(..., gt=0)):
    """
    Retrieve a student by ID. Returns 404 if not found.
    """
    student = student_service.get_student_by_id(id)
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

@router.put("/{id}", response_model=StudentOut)
def update_student(id: int, student_data: StudentUpdate):
    """
    Update a student's details. Returns 404 if not found, 409 if email exists.
    """
    try:
        updated = student_service.update_student(id, student_data)
        if updated is None:
            raise HTTPException(status_code=404, detail="Student not found")
        return updated
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))
    
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_student(id: int):
    """
    Delete a student by ID. Returns 404 if not found.
    """
    success = student_service.delete_student(id)
    if not success:
        raise HTTPException(status_code=404, detail="Student not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.get("/{id}/summary", tags=["AI Summary"])
def get_student_summary(id: int = Path(..., gt=0)):
    """
    Get an AI-generated summary for a student. Returns 404 if not found, 502 for Ollama errors.
    """
    student = student_service.get_student_by_id(id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    summary = generate_student_summary(student)
    if summary.startswith("Ollama API is not reachable") or \
       summary.startswith("Ollama API returned a server error") or \
       summary.startswith("Ollama error:") or \
       summary.startswith("Ollama request timed out.") or \
       summary.startswith("Unexpected error:"):
        raise HTTPException(status_code=502, detail=summary)
    return {"summary": summary}
