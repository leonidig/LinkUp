import pytest


@pytest.mark.asyncio
async def test_create_ref_user_not_found(client, test_master):
    data = {
            "code": 1111111,
            "master_tg_id": test_master['user']['tg_id'],
            "created_by_tg_id": 1111111,
            "bonus_amount": test_master.get('ref_bonus')
        }
    response = await client.post('/refferal/', json=data)
    json = response.json()
    assert json.get('detail') == 'Користувача з телеграм ID 1111111 не знайдено'
    
    assert response.status_code == 404