from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID


class UserModel(BaseModel):
    username: str = Field(min_length=3)
    email: str = Field(min_length=3)
    first_name: str = Field(min_length=3)
    last_name: str = Field(min_length=3)
    password: str = Field(min_length=3)


class UserViewModel(BaseModel):
    id: UUID
    email: str
    username: str
    first_name: str
    last_name: str
    password: str
    created_at: datetime | None = None
    updated_at: datetime | None = None

    class Config:
        orm_mode = True
