from datetime import datetime
import enum
from pydantic import BaseModel, Field
from uuid import UUID  # Import UUID from standard library


class Gender(enum.Enum):
    NONE = "NONE"
    FEMALE = "FEMALE"
    MALE = "MALE"


class AuthorModel(BaseModel):
    full_name: str = Field(min_length=3)
    gender: Gender = Field(default=Gender.NONE)  # Use Pydantic's enum


class AuthorViewModel(BaseModel):
    id: UUID
    full_name: str
    gender: Gender = Gender.NONE
    created_at: datetime | None = None

    class Config:  # Correct the config class name to 'Config'
        orm_mode = True  # Fix 'orm_map' to 'orm_mode' which is the correct attribute
