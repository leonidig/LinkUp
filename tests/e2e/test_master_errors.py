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
        'tg_id': test_user.get('tg_id')
    }

    response = await client.post(f'/masters/', json=data)

    response = await client.post(f'/masters/', json=data)
    assert response.status_code == 409


#create master with 422 ( short description)  
@pytest.mark.asyncio
async def test_create_master_invalid_description(client, test_user):
    data = {
        'specialization': 'Розробник',
        'description': 'Short',
        'experience_years': 3,
        'location': 'Some Location',
        'schedule': 'Monday-Friday => 09.00-19.00',
        'tg_id': test_user.get('tg_id')
    }

    response = await client.post('/masters/', json=data)

    assert response.status_code == 422
    detail = response.json()["detail"]

    assert any(err["loc"][-1] == "description" for err in detail)
    assert any("55" in err["msg"] or "at least" in err["msg"] for err in detail)


#create master with 422 unprocessable entity ( invalid specialization )
@pytest.mark.asyncio
async def test_create_master_invalid_spec(client, test_user):
    data = {
        'specialization': 'Some',
        'description': 'Some test description for create user test test test test',
        'experience_years': 3,
        'location': 'Some Location',
        'schedule': 'Monday-Friday => 09.00-19.00',
        'tg_id': test_user.get('tg_id')
    }

    response = await client.post(f'/masters/', json=data)

    assert response.status_code == 422
    assert "Спеціалізація Some не допустима" in response.json()['detail'][0]['msg']


#create master with 422 unprocessable entity ( invalid experience_years )
@pytest.mark.asyncio
async def test_create_master_invalid_exp_years(client, test_user):
    data = {
        'specialization': 'Some',
        'description': 'Some test description for create user test test test test',
        'experience_years': -1,
        'location': 'Some Location',
        'schedule': 'Monday-Friday => 09.00-19.00',
        'tg_id': test_user.get('tg_id')
    }

    response = await client.post(f'/masters/', json=data)
    assert response.status_code == 422


#create master with 422 unprocessable entity ( invalid location )
@pytest.mark.asyncio
async def test_create_master_invalid_location(client, test_user):
    data = {
        'specialization': 'Some',
        'description': 'Some test description for create user test test test test',
        'experience_years': -1,
        'location': 'ABC',
        'schedule': 'Monday-Friday => 09.00-19.00',
        'tg_id': test_user.get('tg_id')
    }

    response = await client.post(f'/masters/', json=data)
    assert response.status_code == 422


#create master with 422 unprocessable entity ( invalid schedule )
@pytest.mark.asyncio
async def test_create_master_invalid_schedule(client, test_user):
    data = {
        'specialization': 'Some',
        'description': 'Some test description for create user test test test test',
        'experience_years': -1,
        'location': 'Some Location',
        'schedule': 'ABC',
        'tg_id': test_user.get('tg_id')
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
        'tg_id': 123324
    }

    response = await client.post(f'/masters/', json=data)
    assert response.status_code == 404



#check master exists 404 not found ( incorrect telegram_id )
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



# get master by telegram id 404 ( user dont have master profile)
@pytest.mark.asyncio
async def test_master_info_with_not_exists_master_profile(
                                        client,
                                        test_user_whthout_master_profile
                                    ):
    user = test_user_whthout_master_profile
    response = await client.get(f'/masters/{user.get('tg_id')}')
    json = response.json()
    assert json.get('detail') == 'Майстра не знайдено'
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_create_master_error_422_extra_field(client, test_user):
    data = {
        'specialization': 'Розробник',
        'description': 'Some valid description for testing',
        'experience_years': 5,
        'location': 'Some Location',
        'schedule': 'Monday-Friday => 09.00-19.00',
        'tg_id': test_user.get('tg_id'),
        'invalid_key': 'oops'
    }

    response = await client.post('/masters/', json=data)

    assert response.status_code == 422
    # detail = response.json()["detail"]
    # assert any("extra fields not permitted" in err["msg"] for err in detail)