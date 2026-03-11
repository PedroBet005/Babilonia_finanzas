from domain.entities.category import Category
from domain.exceptions import DomainException
from application.dto.category_dto import CreateCategoryDTO
from domain.repositories.finance_repository import FinanceRepository


class CreateCategoryUseCase:

    def __init__(self, repo: FinanceRepository):
        self.repo = repo

    def execute(self, dto: CreateCategoryDTO):
        categories = self.repo.get_categories_by_user(dto.user_id)

        for cat in categories:
            if cat.name == dto.name.lower() and cat.type == dto.type and cat.is_active:
                raise DomainException("Category already exists")

        category = Category.create(dto.name, dto.type, dto.user_id)
        self.repo.create_category(category)

        return category
