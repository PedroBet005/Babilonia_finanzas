class TokenBlacklist:

    def __init__(self):
        self.blacklisted = set()

    def add(self, token: str):
        self.blacklisted.add(token)

    def is_blacklisted(self, token: str) -> bool:
        return token in self.blacklisted


token_blacklist = TokenBlacklist()
