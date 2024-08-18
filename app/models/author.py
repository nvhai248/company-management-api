from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID

from shared.enums.index import Gender


class AuthorModel(BaseModel):
    full_name: str = Field(min_length=3)
    gender: Gender = Field(default=Gender.NONE)

    class Config:
        use_enum_values = True


class AuthorViewModel(BaseModel):
    id: UUID
    full_name: str
    gender: Gender = Gender.NONE
    created_at: datetime | None = None
    updated_at: datetime | None = None

    class Config:
        orm_mode = True
        use_enum_values = True
