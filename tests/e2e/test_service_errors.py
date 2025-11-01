import pytest
from . import get_error_msgs


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
@pytest.mark.asyncio
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



# get master services 404 ( invalid master telegram id )
@pytest.mark.asyncio
async def test_get_master_services_invalid_tg_id(client):
    response = await client.get(f'/services/by-master/1')
    error = response.json()

    assert response.status_code == 404
    assert error.get('detail') == 'Майстра з telegram ID 1 не знайдено'


# get service 404 ( not exists service with this ID)
@pytest.mark.asyncio
async def test_get_service_info_invalid_tg_id(client):
    response = await client.get('/services/139820')
    error = response.json()

    assert error.get('detail') == 'Сервіс з ID 139820 не знайдено'
    assert response.status_code == 404
    

# get master services count 404 ( invalid telegram ID )
@pytest.mark.asyncio
async def test_get_master_services_count_invalid_id(client):
    response = await client.get('/services/count-master-services/9999999')
    error = response.json()

    assert response.status_code == 404
    assert error.get('detail') == 'Майстера з ID 9999999 не знайдено'


# delete service 404 ( invalid ID )
@pytest.mark.asyncio
async def test_delete_service_invalid_id(client):
    response = await client.delete('/services/1111111')
    assert response.status_code == 404


# edit service title 404 ( service ID not found )
@pytest.mark.asyncio
async def test_edit_service_title_404(client, test_service):
    service_id = test_service.get('id')
    new_title = "Updated service title"

    response = await client.put(f"/services/123457", json={"title": new_title})
    assert response.status_code == 404


# edit service 422 ( short title )
@pytest.mark.asyncio
async def test_edit_service_short_title(client, test_service):
    service_id = test_service.get('id')
    new_title = "Some"

    response = await client.put(f"/services/{test_service.get('id')}", json={"title": new_title})
    assert response.status_code == 422
    data = response
    assert ['String should have at least 20 characters'] == get_error_msgs(data)



# edit service 422 ( invalid price )
@pytest.mark.asyncio
async def test_edit_service_low_price(client, test_service):
    service_id = test_service.get('id')
    new_price = -1

    response = await client.put(f"/services/{test_service.get('id')}", json={"price": new_price})
    assert response.status_code == 422
    assert ['Input should be greater than 0'] == get_error_msgs(response)


# edit service 400 ( with no data )
@pytest.mark.asyncio
async def test_edit_service_no_data(client, test_service):
    service_id = test_service.get('id')

    response = await client.put(f"/services/{test_service.get('id')}", json={})
    json = response.json()
    assert response.status_code == 400
    assert json.get('detail') == 'Не передано жодного поля для оновлення'



@pytest.mark.asyncio
async def test_edit_service_short_description(client, test_service):
    service_id = test_service.get('id')
    new_description = 'Some '

    response = await client.put(f"/services/{test_service.get('id')}", json={"description": new_description})
    assert response.status_code == 422
    assert ['String should have at least 55 characters'] == get_error_msgs(response)