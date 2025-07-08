"""
Pydantic models for Student resource.

- Centralized validation for input/output
- Shared base model for common fields
"""

import re
from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional

# Base model for common student attributes and validation
class StudentBase(BaseModel):
    name: str = Field(..., example="John Doe", min_length=3, max_length=50)
    age: int = Field(..., gt=0, lt=130, example=21)
    email: EmailStr = Field(..., example="john.doe@example.com")

    @field_validator("name")
    @classmethod
    def name_must_be_alpha(cls, v):
        if not re.match(r"^[A-Za-z ]+$", v):
            raise ValueError("Name must contain only letters and spaces")
        return v

    class Config:
        extra = "forbid" # Forbid extra fields in input


# Model for creating a student 
class StudentCreate(StudentBase):
    pass


# Model for updating a student 
class StudentUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=3, max_length=50)
    age: Optional[int] = Field(None, gt=0, lt=130)
    email: Optional[EmailStr] = None


# Model for output/response
class StudentOut(StudentBase):
    id: int
