from functools import wraps
from aiogram.types import CallbackQuery
from ..requests_wrapper import BackendClient


def master_only(func):
    @wraps(func)
    async def wrapper(callback: CallbackQuery, *args, **kwargs):
        tg_id = callback.from_user.id
        exists = BackendClient.get(f'/masters/check-exists/{tg_id}')
        
        if not exists:
            await callback.message.reply("❌ У вас нет доступа к этой функции.", show_alert=True)

        return await func(callback, *args, **kwargs)

    return wrapper
