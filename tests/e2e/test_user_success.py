import pytest


async def test_get_user(client, test_user):
    tg_id = test_user["tg_id"]
    response = await client.get(f"/users/check-exists/{tg_id}")
    assert response.status_code == 200
    assert response.json() == True