import pytest


# create
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


# get info 
@pytest.mark.asyncio
async def test_get_order_info(client, test_order):
    response = await client.get(f'/orders/{test_order.get('id')}')

    assert response.status_code == 200



@pytest.mark.asyncio
@pytest.mark.parametrize("action", [
    'pending',
    'confirmed',
    'completed',
    'cancelled'
])
async def test_change_order_status(client, test_order, action):
    response = await client.put(
        f"/orders/set-status/{test_order.get('id')}?action={action}"
    )

    if action == "pending":
        assert response.status_code == 422
    else:
        assert response.status_code == 200
        data = response.json()
        assert data.get("new_status") == action


# test gets all user orders
@pytest.mark.asyncio
async def test_get_filtered_orders(client, test_user):
    response = await client.get(
        f"/orders/filtered/{test_user.get('tg_id')}",
        params={"status": "all"}
    )

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


@pytest.mark.asyncio
async def test_urser_have_orders(client,
                                 test_user
                                ):
    response = await client.get(f'/orders/have/{test_user.get('tg_id')}')
    data = response.json()
    assert response.status_code == 200
    assert data.get('has_orders') == True