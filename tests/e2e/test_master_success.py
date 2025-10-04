import pytest 


@pytest.mark.asyncio
@pytest.mark.run(order=1)
async def test_create_master(client, test_user):
    data = {
        'specialization': 'Developer',
        'description': 'Some test descriptioon for creating master',
        'experience_years': 3,
        'location': 'Some Location',
        'schedule': 'Monday-Friday => 09.00-19.00',
        'user_id': test_user.get('tg_id')
    }

    print('*' * 80)
    print(data)

    response = await client.post(f'/masters/', json=data)
    assert response.status_code == 201