from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base
from .base_entity import BaseEntity
from sqlalchemy.dialects.postgresql import UUID as SQLAlchemyUUID
import uuid

Base = declarative_base()


class Book(Base, BaseEntity):
    __tablename__ = "books"

    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    author_id = Column(SQLAlchemyUUID(as_uuid=True), default=uuid.uuid4, nullable=False)
