from sqlalchemy import Column, String, Enum
from sqlalchemy.ext.declarative import declarative_base

from shared.enums.index import Gender
from .base_entity import BaseEntity


Base = declarative_base()


class Author(Base, BaseEntity):
    __tablename__ = "authors"

    full_name = Column(String, nullable=False)
    gender = Column(Enum(Gender), nullable=False, default=Gender.NONE)
