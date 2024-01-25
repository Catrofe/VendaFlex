import datetime
import logging
from typing import Optional

import jwt
from fastapi import HTTPException, Request

from src.infra.settings import Settings
from src.models.auth_model import TokenData
from src.service.auth_service import AuthService


class HasAuthRole:
    def __init__(
        self, owner: bool = False, admin: bool = False, refresh: bool = False
    ) -> None:
        self.owner = owner
        self.admin = admin
        self.refresh = refresh
        self.auth_service = AuthService()
        self.settings = Settings()

    async def __call__(self, request: Request) -> TokenData:
        try:
            token = await self.verify_if_token_exists(request)
            signature, lee_way = await self.generate_signature(token)
            if not signature:
                raise HTTPException(status_code=401)
            token_decoded = jwt.decode(
                token,
                signature,
                algorithms=["HS256"],
                leeway=datetime.timedelta(minutes=lee_way),
            )
            token_data = TokenData(**token_decoded)
            request.state.user = token_data
        except (
            jwt.ExpiredSignatureError,
            jwt.InvalidSignatureError,
            jwt.InvalidTokenError,
        ) as e:
            logging.info(e)
            raise HTTPException(status_code=401) from e

        await self.verify_role(token_data)
        return token_data

    async def verify_role(self, token_data: TokenData) -> None:
        if self.owner and not token_data.company_owner:
            raise HTTPException(status_code=403, detail="User is not owner")
        if self.admin and not token_data.admin and not token_data.company_owner:
            raise HTTPException(status_code=403, detail="User is not admin")

    async def generate_signature(self, token: str) -> tuple[Optional[str], int]:
        signature = await self.verify_if_user_exists(token)
        lee_way = (
            self.settings.REFRESH_TOKEN_EXPIRE_MINUTES
            if self.refresh
            else self.settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
        return signature, lee_way

    async def verify_if_user_exists(self, token: str) -> Optional[str]:
        token_decoded = jwt.decode(token, options={"verify_signature": False})
        return await self.auth_service.get_user_by_id(token_decoded["id"], self.refresh)

    @staticmethod
    async def verify_if_token_exists(request: Request) -> str:
        if token := request.headers.get("Authorization"):
            return token.replace("Bearer ", "")
        raise HTTPException(status_code=401)
