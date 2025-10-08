from .requests_wrapper import BackendClient


async def check_user(tg_id: int) -> bool:
    status, response = await BackendClient.get(f'/users/check-exists/{tg_id}')
    return response

async def check_master(tg_id: int) -> bool:
    status, response = await BackendClient.get(f'/masters/check-exists/{tg_id}')
    return response