from infrastructure.security.jwt import create_access_token, create_refresh_token
from domain.entities.refresh_token import RefreshToken


class LoginUserUseCase:

    def __init__(self, repo):
        self.repo = repo

    def execute(self, user):

        access_token = create_access_token({"sub": str(user.id)})
        refresh_token_str = create_refresh_token({"sub": str(user.id)})

        refresh_token = RefreshToken.create(user.id, refresh_token_str)

        self.repo.save_refresh_token(refresh_token)

        return {
            "access_token": access_token,
            "refresh_token": refresh_token_str
        }
