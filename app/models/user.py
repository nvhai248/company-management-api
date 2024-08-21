from pydantic import BaseModel, Field, EmailStr
from datetime import datetime
from uuid import UUID
from typing import Optional


class UserBaseModel(BaseModel):
    username: str = Field(min_length=5)
    email: EmailStr
    first_name: str = Field(min_length=3)
    company_id: Optional[UUID]
    last_name: str = Field(min_length=3)


class UserModel(UserBaseModel):
    pass


class UserViewModel(UserBaseModel):
    id: UUID
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True
        from_attributes = True
