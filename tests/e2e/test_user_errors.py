import pytest
from . import get_error_msgs


# create user 422 ( short telegram ID )
@pytest.mark.asyncio
async def test_create_user_short_tg_id(client):
    data = {
        'tg_id': 111,
        'username': 'test',
        'phone': '+38094713844',
        'name': 'some_name'
    }

    response = await client.post('/users/', json=data)

    json = response.json()
    assert response.status_code == 422
    assert get_error_msgs(response) == ['Value error, Некорректний формат Telegram ID']


# create user 422 ( short phone number )
@pytest.mark.asyncio
async def test_create_user_short_phone(client):
    data = {
        'tg_id': 1234567,
        'username': '', # just for test - what happened if we send empty username
        'phone': '+111',
        'name': 'some_name'
    }

    response = await client.post('/users/', json=data)

    json = response.json()
    assert response.status_code == 422
    assert get_error_msgs(response) == ['Value error, Некорректний формат номера телефона']



# create user 422 ( short username )
@pytest.mark.asyncio
async def test_create_user_short_username(client):
    data = {
        'tg_id': 1234567,
        'username': 'a',
        'phone': '+380937164922',
        'name': 'some_name'
    }

    response = await client.post('/users/', json=data)

    json = response.json()
    assert response.status_code == 422
    assert get_error_msgs(response) == ['Value error, Юзер-нейм повинно містити від 2 до 55 символів']


# create user 422 ( long name )
@pytest.mark.asyncio
async def test_create_user_long_name(client):
    data = {
        'tg_id': 1234567,
        'username': 'test',
        'phone': '+380937164922',
        'name': 'Some long name ' * 4
    }

    response = await client.post('/users/', json=data)

    assert response.status_code == 422
    assert get_error_msgs(response) == ['String should have at most 55 characters']


# check user exists 200 ( incorrect user telegram id)
@pytest.mark.asyncio
async def test_check_user_exists_invalid_tg_id(client):
    response = await client.get('/users/check-exists/94574867204')
    assert response.status_code == 200
    assert response.json() == False


# get master 404 ( invalid telegram ID )
@pytest.mark.asyncio
async def test_get_master_by_invalid_tg_id(client):
    response = await client.get('/users/master/347293749239')
    json = response.json()
    assert response.status_code == 404
    assert json.get('detail') == 'Юзера з ID 347293749239 не знайдено'