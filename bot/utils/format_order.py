from datetime import datetime

def format_order_response(order: dict) -> str:
    status_map = {
        "pending": "Очікується",
        "accepted": "Прийнято",
        "completed": "Завершено",
        "cancelled": "Скасовано"
    }
    status_ukr = status_map.get(order.get("status"), order.get("status", "Невідомо"))

    def fmt_date(dt):
        return datetime.fromisoformat(dt).strftime("%Y-%m-%d %H:%M") if dt else None

    created_at = fmt_date(order.get("created_at"))
    deadline = fmt_date(order.get("deadline")) if order.get("deadline") else None
    scheduled_at = fmt_date(order.get("scheduled_at")) if order.get("scheduled_at") else None


    parts = [f"🧾 <b>Замовлення</b>\n"]

    if order.get("description"):
        parts.append(f"💬 <b>Опис:</b> {order['description']}")
    if order.get("price") is not None:
        parts.append(f"💰 <b>Запропонована ціна:</b> {order['price']} грн")
    if created_at:
        parts.append(f"📅 <b>Створено:</b> {created_at}")
    if scheduled_at:
        parts.append(f"⏰ <b>Заплановано:</b> {scheduled_at}")
    if deadline:
        parts.append(f"🕓 <b>Дедлайн:</b> {deadline}")
    if status_ukr:
        parts.append(f"📦 <b>Статус:</b> {status_ukr}")

    return "\n".join(parts)
