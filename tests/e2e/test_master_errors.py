import pytest 


#_______________________________C-R-E-A-T-E________________________________

@pytest.mark.asyncio
async def test_create_master_error_409(client, test_user):
    data = {
        'specialization': 'Розробник',
        'description': 'Some test description for create user test test test test',
        'experience_years': 3,
        'location': 'Some Location',
        'schedule': 'Monday-Friday => 09.00-19.00',
        'user_id': test_user.get('tg_id')
    }

    response = await client.post(f'/masters/', json=data)

    response = await client.post(f'/masters/', json=data)
    assert response.status_code == 409


@pytest.mark.asyncio
async def test_create_master_error_422_description(client, test_user):
    data = {
        'specialization': 'Розробник',
        'description': 'Short',
        'experience_years': 3,
        'location': 'Some Location',
        'schedule': 'Monday-Friday => 09.00-19.00',
        'user_id': test_user.get('tg_id')
    }

    response = await client.post(f'/masters/', json=data)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_create_master_error_404_user_not_found(client):
    data = {
        'specialization': 'Розробник',
        'description': 'Some test description for create user test test test test',
        'experience_years': 3,
        'location': 'Some Location',
        'schedule': 'Monday-Friday => 09.00-19.00',
        'user_id': 123324
    }

    response = await client.post(f'/masters/', json=data)
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_create_master_error_422_incotrrect_spec(client, test_user):
    data = {
        'specialization': 'Some',
        'description': 'Some test description for create user test test test test',
        'experience_years': 3,
        'location': 'Some Location',
        'schedule': 'Monday-Friday => 09.00-19.00',
        'user_id': test_user.get('tg_id')
    }

    response = await client.post(f'/masters/', json=data)
    assert response.status_code == 422

#_______________________________C-R-E-A-T-E________________________________
