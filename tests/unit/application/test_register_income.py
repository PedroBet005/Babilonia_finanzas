import pytest

from application.use_cases.register_incomes import RegisterIncome
from domain.entities.incomes import Income


class FakeFinanceRepository:
    def __init__(self):
        self.incomes = []

    def save_income(self, income: Income):
        self.incomes.append(income)


def test_register_income_successfully():
    repo = FakeFinanceRepository()
    use_case = RegisterIncome(repo)

    result = use_case.execute(
        amount=1000,
        source="Salary",
        apply_tithe=False,
        apply_debt=False,
    )

    assert len(repo.incomes) == 1
    assert repo.incomes[0].amount == 1000
    assert result["available"] == 900.0


def test_register_income_invalid_amount():
    repo = FakeFinanceRepository()
    use_case = RegisterIncome(repo)

    with pytest.raises(ValueError, match="income_amount_must_be_positive"):
        use_case.execute(
            amount=0,
            source="Salary",
            apply_tithe=False,
            apply_debt=False,
        )
