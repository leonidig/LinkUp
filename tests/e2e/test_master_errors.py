import pytest 


@pytest.mark.asyncio
@pytest.mark.run(order=2)
async def test_create_master_error(client, test_user):
    data = {
        'specialization': 'Developer',
        'description': 'dsfdksj fksdj kfsdf klweiweirw[peow[fk jsko kdsfh iweup riqw[w- odweowek]]]',
        'experience_years': 3,
        'location': 'Some Location',
        'schedule': 'Monday-Friday => 09.00-19.00',
        'user_id': test_user.get('tg_id')
    }

    response = await client.post(f'/masters/', json=data)

    response = await client.post(f'/masters/', json=data)
    assert response.status_code == 409