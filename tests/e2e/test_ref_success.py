import pytest


@pytest.mark.asyncio
async def test_create_ref(client, test_master, test_user):
    data = {
            "code": test_user.get('tg_id'),
            "master_tg_id": test_master['user']['tg_id'],
            "created_by_tg_id": test_user.get('tg_id'),
            "bonus_amount": test_master.get('ref_bonus')
        }
    response = await client.post('/refferal/', json=data)

    print('*' * 10)
    print(response.json())
    
    assert response.status_code == 201