from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID


class UserModel(BaseModel):
    username: str = Field(min_length=5)
    email: str = Field()
    first_name: str = Field(min_length=3)
    last_name: str = Field(min_length=3)
    hashed_password: str = Field(min_length=3)


class UserViewModel(BaseModel):
    id: UUID
    email: str
    username: str
    first_name: str
    last_name: str
    hashed_password: str
    created_at: datetime | None = None
    updated_at: datetime | None = None

    class Config:
        orm_mode = True
