import pytest 

# create
@pytest.mark.asyncio
async def test_create_master(client, test_user):
    data = {
        'specialization': 'Розробник',
        'description': 'Some test descriptioon for creating master success test test',
        'experience_years': 3,
        'location': 'Some Location',
        'schedule': 'Monday-Friday => 09.00-19.00',
        'user_id': test_user.get('tg_id')
    }


    response = await client.post(f'/masters/', json=data)
    assert response.status_code == 201


#check_exists
@pytest.mark.asyncio
async def test_check_exists(client, test_user):
    response = await client.get(f'/masters/check-exists/{test_user.get('tg_id')}')
    assert response.status_code == 200


#by_specialization
@pytest.mark.asyncio
@pytest.mark.parametrize("spec", [
        "Розробник",
        "Будівельник",
        "Дизайнер",
        "Фотограф",
        "Водій",
        "Копірайтер",
        "Майстер по ремонту",
        "Майстер краси",
        "Різноробочий",
        "Репетитор"
    ])
async def test_masters_by_spec(client, spec):
        response = await client.get(f'/masters/by-specialization/{spec}')
        assert response.status_code == 200
        data = response.json()
        assert all(m['specialization'] == spec for m in data)


#master_info
@pytest.mark.asyncio
async def test_master_info(client, test_master):
    tg_id = test_master.get('user_id')
    
    response = await client.get(f'/masters/{tg_id}')
    assert response.status_code == 200
    
    data = response.json()

    assert data['specialization'] == 'Розробник'
    assert data.get('user').get('tg_id') == tg_id