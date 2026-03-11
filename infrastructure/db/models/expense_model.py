import uuid

from sqlalchemy import Column, Float, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from infrastructure.db.session import Base


class ExpenseModel(Base):
    __tablename__ = "expenses"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    amount = Column(Float, nullable=False)
    description = Column(String)
    user_id = Column(UUID(as_uuid=True), nullable=False)
    category_id = Column(UUID(as_uuid=True))
    created_at = Column(DateTime(timezone=True),server_default=func.now(),)
