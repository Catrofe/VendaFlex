from __future__ import annotations

from datetime import datetime
from typing import Any

from sqlalchemy import ForeignKey
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from src.infra.settings import Settings

settings = Settings()


def get_session_maker() -> Any:
    url = settings.DATABASE_URL
    engine = create_async_engine(
        url,
        echo=False,
    )
    return async_sessionmaker(engine, expire_on_commit=False)


async def create_database() -> None:
    url = settings.DATABASE_URL
    engine = create_async_engine(
        url,
        echo=False,
    )

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


class Base(DeclarativeBase):
    pass


class Company(Base):
    __tablename__ = "companies"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    address: Mapped[str]
    phone: Mapped[str]
    email: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(default=datetime.now())
    updated_at: Mapped[datetime] = mapped_column(onupdate=datetime.now())


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str]
    password: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    phone: Mapped[str] = mapped_column(unique=True)
    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now())
    updated_at: Mapped[datetime] = mapped_column(onupdate=datetime.now(), nullable=True)
