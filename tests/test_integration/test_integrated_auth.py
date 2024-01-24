import asyncio
import os

import pytest
from fastapi.testclient import TestClient

from src.app import app, startup_event

client = TestClient(app)

URL_API = "/api"


@pytest.fixture
def change_db_url():
    asyncio.run(startup_event())
    yield
    os.remove("VendaFlex.db")


@pytest.fixture
def create_hub(change_db_url):
    client.post(
        "/api/hub",
        json={
            "hub": {
                "name": "Zeta Car",
                "description": "Revendedora de carros",
            },
            "company": {"name": "Loja Duque de Caxias", "cnpj": "11111111000133"},
            "user": {
                "username": "catrofe",
                "password": "12345678",
                "email": "email@email.com",
                "phone": "021999999999",
                "company_id": 0,
            },
        },
    )


@pytest.fixture
def login_user(create_hub):
    response = client.post(
        f"{URL_API}/login",
        json={
            "email": "email@email.com",
            "password": "12345678",
        },
    )
    return response.json()


def test_login_user_error_password(create_hub):
    response = client.post(
        f"{URL_API}/login",
        json={
            "email": "email@email.com",
            "password": "123456789",
        },
    )
    assert response.status_code == 400
    assert response.json() == {"message": "Incorrect email or password"}


def test_login_user_error_email(create_hub):
    response = client.post(
        f"{URL_API}/login",
        json={
            "email": "email21@email.com",
            "password": "12345678",
        },
    )
    assert response.status_code == 404
    assert response.json() == {"message": "User not found"}


def test_login_user(create_hub):
    response = client.post(
        f"{URL_API}/login",
        json={
            "email": "email@email.com",
            "password": "12345678",
        },
    )
    assert response.status_code == 200


def test_refresh_token(login_user):
    response = client.post(
        f"{URL_API}/refresh",
        headers={"Authorization": f"Bearer {login_user['refreshToken']}"},
    )
    assert response.status_code == 200
    assert response.json() == {
        "acessToken": response.json()["acessToken"],
        "refreshToken": response.json()["refreshToken"],
        "tokenExpiresIn": 30,
        "refreshTokenExpiresIn": 60,
        "tokenType": "bearer",
    }


def test_refresh_token_error(login_user):
    response = client.post(
        f"{URL_API}/refresh",
        headers={"Authorization": f"Bearer {login_user['acessToken']}"},
    )
    assert response.status_code == 401


def test_refresh_token_error_404(login_user):
    client.delete("/api/user/1")
    response = client.post(
        f"{URL_API}/refresh",
        headers={"Authorization": f"Bearer {login_user['refreshToken']}"},
    )
    assert response.status_code == 404


def test_logout(login_user):
    response = client.post(
        f"{URL_API}/logout",
        headers={"Authorization": f"Bearer {login_user['acessToken']}"},
    )
    assert response.status_code == 204


def test_logout_error(login_user):
    response = client.post(
        f"{URL_API}/logout",
        headers={"Authorization": f"Bearer {login_user['refreshToken']}"},
    )
    assert response.status_code == 401


def test_logout_error_404(login_user):
    client.delete("/api/user/1")
    response = client.post(
        f"{URL_API}/logout",
        headers={"Authorization": f"Bearer {login_user['acessToken']}"},
    )
    assert response.status_code == 404
