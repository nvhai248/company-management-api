from sqlalchemy import Column, String, Enum, DateTime
from sqlalchemy.dialects.postgresql import UUID as SQLAlchemyUUID
from sqlalchemy.ext.declarative import declarative_base
import uuid
import enum
from datetime import datetime

Base = declarative_base()


class Gender(enum.Enum):
    NONE = "NONE"
    FEMALE = "FEMALE"
    MALE = "MALE"


class Author(Base):
    __tablename__ = "authors"

    id = Column(SQLAlchemyUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    full_name = Column(String, nullable=False)
    gender = Column(Enum(Gender), nullable=False, default=Gender.NONE)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)
