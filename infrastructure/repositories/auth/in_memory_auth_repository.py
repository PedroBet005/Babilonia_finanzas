from domain.ports.finance_repository import FinanceRepository
from domain.entities.refresh_token import RefreshToken


class InMemoryAuthRepository(FinanceRepository):
    def __init__(self):
        self._refresh_tokens: list[RefreshToken] = []

    # =========================
    # REFRESH TOKENS
    # =========================
    def save_refresh_token(self, token: RefreshToken) -> None:
        self._refresh_tokens.append(token)

    def get_refresh_token(self, token_str: str) -> RefreshToken | None:
        for token in self._refresh_tokens:
            if token.token == token_str:
                return token
        return None

    def update_refresh_token(self, token: RefreshToken) -> None:
        for i, stored_token in enumerate(self._refresh_tokens):
            if stored_token.token == token.token:
                self._refresh_tokens[i] = token
                break
