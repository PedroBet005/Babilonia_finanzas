from dataclasses import dataclass
from datetime import datetime, timedelta
from uuid import UUID, uuid4


@dataclass
class RefreshToken:
    id: UUID
    user_id: UUID
    token: str
    expires_at: datetime
    is_active: bool

    @staticmethod
    def create(user_id: UUID, token: str, days_valid: int = 7):
        return RefreshToken(
            id=uuid4(),
            user_id=user_id,
            token=token,
            expires_at=datetime.utcnow() + timedelta(days=days_valid),
            is_active=True
        )

    def deactivate(self):
        self.is_active = False

    def is_expired(self):
        return datetime.utcnow() > self.expires_at
