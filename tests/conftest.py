from datetime import datetime

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
        "tg_id": 1234567,
        "username": "testuser",
        "phone": "+380991112233",
        "name": "Test User"
    }

    response = await client.post("/users/", json=user_data)
    assert response.status_code == 201
    return user_data


@pytest.fixture
async def test_user_without_orders(client):
    user_data = {
        "tg_id": 88888888,
        "username": "some_user",
        "phone": "+193739274123",
        "name": "Some User"
    }

    response = await client.post("/users/", json=user_data)
    assert response.status_code == 201
    return user_data




@pytest.fixture
async def test_user_2(client):
    user_data = {
        "tg_id": 11111111,
        "username": "testuser",
        "phone": "+380991112233",
        "name": "Test User"
    }

    response = await client.post("/users/", json=user_data)
    assert response.status_code == 201
    return user_data


# fixture for - test_master_info_with_not_exists_telegram_id 
@pytest.fixture
async def test_user_whthout_master_profile(client):
    user_data = {
        "tg_id": 11234567,
        "username": "User | Not master",
        "phone": "+888123123123",
        "name": "Not Master"
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



@pytest.fixture
async def test_master(client, test_user):
    data = {
        'specialization': 'Розробник',
        'description': 'Some description for developer test creation master fixture',
        'experience_years': 3,
        'location': 'Some Location',
        'schedule': 'Monday-Friday 09:00-18:00',
        'tg_id': test_user.get('tg_id'),
        'ref_bonus': 10
    }

    response = await client.post('/masters/', json=data)
    assert response.status_code == 201
    return response.json()

    


@pytest.fixture
async def test_service(client, test_master):
    tg_id = test_master['user']['tg_id']
    data = {
        "title": "Some test title for creating service",
        "description": "Some test description for creating service test test test",
        "price": 1500,
        "master_id": tg_id
    }
    response = await client.post("/services/", json=data)
    assert response.status_code == 201
    return response.json()


@pytest.fixture
async def test_order(client, test_master, test_user, test_service):
    now = datetime.now().isoformat()

    data = {
        "user_tg_id": test_user.get("tg_id"),
        "master_tg_id": test_master['user']['tg_id'],
        "service_id": test_service.get("id"),
        "description": "Some Description For Creating order Fixture",
        "price": 1500,
        "scheduled_at": now,
        "deadline": now
    }

    response = await client.post("/orders/", json=data)
    assert response.status_code == 201
    return response.json()