from datetime import datetime


def parse_datetime_or_none(date_str: str) -> datetime | None:
    date_str = date_str.strip().lower()
    if date_str == "ні":
        return None
    try:
        return datetime.strptime(date_str, "%Y-%m-%d %H:%M")
    except ValueError:
        raise ValueError(
            "Некоректний формат! Введи дату у форматі: 2026-10-25 17:00\nАбо введи 'ні', якщо часу немає"
        )