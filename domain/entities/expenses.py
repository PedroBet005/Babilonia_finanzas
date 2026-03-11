from datetime import datetime, timezone
from typing import Optional


class Expense:
    """
    Represents an expense entry in the financial domain.
    """

    def __init__(
        self,
        amount: float,
        category_id: str,
        description: Optional[str] = None,
        date: Optional[datetime] = None,
    ):
        if amount <= 0:
            raise ValueError("expense_amount_must_be_positive")

        if not category_id:
            raise ValueError("expense_category_required")

        self.amount: float = round(amount, 2)
        self.category_id: str = category_id
        self.description: Optional[str] = description
        self.date: datetime = date or datetime.now(timezone.utc)

    # -------- serialización --------

    def to_dict(self) -> dict:
        return {
            "amount": self.amount,
            "category_id": self.category_id,
            "description": self.description,
            "date": self.date.isoformat(),
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Expense":
        return cls(
            amount=data["amount"],
            category_id=data["category_id"],
            description=data.get("description"),
            date=datetime.fromisoformat(data["date"]),
        )

    def __repr__(self) -> str:
        return (
            f"Expense(amount={self.amount}, "
            f"category_id='{self.category_id}', "
            f"date='{self.date.isoformat()}')"
        )
