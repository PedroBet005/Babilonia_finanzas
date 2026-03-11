from fastapi import APIRouter, Depends, Request
from uuid import UUID

from api.v1.deps import get_repository, get_current_user
from application.use_cases.category.create_category import CreateCategoryUseCase
from application.use_cases.category.update_category import UpdateCategoryUseCase
from application.use_cases.category.delete_category import DeleteCategoryUseCase
from application.use_cases.category.list_categories import ListCategoriesUseCase
from application.dto.category_dto import CreateCategoryDTO, UpdateCategoryDTO
from api.v1.schemas.category import CategoryCreate, CategoryResponse
from infrastructure.security.rate_limit import limiter

router = APIRouter(
    prefix="/categories",
    tags=["Categories"],
    dependencies=[Depends(get_current_user)],  # 🔒 protección global
)


@router.post("", response_model=CategoryResponse)
@limiter.limit("100/minute")
def create_category(
    request: Request,
    data: CategoryCreate,
    repo=Depends(get_repository),
):
    use_case = CreateCategoryUseCase(repo)
    dto = CreateCategoryDTO(
        data.name,
        data.type,
        request.state.user["username"],  # 🔥 acceso limpio
    )
    return use_case.execute(dto)


@router.get("", response_model=list[CategoryResponse])
@limiter.limit("100/minute")
def list_categories(
    request: Request,
    repo=Depends(get_repository),
):
    use_case = ListCategoriesUseCase(repo)
    return use_case.execute(request.state.user["username"])


@router.put("/{category_id}", response_model=CategoryResponse)
@limiter.limit("100/minute")
def update_category(
    request: Request,
    category_id: UUID,
    data: CategoryCreate,
    repo=Depends(get_repository),
):
    use_case = UpdateCategoryUseCase(repo)
    dto = UpdateCategoryDTO(
        category_id,
        data.name,
        request.state.user["username"],
    )
    return use_case.execute(dto)


@router.delete("/{category_id}")
@limiter.limit("100/minute")
def delete_category(
    request: Request,
    category_id: UUID,
    repo=Depends(get_repository),
):
    use_case = DeleteCategoryUseCase(repo)
    use_case.execute(
        category_id,
        request.state.user["username"],
    )
    return {"message": "Category deleted"}
