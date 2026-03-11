from fastapi import APIRouter, HTTPException, status, Request

from api.v1.schemas.auth import LoginSchema, TokenSchema
from infrastructure.security.hashing import verify_password
from infrastructure.security.jwt import create_access_token
from infrastructure.security.rate_limit import limiter


router = APIRouter(prefix="/auth", tags=["Auth"])


# ⚠️ DEMO: luego va a repo/DB
FAKE_USER = {
    "username": "admin",
    "password_hash": "$2b$12$examplehash",
    "role": "admin",
}


@router.post("/login", response_model=TokenSchema)
@limiter.limit("5/minute")
def login(request: Request, payload: LoginSchema):

    if payload.username != FAKE_USER["username"]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid_credentials",
        )

    if not verify_password(payload.password, FAKE_USER["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid_credentials",
        )

    access_token = create_access_token({
        "sub": payload.username,
        "role": FAKE_USER["role"],
    })

    return {"access_token": access_token}

