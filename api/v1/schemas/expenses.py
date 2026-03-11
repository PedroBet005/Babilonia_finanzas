from pydantic import BaseModel
from typing import Optional


class ExpenseCreateSchema(BaseModel):
    amount: float
    category: str
    description: Optional[str] = None
