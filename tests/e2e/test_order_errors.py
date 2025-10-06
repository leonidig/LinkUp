import pytest
from . import get_error_msgs


# create order 422 ( chort description)
@pytest.mark.asyncio
async def test_create_order_short_description(client,
                            test_user_whthout_master_profile,
                            test_master,
                            test_service
                        ):
    data = {
        "user_tg_id": test_user_whthout_master_profile.get('tg_id'),
        "master_tg_id": test_master['user']['tg_id'],
        "service_id": test_service.get('id'),
        "description": "Test",
        "price": 200,
    }

    response = await client.post('/orders/', json=data)
    assert response.status_code == 422
    assert get_error_msgs(response) == ['String should have at least 25 characters']


# create order 422 ( invalid price )
@pytest.mark.asyncio
async def test_create_order_invalid_price(client,
                            test_user_whthout_master_profile,
                            test_master,
                            test_service
                        ):
    data = {
        "user_tg_id": test_user_whthout_master_profile.get('tg_id'),
        "master_tg_id": test_master['user']['tg_id'],
        "service_id": test_service.get('id'),
        "description": "Test description for order",
        "price": 99999999999,
    }

    response = await client.post('/orders/', json=data)
    assert response.status_code == 422
    assert get_error_msgs(response) == ['Input should be less than 999999']



# create order 422 ( long master telegram ID)
@pytest.mark.asyncio
async def test_create_order_long_master_tg_id(client,
                            test_master,
                            test_service
                        ):
    data = {
        "user_tg_id": 93254053475934,
        "master_tg_id": test_master['user']['tg_id'],
        "service_id": test_service.get('id'),
        "description": "Test description for order",
        "price": 1500,
    }

    response = await client.post('/orders/', json=data)
    assert response.status_code == 422
    assert get_error_msgs(response) == ['Value error, Некоректний формат — має бути від 6 до 10 цифр']
