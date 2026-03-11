from abc import ABC, abstractmethod
from uuid import UUID

from domain.entities.category import Category


class FinanceRepository(ABC):

    # CATEGORY METHODS

    @abstractmethod
    def create_category(self, category: Category) -> None:
        pass

    @abstractmethod
    def get_categories_by_user(self, user_id: UUID) -> list[Category]:
        pass

    @abstractmethod
    def get_category_by_id(self, category_id: UUID) -> Category | None:
        pass

    @abstractmethod
    def update_category(self, category: Category) -> None:
        pass