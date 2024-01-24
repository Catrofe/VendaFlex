import bcrypt


class BcryptService:
    def __init__(self) -> None:
        self._salt = bcrypt.gensalt()

    def hash_password(self, password: str) -> str:
        return bcrypt.hashpw(password.encode(), self._salt).decode()

    def verify_password(self, password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(password.encode(), hashed_password.encode())
