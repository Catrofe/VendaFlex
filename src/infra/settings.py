from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    ENV: str = "Test"
    DATABASE_URL: str = "sqlite+aiosqlite:///VendaFlex.db"
