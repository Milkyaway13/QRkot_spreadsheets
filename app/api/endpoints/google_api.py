from datetime import datetime

from aiogoogle import Aiogoogle
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.constants import FORMAT
from app.core.db import get_async_session
from app.core.google_client import get_service
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.services.google_api import (
    set_user_permissions,
    spreadsheets_create,
    spreadsheets_update_value,
)

router = APIRouter()


@router.get("/", response_model=str, dependencies=(Depends(current_superuser),))
async def get_report(
    session: AsyncSession = Depends(get_async_session),
    wrapper_services: Aiogoogle = Depends(get_service),
):
    current_time = datetime.now().strftime(FORMAT)
    projects = await charity_project_crud.get_projects_by_completion_rate(session)
    spreadsheet_id = await spreadsheets_create(current_time, wrapper_services)
    await set_user_permissions(spreadsheet_id, wrapper_services)
    await spreadsheets_update_value(
        spreadsheet_id, projects, current_time, wrapper_services
    )
    return (
        f"Ссылка на таблицу: "
        f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}/edit#gid=0"
    )
