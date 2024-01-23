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
