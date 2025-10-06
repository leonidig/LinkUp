import pytest


@pytest.mark.asyncio
async def test_create_order(client, test_user,
                            test_user_whthout_master_profile,
                            test_master,
                            test_service
                        ):
    data = {
        "user_tg_id": test_user_whthout_master_profile.get('tg_id'),
        "master_tg_id": test_master['user']['tg_id'],
        "service_id": test_service.get('id'),
        "description": "Some description for test create order",
        "price": 200,
    }

    response = await client.post('/orders/', json=data)
    assert response.status_code == 201