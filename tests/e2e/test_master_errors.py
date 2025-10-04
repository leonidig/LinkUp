import pytest 
import warnings
from sqlalchemy.exc import SAWarning


#create master with 409 conflict ( already created)
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


#create master with 409 conflict ( already created)  
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



#create master with 404 not found ( not exists user with this telegram_id )
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


#create master with 422 unprocessable entity ( invalid specialization )
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
    assert "Спеціалізація Some не допустима" in response.json()['detail'][0]['msg']


#check_exists
@pytest.mark.asyncio
async def test_check_master_exists_incorrect_id(client):
    response = await client.get('/masters/check-exists/111111')
    assert response.json() is False


# get masters by selected specialization 404 not found ( incorrect spec)

@pytest.mark.filterwarnings("ignore::sqlalchemy.exc.SAWarning")
@pytest.mark.asyncio
async def test_get_master_by_invalid_spec(client):
    response = await client.get('/masters/by-specialization/some')
    assert response.status_code == 422  
    errors = response.json()
    print('*' * 100)
    print(errors)