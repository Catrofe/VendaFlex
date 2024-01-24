from typing import Optional

from sqlalchemy import select

from src.infra.database import User, get_session_maker


class AuthRepository:
    def __init__(self) -> None:
        self._session_maker = get_session_maker()

    async def get_user_by_email(self, email: str) -> Optional[User]:
        async with self._session_maker() as session:
            query = await session.execute(select(User).filter(User.email == email))
            user = query.scalar()

        return user or None

    async def get_user_by_id(self, user_id: int) -> Optional[User]:
        async with self._session_maker() as session:
            query = await session.execute(select(User).where(User.id == user_id))
            user = query.scalar()

        return user or None

    async def update_signature_token(
        self, user: User, access_token: str, refresh_token: str
    ) -> User:
        async with self._session_maker() as session:
            user.acess_token = access_token
            user.refresh_token = refresh_token
            await session.merge(user)
            await session.commit()

        return user
