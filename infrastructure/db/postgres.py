from infrastructure.db.session import engine
from infrastructure.db.session import Base


def init_postgres():
    Base.metadata.create_all(bind=engine)
