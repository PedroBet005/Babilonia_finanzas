from uuid import UUID
from domain.repositories.finance_repository import FinanceRepository


class ListCategoriesUseCase:

    def __init__(self, repo: FinanceRepository):
        self.repo = repo

    def execute(self, user_id: UUID):
        categories = self.repo.get_categories_by_user(user_id)
        return [c for c in categories if c.is_active]
