from typing import List

from domain.entities.incomes import Income
from domain.entities.expenses import Expense
from domain.services.babylonian_rules import BabylonianRules, BabylonianDistribution
from domain.ports.repositories import FinanceRepository


class BalanceService:
    """
    Coordinates financial operations and balance calculations.
    """

    def __init__(self, repository: FinanceRepository):
        self.repository = repository

    def register_income(
        self,
        income: Income,
        apply_tithe: bool = False,
        apply_debt: bool = False,
    ) -> BabylonianDistribution:
        distribution = BabylonianRules.apply(
            amount=income.amount,
            apply_tithe=apply_tithe,
            apply_debt=apply_debt,
        )

        self.repository.save_income(income)

        return distribution

    def register_expense(self, expense: Expense) -> None:
        self.repository.save_expense(expense)

    def get_balance(self) -> float:
        incomes: List[Income] = self.repository.get_incomes()
        expenses: List[Expense] = self.repository.get_expenses()

        total_income = sum(i.amount for i in incomes)
        total_expenses = sum(e.amount for e in expenses)

        return round(total_income - total_expenses, 2)

