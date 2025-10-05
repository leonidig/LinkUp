import pytest


# create user
@pytest.mark.asyncio
async def test_create_user(client):
    data = {
        'tg_id': 1234567,
        'username': 'test',
        'phone': '+38094713844',
        'name': 'some_name'
    }

    response = await client.post('/users/', json=data)

    assert response.status_code == 201
    assert response.json() == 'Created!'


# check user exists
@pytest.mark.asyncio
async def test_get_user(client, test_user):
    tg_id = test_user["tg_id"]
    response = await client.get(f"/users/check-exists/{tg_id}")
    assert response.status_code == 200
    assert response.json() == True


# get master by telegram ID
@pytest.mark.asyncio
async def test_get_master_by_tg_id(client, test_user, test_master):
    response = await client.get(f'/users/master/{test_user.get('tg_id')}')
    assert response.status_code == 200
    assert response.json() is not None