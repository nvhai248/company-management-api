from sqlalchemy import Column, Enum, Float, String
from sqlalchemy.ext.declarative import declarative_base

from shared.enums import CompanyMode
from .base_entity import BaseEntity
from sqlalchemy.dialects.postgresql import UUID as SQLAlchemyUUID
import uuid

Base = declarative_base()


class Company(Base, BaseEntity):
    __tablename__ = "companies"

    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    mode = Column(Enum(CompanyMode), nullable=False)
    rating = Column(Float, nullable=False)
