from sqlalchemy import Column, Enum, Float, String
from sqlalchemy.ext.declarative import declarative_base

from shared.enums.index import CompanyMode
from .base_entity import BaseEntity
from sqlalchemy.dialects.postgresql import UUID as SQLAlchemyUUID
import uuid

Base = declarative_base()


class Book(Base, BaseEntity):
    __tablename__ = "books"

    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    mode = Column(Enum(CompanyMode), nullable=False)
    rating = Column(Float, nullable=False)
