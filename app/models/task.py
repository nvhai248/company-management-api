from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID

from shared.enums.index import TaskPriority, TaskStatus


class TaskModel(BaseModel):
    summary: str = Field()
    description: str = Field()
    status: TaskStatus = Field()
    priority: TaskPriority = Field()

    class Config:
        use_enum_values = True


class TaskViewModel(BaseModel):
    id: UUID
    summary: str
    description: str
    user_id: UUID
    status: TaskStatus = Field()
    priority: TaskPriority = Field()
    created_at: datetime | None = None
    updated_at: datetime | None = None

    class Config:
        orm_mode = True
        use_enum_values = True
