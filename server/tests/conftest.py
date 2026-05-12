import os
import uuid

import infrastructure.models  # noqa: F401 — registers ORM models with Base.metadata
import pytest
from fastapi.testclient import TestClient

from api.dependencies import get_uow
from infrastructure.database.base import build_session_factory
from infrastructure.unit_of_work import SqlAlchemyUnitOfWork
from main import app

ADMIN_KEY = "change-me-admin-key"  # default from core/config.py
_TEST_DB_PATH = "test_fuzz.db"
_TEST_DB_URL = f"sqlite:///./{_TEST_DB_PATH}"


@pytest.fixture(scope="session")
def session_factory():
    sf = build_session_factory(_TEST_DB_URL, init_db=True)
    yield sf
    try:
        os.remove(_TEST_DB_PATH)
    except OSError:
        pass  # Windows may keep the file locked until process exit


@pytest.fixture(scope="session")
def client(session_factory):
    def override_get_uow():
        uow = SqlAlchemyUnitOfWork(session_factory)
        with uow:
            yield uow

    app.dependency_overrides[get_uow] = override_get_uow
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


# ── helpers ──────────────────────────────────────────────────────────────────

def unique(prefix: str = "user") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"


def register(client, username, password="pass1234", role="collector", admin_key=None):
    payload = {"username": username, "password": password, "role": role}
    if admin_key is not None:
        payload["admin_key"] = admin_key
    return client.post("/api/v1/auth/register", json=payload)


def login(client, username, password="pass1234"):
    return client.post("/api/v1/auth/token", data={"username": username, "password": password})


def bearer(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}


# ── shared token fixtures ─────────────────────────────────────────────────────

@pytest.fixture(scope="session")
def admin_token(client):
    name = unique("admin")
    register(client, name, role="admin", admin_key=ADMIN_KEY)
    r = login(client, name)
    return r.json()["access_token"]


@pytest.fixture(scope="session")
def collector_token(client):
    name = unique("collector")
    register(client, name)
    r = login(client, name)
    return r.json()["access_token"]


@pytest.fixture(scope="session")
def card_id(client, admin_token):
    r = client.post(
        "/api/v1/master-cards/",
        json={"title": "Base Card", "symbol": "BC", "rarity": "common", "description": "test", "quantity": 5},
        headers=bearer(admin_token),
    )
    assert r.status_code == 201
    return r.json()["id"]
