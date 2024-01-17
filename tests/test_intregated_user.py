import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import create_async_engine

from src.app import app
from src.infra.database import Base
from src.infra.settings import Settings

client = TestClient(app)

URL_API = "/api/user"


@pytest.fixture
async def drop_database():
    settings = Settings()
    engine = create_async_engine(settings.DATABASE_URL, echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all())


@pytest.fixture
def create_user(drop_database):
    client.post(
        URL_API,
        json={
            "username": "catrofe",
            "password": "12345678",
            "email": "email@email.com",
            "phone": "999999999",
            "companyId": None,
        },
    )


def test_create_user(drop_database):
    response = client.post(
        URL_API,
        json={
            "username": "catrofe",
            "password": "12345678",
            "email": "email@email.com",
            "phone": "999999999",
            "companyId": None,
        },
    )
    assert response.status_code == 201
    assert response.json() == {
        "id": 1,
        "username": "catrofe",
        "email": "email@email.com",
        "phone": "999999999",
        "companyId": None,
    }


def test_error_create_user_duplicated_email(create_user):
    response = client.post(
        URL_API,
        json={
            "username": "catrofe",
            "password": "12345678",
            "email": "email@email.com",
            "phone": "999999998",
            "companyId": None,
        },
    )
    assert response.status_code == 409


def test_error_create_user_duplicated_phone(create_user):
    response = client.post(
        URL_API,
        json={
            "username": "catrofe",
            "password": "12345678",
            "email": "email@email2.com",
            "phone": "999999999",
            "companyId": None,
        },
    )
    assert response.status_code == 409


def test_error_create_user_company_not_exists(drop_database):
    response = client.post(
        URL_API,
        json={
            "username": "catrofe",
            "password": "12345678",
            "email": "email@email.com",
            "phone": "999999999",
            "companyId": 2,
        },
    )
    assert response.status_code == 400
