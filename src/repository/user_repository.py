from typing import Optional

from sqlmodel import select

from src.infra.database import User, get_session_maker
from src.models.user_model import UserModel, UserModelOut


class UserRepository:
    def __init__(self) -> None:
        self._session_maker = get_session_maker()

    async def save_user(self, user: UserModel) -> User:
        async with self._session_maker() as session:
            user_db = User(**user.model_dump())
            session.add(user_db)
            await session.commit()
        return user_db

    async def verify_if_user_exists(
        self, username: str, email: str, phone: str
    ) -> bool:
        async with self._session_maker() as session:
            query = await session.exec(
                select(User).where(
                    (User.username == username)
                    | (User.email == email)
                    | (User.phone == phone)
                )
            )

        return bool(query.first())

    async def get_user_by_id(self, user_id: int) -> Optional[UserModelOut]:
        async with self._session_maker() as session:
            query = await session.exec(select(User).where(User.id == user_id))
            user = query.first()

        return UserModelOut(**user.__dict__) if user else None
