from datetime import datetime

from app.core.config import settings

LIFETIME = 3600
MIN_PASSWORD_LENGHT = 3
NAME_MAX_LENGHT = 100
NAME_MIN_LENHGT = 1
FORMAT = "%Y/%m/%d %H:%M:%S"
ROW_COUNT = (100,)
COLUMN_COUNT = 10
SPREADSHEETS_BODY = {
    "properties": {"title": "", "locale": "ru_RU"},
    "sheets": (
        {
            "properties": {
                "sheetType": "GRID",
                "sheetId": 0,
                "title": "Лист1",
                "gridProperties": {"rowCount": ROW_COUNT, "columnCount": COLUMN_COUNT},
            }
        },
    ),
}
PERMISSIONS_BODY = {"type": "user", "role": "writer", "emailAddress": settings.email}
# Оставил здесь список, потому что в функции spreadsheets_update_value
# использую list comprehension
# В остальных местах поменял на кортежи, где это возможно
TABLE_VALUES = [
    ["Отчёт от", datetime.now().strftime(FORMAT)],
    ["Топ проектов по скорости закрытия"],
    ["Название проекта", "Время сбора", "Описание"],
]
UPDATE_BODY = {"majorDimension": "ROWS", "values": TABLE_VALUES}
