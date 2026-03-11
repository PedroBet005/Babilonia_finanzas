from uuid import UUID
from domain.entities.category import CategoryType


class CreateCategoryDTO:
    def __init__(self, name: str, type: CategoryType, user_id: UUID):
        self.name = name
        self.type = type
        self.user_id = user_id


class UpdateCategoryDTO:
    def __init__(self, category_id: UUID, name: str, user_id: UUID):
        self.category_id = category_id
        self.name = name
        self.user_id = user_id
