from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from ..utils import check_user, BackendClient
from ..keyboards import register_kb, select_master_by_specialization_kb


masters_catalog_router = Router()
PAGE_SIZE = 1


async def fetch_masters(spec: str):
    status, masters = await BackendClient.get(f"/masters/by-specialization/{spec}")
    return masters


@masters_catalog_router.message(F.text == "Знайти майстра")
async def masters_catalog(message: Message):
    status, exists = await check_user(message.from_user.id)
    if not exists:
        await message.reply(
            "Для того щоб продивитись список майстрів - потрібно пройти регістрацію",
            reply_markup=register_kb()
        )
    else:
        await message.reply(
            "Обери спеціалізацію для майстра",
            reply_markup=select_master_by_specialization_kb()
        )


def build_masters_kb(masters, page, total_pages, spec):
    builder = InlineKeyboardBuilder()
    for m in masters:
        builder.row(
            InlineKeyboardButton(
                text=f"{m['user']['name']} ⭐{m['rating']}",
                callback_data=f"show_master:{m['user']['tg_id']}:{page}:{spec}"
            )
        )
    if page > 1:
        builder.button(text="⬅️ Назад", callback_data=f"masters_page:{page-1}:{spec}")
    if page < total_pages:
        builder.button(text="➡️ Вперед", callback_data=f"masters_page:{page+1}:{spec}")
    builder.adjust(1)
    return builder.as_markup()


def build_master_detail_kb(master_id, page, spec):
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="✅ Замовити", callback_data=f"make_order_{master_id}")
    )
    builder.row(
        InlineKeyboardButton(text="⬅️ Назад", callback_data=f"masters_page:{page}:{spec}")
    )
    return builder.as_markup()


@masters_catalog_router.callback_query(F.data.startswith("select_spec_"))
async def show_masters(callback: CallbackQuery):
    spec = callback.data.removeprefix("select_spec_")
    await callback.message.edit_reply_markup(reply_markup=None)

    masters = await fetch_masters(spec)
    if not masters:
        await callback.message.answer("❌ Майстрів не знайдено!")

    else:
        page = 1
        total_pages = max(1, (len(masters) + PAGE_SIZE - 1) // PAGE_SIZE)
        masters_page = masters[(page-1)*PAGE_SIZE : page*PAGE_SIZE]

        kb = build_masters_kb(masters_page, page, total_pages, spec)
        await callback.message.answer(
            f"🔎 Майстри ({spec}) — Сторінка {page}/{total_pages}",
            reply_markup=kb
        )
        await callback.answer()


@masters_catalog_router.callback_query(F.data.startswith("masters_page:"))
async def change_page(callback: CallbackQuery):
    _, page, spec = callback.data.split(":")
    page = int(page)

    masters = await fetch_masters(spec)
    if not masters:
        await callback.message.edit_text("❌ Майстрів не знайдено!")

    total_pages = max(1, (len(masters) + PAGE_SIZE - 1) // PAGE_SIZE)
    if page > total_pages:
        page = total_pages
    masters_page = masters[(page-1)*PAGE_SIZE : page*PAGE_SIZE]

    kb = build_masters_kb(masters_page, page, total_pages, spec)
    await callback.message.edit_text(
        f"🔎 Майстри ({spec}) — Сторінка {page}/{total_pages}",
        reply_markup=kb
    )
    await callback.answer()


@masters_catalog_router.callback_query(F.data.startswith("show_master:"))
async def show_master_detail(callback: CallbackQuery):
    _, master_id, page, spec = callback.data.split(":")
    master_id = int(master_id)
    page = int(page)

    masters = await fetch_masters(spec)
    master = next((m for m in masters if m["user"]["tg_id"] == master_id), None)

    if not master:
        await callback.answer("Майстра не знайдено", show_alert=True)

    text = f"""
<b>👨‍🔧 {master['user']['name']}</b>

<pre>
🛠️ Спеціалізація: {master['specialization']}
📄 Опис:\n{master['description']}\n
📊 Досвід: {master['experience_years']} років
📍 Локація: {master['location']}
⏰ Графік роботи:\n{master['schedule']}\n
⭐ Рейтинг: {master['rating']}
👍 Гарних відгуків: {master['good_grades']}
👎 Поганих відгуків: {master['bad_grades']}
</pre>
Всі його послуги будуть доступні за кнопкою 'Замовити'
"""
    kb = build_master_detail_kb(master_id, page, spec)
    await callback.message.edit_text(text, reply_markup=kb, parse_mode="HTML")