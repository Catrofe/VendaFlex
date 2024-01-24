from datetime import datetime, timedelta, timezone

import jwt

from src.infra.database import User
from src.infra.settings import Settings
from src.models.auth_model import TokenModel


class JWTService:
    def __init__(self) -> None:
        self.settings = Settings()

    async def create_token(self, user: User) -> TokenModel:
        return TokenModel(
            acessToken=await self.generate_token(
                user, False, self.settings.ACCESS_TOKEN_EXPIRE_MINUTES
            ),
            refreshToken=await self.generate_token(
                user, True, self.settings.REFRESH_TOKEN_EXPIRE_MINUTES
            ),
            tokenExpiresIn=self.settings.ACCESS_TOKEN_EXPIRE_MINUTES,
            refreshTokenExpiresIn=self.settings.REFRESH_TOKEN_EXPIRE_MINUTES,
        )

    async def generate_token(self, user: User, refresh: bool, expires: int) -> str:
        assignature = user.refresh_token if refresh else user.acess_token
        return jwt.encode(
            {
                "id": user.id,
                "username": user.username,
                "company_id": user.company_id,
                "company_owner": user.company_owner,
                "admin": user.admin,
                "refresh": refresh,
                "exp": datetime.now(timezone.utc) + timedelta(minutes=expires),
            },
            assignature,
            algorithm="HS256",
        )
