from datetime import datetime, timezone
from typing import Optional


class Income:
    """
    Represents an income entry in the financial domain.
    """

    def __init__(
        self,
        amount: float,
        source: str,
        category_id: str,
        date: Optional[datetime] = None,
    ):
        if amount <= 0:
            raise ValueError("income_amount_must_be_positive")

        if not source:
            raise ValueError("income_source_required")

        if not category_id:
            raise ValueError("income_category_required")

        self.amount: float = round(amount, 2)
        self.source: str = source
        self.category_id: str = category_id
        self.date: datetime = date or datetime.now(timezone.utc)

    # -------- serialización --------

    def to_dict(self) -> dict:
        return {
            "amount": self.amount,
            "source": self.source,
            "category_id": self.category_id,
            "date": self.date.isoformat(),
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Income":
        return cls(
            amount=data["amount"],
            source=data["source"],
            category_id=data["category_id"],
            date=datetime.fromisoformat(data["date"]),
        )

    def __repr__(self) -> str:
        return (
            f"Income(amount={self.amount}, "
            f"source='{self.source}', "
            f"category_id='{self.category_id}', "
            f"date='{self.date.isoformat()}')"
        )
