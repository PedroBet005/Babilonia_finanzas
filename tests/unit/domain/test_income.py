import pytest
from datetime import datetime

from domain.entities.incomes import Income


def test_income_amount_must_be_positive():
    with pytest.raises(ValueError, match="income_amount_must_be_positive"):
        Income(amount=0, source="Salary")


def test_income_source_required():
    with pytest.raises(ValueError, match="income_source_required"):
        Income(amount=100, source="")


def test_income_created_successfully():
    income = Income(amount=1500, source="Salary")

    assert income.amount == 1500
    assert income.source == "Salary"
    assert isinstance(income.date, datetime)
