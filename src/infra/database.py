from __future__ import annotations

from datetime import datetime
from typing import Any

from sqlalchemy import ForeignKey
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from src.infra.settings import Settings

settings = Settings()

engine = create_async_engine(settings.DATABASE_URL, echo=False)


def get_session_maker() -> Any:
    return async_sessionmaker(engine, expire_on_commit=False)


async def create_database() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


class Base(DeclarativeBase):
    pass


class Hub(Base):
    __tablename__ = "hub"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    description: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(default=datetime.now())
    updated_at: Mapped[datetime] = mapped_column(onupdate=datetime.now(), nullable=True)


class Company(Base):
    __tablename__ = "company"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    cnpj: Mapped[str]
    hub_id: Mapped[int] = mapped_column(ForeignKey("hub.id"))
    company_admin: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now())
    updated_at: Mapped[datetime] = mapped_column(onupdate=datetime.now(), nullable=True)


class User(Base):
    __tablename__ = "tb_user"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    phone: Mapped[str] = mapped_column(unique=True)
    company_id: Mapped[int] = mapped_column(ForeignKey("company.id"), nullable=True)
    company_owner: Mapped[bool] = mapped_column(default=False)
    admin: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now())
    updated_at: Mapped[datetime] = mapped_column(onupdate=datetime.now(), nullable=True)
