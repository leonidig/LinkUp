import pytest
from sqlalchemy import delete
from httpx import AsyncClient, ASGITransport

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


# fixtures.py
@pytest.fixture
async def test_master(client, test_user):
    data = {
        'specialization': 'Розробник',
        'description': 'Some description for developer test creation master fixture',
        'experience_years': 3,
        'location': 'Some Location',
        'schedule': 'Monday-Friday 09:00-18:00',
        'user_id': test_user['tg_id']
    }
    response = await client.post('/masters/', json=data)
    assert response.status_code == 201
    return response.json() 
