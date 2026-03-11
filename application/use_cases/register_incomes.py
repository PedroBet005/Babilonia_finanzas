from domain.entities.incomes import Income
from domain.entities.category import CategoryType
from domain.exceptions import DomainException
from domain.ports.repositories import FinanceRepository
from domain.services.babylonian_rules import apply_babylonian_rules


class RegisterIncome:
    def __init__(self, repo: FinanceRepository):
        self.repo = repo

    def execute(
        self,
        amount: float,
        source: str,
        category_id: str,
        user_id: str,
        apply_tithe: bool,
        apply_debt: bool,
    ) -> dict:

        # 1️⃣ VALIDAR CATEGORÍA
        category = self.repo.get_category_by_id(category_id)

        if not category:
            raise DomainException("Category not found")

        if category.user_id != user_id:
            raise DomainException("Unauthorized")

        if not category.is_active:
            raise DomainException("Category inactive")

        if category.type != CategoryType.INCOME:
            raise DomainException("Invalid category type")

        # 2️⃣ crear Income
        income = Income(
            amount=amount,
            source=source,
            category_id=category_id,
        )

        # 3️⃣ aplicar reglas de Babilonia
        distribution = apply_babylonian_rules(
            amount=income.amount,
            tithe=apply_tithe,
            debt=apply_debt,
        )

        # 4️⃣ persistir
        self.repo.save_income(income)

        return {
            **distribution,
            "income": income.to_dict(),
        }
