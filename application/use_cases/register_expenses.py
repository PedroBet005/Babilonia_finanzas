from domain.entities.expenses import Expense
from domain.entities.category import CategoryType
from domain.exceptions import DomainException
from domain.ports.repositories import FinanceRepository


class RegisterExpense:
    def __init__(self, repo: FinanceRepository):
        self.repo = repo

    def execute(
        self,
        amount: float,
        category_id: str,
        user_id: str,
        description: str | None = None,
    ) -> dict:

        # 1️⃣ VALIDAR CATEGORÍA
        category = self.repo.get_category_by_id(category_id)

        if not category:
            raise DomainException("Category not found")

        if category.user_id != user_id:
            raise DomainException("Unauthorized")

        if not category.is_active:
            raise DomainException("Category inactive")

        if category.type != CategoryType.EXPENSE:
            raise DomainException("Invalid category type")

        # 2️⃣ crear Expense
        expense = Expense(
            amount=amount,
            category_id=category_id,
            description=description,
        )

        # 3️⃣ persistir
        self.repo.save_expense(expense)

        return expense.to_dict()

