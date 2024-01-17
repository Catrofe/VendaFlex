from fastapi import HTTPException

from src.models.user_model import UserModel, UserModelOut
from src.repository.user_repository import UserRepository
from src.service.BcryptService import BcryptService


class UserService:
    def __init__(self) -> None:
        self._repository = UserRepository()
        self._encrypted = BcryptService()

    async def create_user(self, user: UserModel) -> UserModelOut:
        await self.verify_if_user_exists(user)
        user.password = self._encrypted.hash_password(user.password)
        user_db = await self._repository.save_user(user)
        return UserModelOut(**user_db.__dict__, companyId=user_db.company_id)

    async def verify_if_user_exists(self, user: UserModel) -> None:
        exists = await self._repository.verify_if_user_exists(
            user.username, user.email, user.phone
        )
        if exists:
            raise HTTPException(status_code=409, detail="User already exists")
