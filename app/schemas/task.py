import uuid
from sqlalchemy import Column, String, Enum
from sqlalchemy.ext.declarative import declarative_base

from shared.enums import TaskPriority, TaskStatus
from sqlalchemy.dialects.postgresql import UUID as SQLAlchemyUUID
from .base_entity import BaseEntity


Base = declarative_base()


class Task(Base, BaseEntity):
    __tablename__ = "tasks"

    summary = Column(String, nullable=False)
    description = Column(String, nullable=False)
    status = Column(Enum(), nullable=TaskStatus, default=TaskStatus.ACTIVE)
    priority = Column(Enum(), nullable=TaskPriority, default=TaskPriority.HIGHEST)
    user_id = Column(SQLAlchemyUUID(as_uuid=True), default=uuid.uuid4, nullable=False)
