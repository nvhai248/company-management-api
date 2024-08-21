from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID

from shared.enums import CompanyMode


class CompanyModel(BaseModel):
    name: str = Field(min_length=3)
    description: str = Field()
    mode: CompanyMode = Field(default=CompanyMode.ACTIVE)
    rating: float = Field()

    class Config:
        use_enum_values = True


class CompanyViewModel(BaseModel):
    id: UUID
    name: str
    description: str
    mode: CompanyMode = CompanyMode.ACTIVE
    created_at: datetime | None = None
    updated_at: datetime | None = None

    class Config:
        orm_mode = True
        use_enum_values = True
        from_attributes = True
