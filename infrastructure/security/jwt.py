from datetime import datetime, timedelta
from typing import Dict, Any

from jose import jwt

# ⚠️ En producción esto debe venir desde settings / .env
SECRET_KEY = "CHANGE_ME_SECRET"
ALGORITHM = "HS256"

# 🔐 Expiraciones
ACCESS_TOKEN_EXPIRE_MINUTES = 15
REFRESH_TOKEN_EXPIRE_DAYS = 7


# =========================
# ACCESS TOKEN
# =========================
def create_access_token(data: Dict[str, Any]) -> str:
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({
        "exp": expire,
        "type": "access",
    })

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# =========================
# REFRESH TOKEN
# =========================
def create_refresh_token(data: Dict[str, Any]) -> str:
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(
        days=REFRESH_TOKEN_EXPIRE_DAYS
    )

    to_encode.update({
        "exp": expire,
        "type": "refresh",
    })

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# =========================
# DECODE
# =========================
def decode_token(token: str) -> dict:
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
