import asyncio
import os

import pytest
from fastapi.testclient import TestClient

from src.app import app, startup_event

client = TestClient(app)

URL_API = "/api/user"


@pytest.fixture
def change_db_url():
    asyncio.run(startup_event())
    yield
    os.remove("VendaFlex.db")


@pytest.fixture
def create_user(change_db_url):
    client.post(
        URL_API,
        json={
            "username": "catrofe",
            "password": "12345678",
            "email": "email@email.com",
            "phone": "021999999999",
            "companyId": None,
        },
    )


def test_create_user(change_db_url):
    response = client.post(
        "/api/user/",
        json={
            "username": "catrofe",
            "password": "12345678",
            "email": "email@email.com",
            "phone": "021999999999",
            "companyId": None,
        },
    )
    assert response.status_code == 201
    assert response.json() == {
        "id": 1,
        "username": "catrofe",
        "email": "email@email.com",
        "phone": "021999999999",
        "companyId": None,
    }


def test_error_create_user_duplicated_email(create_user):
    response = client.post(
        URL_API,
        json={
            "username": "catrofe",
            "password": "12345678",
            "email": "email@email.com",
            "phone": "021999999999",
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
            "phone": "021999999999",
            "companyId": None,
        },
    )
    assert response.status_code == 409


@pytest.mark.skip("Company do not exist")
def test_error_create_user_company_not_exists(change_db_url):
    response = client.post(
        URL_API,
        json={
            "username": "catrofe",
            "password": "12345678",
            "email": "email@email.com",
            "phone": "021999999999",
            "companyId": 2,
        },
    )
    assert response.status_code == 400


def test_get_user(create_user):
    response = client.get(f"{URL_API}/1")
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "username": "catrofe",
        "email": "email@email.com",
        "phone": "021999999999",
        "companyId": None,
    }


def test_get_user_not_found(change_db_url):
    response = client.get(f"{URL_API}/1")
    assert response.status_code == 404


def test_edit_user_not_foud(change_db_url):
    response = client.put(
        f"{URL_API}/1",
        json={
            "username": "catrofe",
            "email": "email@email.com",
            "phone": "021999999999",
            "companyId": None,
        },
    )
    assert response.status_code == 404


def test_edit_user_conflict_email(create_user):
    response = client.put(
        f"{URL_API}/1",
        json={
            "username": "catrofe",
            "email": "email@email.com",
            "phone": "021999999999",
            "companyId": None,
        },
    )
    assert response.status_code == 409


def test_edit_user_sucess(create_user):
    response = client.put(
        f"{URL_API}/1",
        json={
            "username": "catrofinho",
            "email": "email2@email.com",
            "phone": "021999999998",
            "companyId": None,
        },
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "username": "catrofinho",
        "email": "email2@email.com",
        "phone": "021999999998",
        "companyId": None,
    }


def test_edit_username(create_user):
    response = client.put(
        f"{URL_API}/1",
        json={
            "username": "catrofinho",
        },
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "username": "catrofinho",
        "email": "email@email.com",
        "phone": "021999999999",
        "companyId": None,
    }


def test_delete_user_not_found(change_db_url):
    response = client.delete(f"{URL_API}/1")
    assert response.status_code == 404


def test_delete_user_sucess(create_user):
    response = client.delete(f"{URL_API}/1")
    assert response.status_code == 204

    get_user = client.get(f"{URL_API}/1")
    assert get_user.status_code == 404


def test_change_password_not_found(change_db_url):
    response = client.patch(
        f"{URL_API}/1",
        json={
            "password": "12345678",
        },
    )
    assert response.status_code == 404


def test_change_password_sucess(create_user):
    response = client.patch(
        f"{URL_API}/1",
        json={
            "password": "12345678",
        },
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "username": "catrofe",
        "email": "email@email.com",
        "phone": "021999999999",
        "companyId": None,
    }
