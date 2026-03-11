import pytest

from application.use_cases.get_balance import GetBalance
from domain.ports.repositories import FinanceRepository


class FakeFinanceRepository(FinanceRepository):
    def get_summary(self):
        return {
            "income": 1000.0,
            "expenses": 400.0,
            "savings": 100.0,
            "tithe": 100.0,
            "debts": 0.0,
            "balance": 400.0,
        }

    # Métodos obligatorios por la interfaz (no usados aquí)
    def save_income(self, income):
        pass

    def save_expense(self, expense):
        pass

    def get_incomes(self):
        return []

    def get_expenses(self):
        return []


def test_get_balance_successfully():
    repo = FakeFinanceRepository()
    use_case = GetBalance(repo)

    result = use_case.execute()

    assert result["income"] == 1000.0
    assert result["expenses"] == 400.0
    assert result["balance"] == 400.0
