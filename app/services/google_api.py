from datetime import datetime

from aiogoogle import Aiogoogle

from app.core.constants import (
    PERMISSIONS_BODY, SPREADSHEETS_BODY,
    TABLE_VALUES, UPDATE_BODY
)
from app.models.charity_project import CharityProject


async def spreadsheets_create(
    current_time: datetime, wrapper_services: Aiogoogle
) -> str:
    SPREADSHEETS_BODY["properties"]["title"] = f"Отчёт от {current_time}"

    service = await wrapper_services.discover("sheets", "v4")
    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=SPREADSHEETS_BODY)
    )
    spreadsheet_id = response["spreadsheetId"]
    return spreadsheet_id


async def set_user_permissions(
    spreadsheet_id: str, wrapper_services: Aiogoogle
) -> None:
    service = await wrapper_services.discover("drive", "v3")
    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheet_id, json=PERMISSIONS_BODY, fields="id"
        )
    )


async def spreadsheets_update_value(
    spreadsheet_id: str,
    projects: list[CharityProject],
    current_time: datetime,
    wrapper_services: Aiogoogle,
) -> None:
    TABLE_VALUES[0][1] = current_time

    service = await wrapper_services.discover("sheets", "v4")

    TABLE_VALUES.extend([
        str(project.name),
        str(project.close_date - project.create_date),
        str(project.description),
    ] for project in projects)

    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheet_id,
            range="A1:E30",
            valueInputOption="USER_ENTERED",
            json=UPDATE_BODY,
        )
    )
