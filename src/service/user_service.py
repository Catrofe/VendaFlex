from typing import Optional

from fastapi import HTTPException

from src.models.user_model import UserModel, UserModelEdit, UserModelOut
from src.repository.user_repository import UserRepository
from src.service.BcryptService import BcryptService


class UserService:
    def __init__(self) -> None:
        self._repository = UserRepository()
        self._encrypted = BcryptService()

    async def create_user(self, user: UserModel) -> UserModelOut:
        await self.verify_if_user_exists(user.username, user.email, user.phone)
        user.password = self._encrypted.hash_password(user.password)
        user_db = await self._repository.save_user(user)
        return UserModelOut(**user_db.__dict__)

    async def verify_if_user_exists(
        self, username: Optional[str], email: Optional[str], phone: Optional[str]
    ) -> None:
        exists = await self._repository.verify_if_user_exists(username, email, phone)
        if exists:
            raise HTTPException(status_code=409, detail="User already exists")

    async def get_user_by_id(self, user_id: int) -> UserModelOut:
        user = await self._repository.get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return UserModelOut(**user.__dict__)

    async def update_user(self, user_id: int, request: UserModelEdit) -> UserModelOut:
        await self.verify_if_user_exists(request.username, request.email, request.phone)

        user = await self._repository.get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        user_db = await self._repository.update_user(user, request)
        return UserModelOut(**user_db.__dict__)

    async def delete_user(self, user_id: int) -> None:
        user = await self._repository.get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        await self._repository.delete_user(user)
