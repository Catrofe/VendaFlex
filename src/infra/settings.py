from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    ENV: str = "Test"
    DATABASE_URL: str = "sqlite+aiosqlite:///VendaFlex.db"
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_SIGNATURE: str = "refresh"
    TOKEN_SIGNATURE: str = "access"
