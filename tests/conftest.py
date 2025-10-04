import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy import delete

from . import app
from server.db import AsyncDB, Master, User


@pytest.fixture
async def client():
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://localhost:8000/api"
    ) as ac:
        yield ac


@pytest.fixture
async def test_user(client):
    user_data = {
        "tg_id": 344444,
        "username": "testuser",
        "phone": "+380991112233",
        "name": "Test User"
    }

    response = await client.post("/users/", json=user_data)
    assert response.status_code == 201
    return user_data


@pytest.fixture(autouse=True)
async def clean_db():
    async with AsyncDB.Session() as session:
        await session.execute(delete(Master))
        await session.commit()
    yield
