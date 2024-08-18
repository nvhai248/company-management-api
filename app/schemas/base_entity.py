from datetime import datetime
import uuid
from sqlalchemy import Column, DateTime
from sqlalchemy.dialects.postgresql import UUID as SQLAlchemyUUID


class BaseEntity:
    id = Column(SQLAlchemyUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)
