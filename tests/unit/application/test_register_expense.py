import pytest

from application.use_cases.register_expenses import RegisterExpense
from domain.entities.expenses import Expense
from domain.ports.repositories import FinanceRepository


class FakeFinanceRepository(FinanceRepository):
    def __init__(self):
        self.incomes = []
        self.expenses = []

    # --- Income methods ---
    def save_income(self, income):
        self.incomes.append(income)

    def get_incomes(self):
        return self.incomes
    # --- Expense methods ---
    def save_expense(self, expense):
        self.expenses.append(expense)

    def get_expenses(self):
        return self.expenses

    # --- Summary (requerido por la interfaz) ---
    def get_summary(self):
        return {
            "income": sum(i.amount for i in self.incomes),
            "expenses": sum(e.amount for e in self.expenses),
            "balance": sum(i.amount for i in self.incomes)
            - sum(e.amount for e in self.expenses),
        }




def test_register_expense_successfully():
    repo = FakeFinanceRepository()
    use_case = RegisterExpense(repo)

    result = use_case.execute(
        amount=250.75,
        category="Food",
        description="Groceries",
    )

    assert len(repo.expenses) == 1
    assert repo.expenses[0].amount == 250.75
    assert repo.expenses[0].category == "Food"

    assert result["amount"] == 250.75
    assert result["category"] == "Food"
    assert result["description"] == "Groceries"


def test_register_expense_invalid_amount():
    repo = FakeFinanceRepository()
    use_case = RegisterExpense(repo)

    with pytest.raises(ValueError, match="expense_amount_must_be_positive"):
        use_case.execute(
            amount=0,
            category="Food",
        )


def test_register_expense_category_required():
    repo = FakeFinanceRepository()
    use_case = RegisterExpense(repo)

    with pytest.raises(ValueError, match="expense_category_required"):
        use_case.execute(
            amount=100,
            category="",
        )
