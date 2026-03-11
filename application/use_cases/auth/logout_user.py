from infrastructure.security.token_blacklist import token_blacklist


class LogoutUserUseCase:

    def execute(self, access_token: str):
        token_blacklist.add(access_token)
