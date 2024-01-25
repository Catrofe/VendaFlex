import asyncio
import os

import pytest
from fastapi.testclient import TestClient

from src.app import app, startup_event

client = TestClient(app)

URL_API = "/api/hub"


@pytest.fixture
def change_db_url():
    asyncio.run(startup_event())
    yield
    os.remove("VendaFlex.db")


@pytest.fixture
def create_hub(change_db_url):
    client.post(
        URL_API,
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
        "/api/login",
        json={
            "email": "email@email.com",
            "password": "12345678",
        },
    )
    return response.json()["acessToken"]


def test_create_hub(change_db_url):
    response = client.post(
        URL_API,
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
    assert response.status_code == 201


def test_get_hub_by_id(login_user):
    print(login_user)
    response = client.get(
        f"{URL_API}/1",
        headers={"Authorization": login_user},
    )
    assert response.status_code == 200


def test_get_hub_by_id_error(login_user):
    client.delete(f"{URL_API}/1", headers={"Authorization": login_user})
    response = client.get(
        f"{URL_API}/1",
        headers={"Authorization": login_user},
    )
    assert response.status_code == 404


def test_get_all_hubs(login_user):
    response = client.get(
        URL_API,
        headers={"Authorization": login_user},
    )
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_get_all_hubs_empty(login_user):
    client.delete(f"{URL_API}/1", headers={"Authorization": login_user})
    response = client.get(URL_API, headers={"Authorization": login_user})
    assert response.status_code == 404


def test_update_hub(login_user):
    response = client.put(
        f"{URL_API}/1",
        json={"name": "Zeta Car", "description": "Revendedora de carros top 1"},
        headers={"Authorization": login_user},
    )
    assert response.status_code == 200
    assert response.json().get("description") == "Revendedora de carros top 1"


def test_update_hub_not_found(login_user):
    response = client.put(
        f"{URL_API}/2",
        json={"name": "Zeta Car", "description": "Revendedora de carros top 1"},
        headers={"Authorization": login_user},
    )
    assert response.status_code == 404


def test_delete_hub(login_user):
    response = client.delete(
        f"{URL_API}/1",
        headers={"Authorization": login_user},
    )
    assert response.status_code == 204

    get_hub = client.get(
        f"{URL_API}/1",
        headers={"Authorization": login_user},
    )
    assert get_hub.status_code == 404


def test_delete_hub_not_found(login_user):
    client.delete(f"{URL_API}/1", headers={"Authorization": login_user})
    response = client.delete(
        f"{URL_API}/1",
        headers={"Authorization": login_user},
    )
    assert response.status_code == 404
