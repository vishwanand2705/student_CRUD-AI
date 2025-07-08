"""
Core CRUD logic for Student resource.

- Lock management for thread safety
- Read/write from in-memory store
"""

from app.models.student import StudentCreate, StudentUpdate, StudentOut
from typing import List
from app.store import memory_store


def create_student(student: StudentCreate) -> StudentOut:
    """
    Create a new student, ensuring unique email.
    """
    with memory_store.store_lock:
        email_lower = student.email.lower()
        
        # Check for existing email
        for existing_student in memory_store.students.values():
            if existing_student.email == email_lower:
                raise ValueError("Email already exists")
        
        # Create new student with normalized email and auto-generated ID
        student_id = memory_store.id_counter
        memory_store.id_counter += 1
        
        new_student = StudentOut(
            id=student_id,
            email=email_lower,
            **student.model_dump(exclude={"email"})
        )
        
        memory_store.students[student_id] = new_student
        return new_student

def get_all_students() -> List[StudentOut]:
    """
    Retrieve all students.
    """
    with memory_store.store_lock:
        return list(memory_store.students.values())

def get_student_by_id(student_id: int) -> StudentOut | None:
    """
    Retrieve a student by ID.
    """
    with memory_store.store_lock:
        return memory_store.students.get(student_id)

def update_student(student_id: int, update_data: StudentUpdate) -> StudentOut | None:
    """
    Update a student's details, ensuring unique email if changed.
    """
    with memory_store.store_lock:
        existing = memory_store.students.get(student_id)
        if not existing:
            return None
        
        # Get only the fields that are being updated
        update_dict = update_data.model_dump(exclude_unset=True)
        
        # Handle email uniqueness check and normalization
        if "email" in update_dict:
            email_lower = update_dict["email"].lower()
            # Check for duplicates only if email is actually changing
            if email_lower != existing.email:
                for sid, student in memory_store.students.items():
                    if student.email == email_lower and sid != student_id:
                        raise ValueError("Email already exists")
            update_dict["email"] = email_lower
        
        # Create updated student using model_copy with updates
        updated_student = existing.model_copy(update=update_dict)
        memory_store.students[student_id] = updated_student
        return updated_student

def delete_student(student_id: int) -> bool:
    """
    Delete a student by ID.
    Returns True if deleted, False if not found.
    """
    with memory_store.store_lock:
        if student_id in memory_store.students:
            del memory_store.students[student_id]
            return True
        return False
