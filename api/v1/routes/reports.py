from fastapi import APIRouter, Depends, Request

from application.use_cases.get_balance import GetBalance
from api.v1.deps import get_finance_repository, get_current_user
from infrastructure.security.rate_limit import limiter

router = APIRouter(
    prefix="/reports",
    tags=["Reports"],
    dependencies=[Depends(get_current_user)],
)


@router.get("/balance")
@limiter.limit("100/minute")
def get_balance(
    request: Request,
    repo=Depends(get_finance_repository),
):
    use_case = GetBalance(repo)
    return use_case.execute()
