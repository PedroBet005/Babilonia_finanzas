from uuid import UUID
from domain.exceptions import DomainException
from domain.repositories.finance_repository import FinanceRepository


class DeleteCategoryUseCase:

    def __init__(self, repo: FinanceRepository):
        self.repo = repo

    def execute(self, category_id: UUID, user_id: UUID):

        category = self.repo.get_category_by_id(category_id)

        if not category:
            raise DomainException("Category not found")

        if category.user_id != user_id:
            raise DomainException("Unauthorized")

        category.deactivate()
        self.repo.update_category(category)
