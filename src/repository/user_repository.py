from src.infra.database import get_session_maker


class UserRepository:
    def __init__(self) -> None:
        self._session_maker = get_session_maker()
