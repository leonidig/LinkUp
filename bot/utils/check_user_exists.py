from .requests_wrapper import BackendClient


def check_user(tg_id: int):
    return BackendClient.get(f'/users/check-exists/{tg_id}')


def check_master(tg_id: int):
    return BackendClient.get(f'/masters/check-exists/{tg_id}')