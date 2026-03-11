from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from collections.abc import Generator

from infrastructure.repositories.sqlalchemy_finance_repository import (
    SQLAlchemyFinanceRepository,
)
from infrastructure.db.session import SessionLocal
from infrastructure.security.jwt import decode_token
from infrastructure.security.token_blacklist import token_blacklist


# =====================================================
# DATABASE
# =====================================================

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# =====================================================
# REPOSITORY (REAL - SQLALCHEMY)
# =====================================================

def get_repository(db: Session = Depends(get_db)):
    return SQLAlchemyFinanceRepository(db)


# =====================================================
# AUTH
# =====================================================

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def get_current_user(
    request: Request,
    token: str = Depends(oauth2_scheme),
):
    # 🔒 1️⃣ Verificar si el token está en blacklist
    if token_blacklist.is_blacklisted(token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token revoked",
        )

    # 🔐 2️⃣ Decodificar JWT
    try:
        payload = decode_token(token)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid_token",
        )

    user_data = {
        "username": payload.get("sub"),
        "role": payload.get("role"),
    }

    # 🔥 Guardamos el usuario autenticado en request.state
    request.state.user = user_data

    return user_data


def require_admin(request: Request):
    user = request.state.user

    if user["role"] != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="admin_required",
        )

    return user
