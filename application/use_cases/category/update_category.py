from domain.exceptions import DomainException
from application.dto.category_dto import UpdateCategoryDTO
from domain.repositories.finance_repository import FinanceRepository


class UpdateCategoryUseCase:

    def __init__(self, repo: FinanceRepository):
        self.repo = repo

    def execute(self, dto: UpdateCategoryDTO):

        category = self.repo.get_category_by_id(dto.category_id)

        if not category:
            raise DomainException("Category not found")

        if category.user_id != dto.user_id:
            raise DomainException("Unauthorized")

        category.name = dto.name.lower()

        self.repo.update_category(category)

        return category
