from sqlalchemy.orm import Session
from domain.repositories.finance_repository import FinanceRepository
from infrastructure.db.models.category_model import CategoryModel
from domain.entities.category import Category
from uuid import UUID


class SQLAlchemyFinanceRepository(FinanceRepository):

    def __init__(self, db: Session):
        self.db = db

    # ---------- CATEGORY ----------

    def create_category(self, category: Category):
        model = CategoryModel(
            id=category.id,
            name=category.name,
            type=category.type.value,
            user_id=category.user_id,
            is_active=category.is_active,
            created_at=category.created_at
        )
        self.db.add(model)
        self.db.commit()

    def get_categories_by_user(self, user_id: UUID):
        rows = self.db.query(CategoryModel)\
            .filter(CategoryModel.user_id == user_id)\
            .all()

        return [
            Category(
                id=r.id,
                name=r.name,
                type=r.type,
                user_id=r.user_id,
                is_active=r.is_active,
                created_at=r.created_at
            )
            for r in rows
        ]

    def get_category_by_id(self, category_id: UUID):
        r = self.db.query(CategoryModel)\
            .filter(CategoryModel.id == category_id)\
            .first()

        if not r:
            return None

        return Category(
            id=r.id,
            name=r.name,
            type=r.type,
            user_id=r.user_id,
            is_active=r.is_active,
            created_at=r.created_at
        )

    def update_category(self, category: Category):
        model = self.db.query(CategoryModel)\
            .filter(CategoryModel.id == category.id)\
            .first()

        model.name = category.name
        model.is_active = category.is_active

        self.db.commit()