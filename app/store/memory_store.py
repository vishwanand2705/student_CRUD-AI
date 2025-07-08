"""
In-memory data store for students.

- Uses a global dictionary to store students by ID
- Provides a unique ID counter
- Includes a lock for thread-safe access
"""

from typing import Dict
from threading import Lock
from app.models.student import StudentOut

# Global in-memory store: student_id -> StudentOut
students: Dict[int, StudentOut] = {}

# Unique ID counter for assigning new student IDs
id_counter: int = 1

# Lock for thread-safe access to the store
store_lock = Lock()
