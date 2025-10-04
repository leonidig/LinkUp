import pytest


def get_error_msgs(response):
    json_data = response.json()
    if response.status_code != 422 or "detail" not in json_data:
        raise ValueError(f"No validation errors in response: {json_data}")
    # возвращаем список всех msg
    return [err["msg"] for err in json_data["detail"]]



# create service 422 ( short description )
@pytest.mark.asyncio
async def test_create_service_short_description(client, test_master):
    tg_id = test_master.get('tg_id')
    data = {
        "title": "Some test title for creating service",
        "description": "Some short description",
        "price": 1500,
        "master_id": tg_id
    }
    
    response = await client.post('/services/', json=data)
    assert response.status_code == 422
    msg = get_error_msgs(response=response)
    assert 'String should have at least 55 characters' in msg


# create service 422 ( invalid telegram id)
@pytest.mark.asyncio
async def test_create_service_invalid_master_id(client):
    data = {
        "title": "Some test title for creating service",
        "description": "Some short description for test creating service test test",
        "price": 1500,
        "master_id": 111
    }
    response = await client.post('/services/', json=data)
    assert response.status_code == 422
    msg = get_error_msgs(response)
    assert 'Value error, Некорректний формат Telegram ID' in msg



# create service 422 ( long title )
@pytest.mark.asyncio
async def test_create_service_long_title(client, test_master):
    data = {
        "title": "Some test title for creating service test test test" * 3,
        "description": "Some short description for test creating service test test",
        "price": 1500,
        "master_id": test_master.get('tg_id')
    }

    response = await client.post('/services/', json=data)
    msg = get_error_msgs(response)
    assert "String should have at most 122 characters" in msg
    assert response.status_code == 422



# create service 422 ( low price )
async def test_create_service_low_price(client, test_master):
    data = {
        "title": "Some test title for creating service",
        "description": "Some short description for test creating service test test",
        "price": -1,
        "master_id": test_master.get('tg_id')
    }
    response = await client.post('/services/', json=data)
    msg = get_error_msgs(response)
    assert 'Input should be greater than 0' in msg
    assert response.status_code == 422