import pytest
from datetime import datetime

from domain.entities.expenses import Expense


def test_expense_amount_must_be_positive():
    with pytest.raises(ValueError, match="expense_amount_must_be_positive"):
        Expense(amount=0, category="Food")


def test_expense_category_required():
    with pytest.raises(ValueError, match="expense_category_required"):
        Expense(amount=50, category="")


def test_expense_created_successfully():
    expense = Expense(
        amount=75.5,
        category="Food",
        description="Lunch"
    )

    assert expense.amount == 75.5
    assert expense.category == "Food"
    assert expense.description == "Lunch"
    assert isinstance(expense.date, datetime)
