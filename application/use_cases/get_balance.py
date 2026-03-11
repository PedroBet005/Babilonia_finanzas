from domain.ports.repositories import FinanceRepository


class GetBalance:

    def __init__(self, repo):
        self.repo = repo

    def execute(self):
        summary = self.repo.get_summary()

        income = summary.get("income", 0)
        expenses = summary.get("expenses", 0)
        savings = summary.get("savings", 0)
        tithe = summary.get("tithe", 0)
        debts = summary.get("debts", 0)

        balance = income - expenses - savings - tithe - debts

        return {
            "income": income,
            "expenses": expenses,
            "savings": savings,
            "tithe": tithe,
            "debts": debts,
            "balance": balance,
        }


