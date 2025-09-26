from .requests_wrapper import BackendClient


def check_user(tg_id: int):
    return BackendClient.get(f'/users/check-exists/{tg_id}')