import pytest


# create service 
@pytest.mark.asyncio
async def test_create_service(client, test_master):
    data = {
        'title':  'Some test title for service',
        'description': 'Some test description for some test service test test test',
        'price': 1500,
        'master_id': test_master['user']['tg_id']
    }
    response = await client.post('/services/', json=data)

    assert response.status_code == 201


# service info
@pytest.mark.asyncio
async def test_service_info(client, test_service):
    id = test_service.get('id')
    response = await client.get(f'/services/{id}')
    assert response.status_code == 200


# get master`s services
@pytest.mark.asyncio
async def test_get_services_by_master(client, test_master):
    tg_id = test_master['user']['tg_id']
    response = await client.get(f'/services/by-master/{tg_id}')
    assert response.status_code == 200
    services = response.json()
    assert len(services) > 0


# get service by id
@pytest.mark.asyncio
async def test_get_service_by_id(client, test_service):
    response = await client.get(f'/services/{test_service.get('id')}')
    data = response.json()
    assert response.status_code == 200
    assert data.get('title') == 'Some test title for creating service'


# get count master services
@pytest.mark.asyncio
async def test_count_master_services(client, test_master):
    tg_id = test_master['user']['tg_id']
    response = await client.get(f'/services/count-master-services/{tg_id}')
    count = response.json()

    assert response.status_code == 200
    assert count > 0



# get master user profile by service ID
@pytest.mark.asyncio
async def test_get_master_user_profile_by_service_id(client, test_service):
    response = await client.get(f'/services/get-master-by-service/{test_service.get('id')}')
    assert response.status_code == 200


# delete service 
@pytest.mark.asyncio
async def test_delete_service(client,
                              test_service
                              ):
    response = await client.delete(f'/services/{test_service.get('id')}')
    assert response.status_code == 204



# edit service title
@pytest.mark.asyncio
async def test_edit_service_title(client, test_service):
    service_id = test_service.get('id')
    new_title = "Updated service title"

    response = await client.put(f"/services/{service_id}", json={"title": new_title})
    assert response.status_code == 200

    data = response.json()
    assert data["title"] == new_title
    assert data["description"] == test_service["description"]
    assert data["price"] == test_service["price"]


# edit service description
@pytest.mark.asyncio
async def test_edit_service_description(client, test_service):
    service_id = test_service.get('id')
    new_description = "Updated description text for testing test some test text"

    response = await client.put(f"/services/{service_id}", json={"description": new_description})
    assert response.status_code == 200

    data = response.json()
    assert data["description"] == new_description
    assert data["title"] == test_service["title"]
    assert data["price"] == test_service["price"]


# edit service price 
@pytest.mark.asyncio
async def test_edit_service_price(client, test_service):
    service_id = test_service.get('id')
    new_price = 2500

    response = await client.put(f"/services/{service_id}", json={"price": new_price})
    assert response.status_code == 200

    data = response.json()
    assert data["price"] == new_price
    assert data["title"] == test_service["title"]
    assert data["description"] == test_service["description"]