import uuid

from fastapi import HTTPException

from src.infra.database import User
from src.models.auth_model import TokenModel
from src.repository.auth_repository import AuthRepository
from src.service.BcryptService import BcryptService
from src.service.jwt_service import JWTService


class AuthService:
    def __init__(self) -> None:
        self._repository = AuthRepository()
        self._encrypted = BcryptService()
        self._jwt = JWTService()

    async def authenticate(self, email: str, password: str) -> TokenModel:
        user = await self._repository.get_user_by_email(email)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        if not self._encrypted.verify_password(password, user.password):
            raise HTTPException(status_code=401, detail="Invalid password")

        user = await self.update_assignature_token(user)
        return await self._jwt.create_token(user)

    async def get_user_by_id(self, user_id: int, refresh: bool) -> str:
        user = await self._repository.get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user.refresh_token if refresh else user.acess_token

    async def update_assignature_token(self, user: User) -> User:
        return await self._repository.update_signature_token(
            user, str(uuid.uuid4()), str(uuid.uuid4())
        )
