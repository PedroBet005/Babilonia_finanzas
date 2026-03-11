from fastapi import APIRouter, Depends, Request

from api.v1.deps import get_finance_repository, get_current_user
from application.use_cases.get_balance import GetBalance
from infrastructure.security.rate_limit import limiter

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"],
    dependencies=[Depends(get_current_user)],
)



@router.get("/")
@limiter.limit("100/minute")
def get_dashboard(
    request: Request,
    repo=Depends(get_finance_repository),
):
    use_case = GetBalance(repo)
    balance = use_case.execute()

    return {
        "summary": balance,
        "message": "Financial dashboard overview",
    }
