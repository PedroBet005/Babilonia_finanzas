from fastapi import APIRouter, Depends, status, Request

from api.v1.schemas.incomes import IncomeCreateSchema
from api.v1.deps import get_finance_repository, get_current_user
from application.use_cases.register_incomes import RegisterIncome
from infrastructure.security.rate_limit import limiter

router = APIRouter(
    prefix="/incomes",
    tags=["Incomes"],
    dependencies=[Depends(get_current_user)],  # 🔒 PROTECCIÓN GLOBAL
)


@router.post("/", status_code=status.HTTP_201_CREATED)
@limiter.limit("100/minute")
def register_income(
    request: Request,
    payload: IncomeCreateSchema,
    repo=Depends(get_finance_repository),
):
    use_case = RegisterIncome(repo)
    return use_case.execute(**payload.model_dump())

