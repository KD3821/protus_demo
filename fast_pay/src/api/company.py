from typing import Annotated

from fastapi import APIRouter, Depends, Header

from src.services.company import ProviderService

router = APIRouter(prefix="/companies", tags=["Companies"])


@router.get("/info/")
async def get_info(
    user: Annotated[str, Header()],
    service: ProviderService = Depends(),
):
    """
    Получение данных для Company на главной странице
    """
    return await service.get_info(client_id=user)


@router.get("/dashboard/")
async def get_services(
    user: Annotated[str, Header()],
    service: ProviderService = Depends(),
):
    """
    Набор услуг Company
    """
    return await service.get_dashboard(client_id=user)
