from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID


class BookModel(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(min_length=3)
    author_id: UUID = Field(default_factory=UUID)


class BookViewModel(BaseModel):
    id: UUID
    title: str
    description: str
    author_id: UUID
    created_at: datetime | None = None
    updated_at: datetime | None = None

    class Config:
        orm_mode = True
