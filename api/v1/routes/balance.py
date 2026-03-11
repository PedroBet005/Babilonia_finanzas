from fastapi import APIRouter, Depends, Request

from api.v1.deps import get_finance_repository, get_current_user
from application.use_cases.get_balance import GetBalance
from infrastructure.security.rate_limit import limiter

router = APIRouter(
    prefix="/balance",
    tags=["Balance"],
    dependencies=[Depends(get_current_user)],
)


@router.get("/", status_code=200)
@limiter.limit("100/minute")
def get_balance(
    request: Request,
    repo=Depends(get_finance_repository),
):
    use_case = GetBalance(repo)
    return use_case.execute()

