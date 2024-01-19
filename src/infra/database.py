from __future__ import annotations

from datetime import datetime
from typing import Any, Optional

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker as session
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import DateTime
from sqlmodel import Field, SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from src.infra.settings import Settings

settings = Settings()

engine = create_async_engine(settings.DATABASE_URL, echo=False)


def get_session_maker() -> Any:
    return session(engine, class_=AsyncSession, expire_on_commit=False)  # type: ignore


async def create_database() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


class Company(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(min_length=2, max_length=155)
    phone: str = Field(min_length=10, max_length=20)
    email: str = Field(min_length=8, max_length=155)
    created_at: Optional[datetime] = Field(default=None)
    updated_at: Optional[datetime] = Field(default=None, nullable=True)


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(unique=True, min_length=3, max_length=50)
    password: str = Field(min_length=8, max_length=155)
    email: str = Field(unique=True, min_length=8, max_length=155)
    phone: str = Field(unique=True, min_length=10, max_length=20)
    company_id: Optional[int] = Field(
        default=None, nullable=True, foreign_key="company.id"
    )
    created_at: Optional[datetime] = Field(default=datetime.now())
    updated_at: Optional[datetime] = Field(
        sa_column=Column("updated_at", DateTime, onupdate=datetime.now())
    )
