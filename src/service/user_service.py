from src.repository.user_repository import UserRepository


class UserService:
    def __init__(self) -> None:
        self._repository = UserRepository()
