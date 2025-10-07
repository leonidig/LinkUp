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