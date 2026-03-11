from domain.repositories.finance_repository import FinanceRepository
from domain.entities.category import Category


class InMemoryFinanceRepository(FinanceRepository):
    def __init__(self):
        self._incomes = []
        self._expenses = []
        self._categories: list[Category] = []

    # =========================
    # INCOME
    # =========================
    def save_income(self, income) -> None:
        self._incomes.append(income)

    def get_incomes(self):
        return self._incomes

    # =========================
    # EXPENSE
    # =========================
    def save_expense(self, expense) -> None:
        self._expenses.append(expense)

    def get_expenses(self):
        return self._expenses

    # =========================
    # SUMMARY
    # =========================
    def get_summary(self) -> dict:
        total_income = sum(i.amount for i in self._incomes)
        total_expenses = sum(e.amount for e in self._expenses)

        return {
            "income": total_income,
            "expenses": total_expenses,
            "balance": total_income - total_expenses,
        }

    # =========================
    # CATEGORIES
    # =========================
    def create_category(self, category) -> None:
        self._categories.append(category)

    def get_categories_by_user(self, user_id):
        return [c for c in self._categories if c.user_id == user_id]

    def get_category_by_id(self, category_id):
        for c in self._categories:
            if c.id == category_id:
                return c
        return None

    def update_category(self, category) -> None:
        for i, c in enumerate(self._categories):
            if c.id == category.id:
                self._categories[i] = category
                break
