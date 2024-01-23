from fastapi import HTTPException

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

        return await self._jwt.create_token(user)
