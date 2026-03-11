from pydantic import BaseModel


class IncomeCreateSchema(BaseModel):
    amount: float
    source: str
    apply_tithe: bool = False
    apply_debt: bool = False
