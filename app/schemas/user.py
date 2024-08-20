import uuid
from sqlalchemy import Boolean, Column, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import UUID as SQLAlchemyUUID
from .base_entity import BaseEntity
from passlib.context import CryptContext

Base = declarative_base()


bcrypt_context = CryptContext(schemes=["bcrypt"])


class User(Base, BaseEntity):
    __tablename__ = "users"

    username = Column(String, nullable=False)
    email = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    company_id = Column(
        SQLAlchemyUUID(as_uuid=True), default=uuid.uuid4, nullable=False
    )
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)


def get_password_hash(password):
    return bcrypt_context.hash(password)


def verify_password(plain_password, hashed_password):
    return bcrypt_context.verify(plain_password, hashed_password)
