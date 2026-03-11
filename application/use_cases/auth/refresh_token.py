from domain.exceptions import DomainException
from infrastructure.security.jwt import create_access_token


class RefreshTokenUseCase:

    def __init__(self, repo):
        self.repo = repo

    def execute(self, refresh_token_str):

        # 1️⃣ Buscar token
        token = self.repo.get_refresh_token(refresh_token_str)

        if not token:
            raise DomainException("Invalid refresh token")

        # 2️⃣ Validar si está activo
        if not token.is_active:
            raise DomainException("Token inactive")

        # 3️⃣ Validar expiración
        if token.is_expired():
            raise DomainException("Token expired")

        # 4️⃣ Generar nuevo access token
        return {
            "access_token": create_access_token({
                "sub": str(token.user_id)
            })
        }
