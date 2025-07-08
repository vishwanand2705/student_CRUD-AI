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
        for s in memory_store.students.values():
            if s.email == student.email:
                raise ValueError("Email already exists")
        student_id = memory_store.id_counter
        new_student = StudentOut(id=student_id, **student.model_dump())
        memory_store.students[student_id] = new_student
        memory_store.id_counter += 1
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
        
        # Unique email check if email is being updated
        if update_data.email:
            for sid, s in memory_store.students.items():
                if s.email == update_data.email and sid != student_id:
                    raise ValueError("Email already exists")

        updated_data = existing.model_dump()
        for key, value in update_data.model_dump(exclude_unset=True).items():
            updated_data[key] = value

        updated_student = StudentOut(**updated_data)
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
