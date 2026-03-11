from pydantic import BaseModel
from uuid import UUID
from domain.entities.category import CategoryType


class CategoryCreate(BaseModel):
    name: str
    type: CategoryType


class CategoryResponse(BaseModel):
    id: UUID
    name: str
    type: CategoryType

    class Config:
        from_attributes = True
