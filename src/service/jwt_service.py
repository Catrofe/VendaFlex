from datetime import datetime, timedelta

import jwt

from src.infra.database import User
from src.infra.settings import Settings
from src.models.auth_model import TokenModel


class JWTService:
    def __init__(self) -> None:
        self.settings = Settings()

    async def create_token(self, user: User) -> TokenModel:
        return TokenModel(
            access_token=await self.generate_token(
                user, False, self.settings.ACCESS_TOKEN_EXPIRE_MINUTES
            ),
            refresh_token=await self.generate_token(
                user, True, self.settings.REFRESH_TOKEN_EXPIRE_MINUTES
            ),
            token_expires_in=self.settings.ACCESS_TOKEN_EXPIRE_MINUTES,
            refresh_token_expires_in=self.settings.REFRESH_TOKEN_EXPIRE_MINUTES,
        )

    async def generate_token(self, user: User, refresh: bool, expires: int) -> str:
        return jwt.encode(
            {
                "id": user.id,
                "username": user.username,
                "company_id": user.company_id,
                "company_owner": user.company_owner,
                "admin": user.admin,
                "refresh": refresh,
                "exp": datetime.now() + timedelta(minutes=expires),
            },
            self.settings.REFRESH_SIGNATURE
            if refresh
            else self.settings.TOKEN_SIGNATURE,
            algorithm="HS256",
        )
