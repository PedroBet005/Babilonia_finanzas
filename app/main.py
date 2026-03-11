from fastapi import FastAPI
from contextlib import asynccontextmanager

from api.v1.routes.auth import router as auth_router
from api.v1.routes.incomes import router as incomes_router
from api.v1.routes.expenses import router as expenses_router
from api.v1.routes.reports import router as reports_router
from api.v1.routes.balance import router as balance_router

from slowapi.middleware import SlowAPIMiddleware
from infrastructure.security.rate_limit import limiter
from infrastructure.db.postgres import init_postgres
from infrastructure.db.session import Base, engine


# =====================================================
# LIFESPAN (FORMA MODERNA - REEMPLAZA on_event)
# =====================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 🔥 Startup
    init_postgres()
    Base.metadata.create_all(bind=engine)
    yield
    # 🔥 Shutdown (opcional)


app = FastAPI(
    title="Babilonia Finanzas",
    version="1.0.0",
    lifespan=lifespan,
)


# =====================================================
# RATE LIMIT
# =====================================================

app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)


# =====================================================
# ROUTERS
# =====================================================

app.include_router(auth_router, prefix="/api/v1")
app.include_router(incomes_router, prefix="/api/v1")
app.include_router(expenses_router, prefix="/api/v1")
app.include_router(reports_router, prefix="/api/v1")
app.include_router(balance_router, prefix="/api/v1")


# =====================================================
# ROOT
# =====================================================

@app.get("/")
def root():
    return {"status": "Babilonia Finanzas API funcionando"}
