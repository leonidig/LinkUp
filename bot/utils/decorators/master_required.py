from functools import wraps
from aiogram.types import CallbackQuery, Message
from ..requests_wrapper import BackendClient


def master_only(func):
    @wraps(func)
    async def wrapper(event: CallbackQuery | Message, *args, **kwargs):
        tg_id = event.from_user.id

        status, exists = await BackendClient.get(f'/masters/check-exists/{tg_id}')

        if not exists:
            if isinstance(event, CallbackQuery):
                await event.answer("❌ У тебе немає доступу для цієї функції", show_alert=True)
            else:
                await event.reply("❌ У тебе немає доступу для цієї функції")
            return

        return await func(event, *args, **kwargs)

    return wrapper