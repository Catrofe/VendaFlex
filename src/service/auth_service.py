from src.service.user_service import UserService


class AuthService:
    def __init__(self) -> None:
        self._user_service = UserService()
