from fastapi import APIRouter, Depends, status, Request

from api.v1.schemas.expenses import ExpenseCreateSchema
from application.use_cases.register_expenses import RegisterExpense
from api.v1.deps import get_finance_repository, get_current_user
from infrastructure.security.rate_limit import limiter

router = APIRouter(
    prefix="/expenses",
    tags=["Expenses"],
    dependencies=[Depends(get_current_user)],
)



@router.post("/", status_code=status.HTTP_201_CREATED)
@limiter.limit("100/minute")
def create_expense(
    request: Request,
    payload: ExpenseCreateSchema,
    repo=Depends(get_finance_repository),
):
    use_case = RegisterExpense(repo)
    return use_case.execute(**payload.model_dump())
