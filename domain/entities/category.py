# domain/entities/category.py

from dataclasses import dataclass
from datetime import datetime
from uuid import UUID, uuid4
from enum import Enum


class CategoryType(str, Enum):
    INCOMES = "incomes"
    EXPENSES = "expenses"


@dataclass
class Category:
    id: UUID
    name: str
    type: CategoryType
    user_id: UUID
    is_active: bool
    created_at: datetime

    @staticmethod
    def create(name: str, type: CategoryType, user_id: UUID) -> "Category":
        return Category(
            id=uuid4(),
            name=name.strip().lower(),
            type=type,
            user_id=user_id,
            is_active=True,
            created_at=datetime.utcnow()
        )

    def deactivate(self):
        self.is_active = False

