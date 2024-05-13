from typing import Annotated

from fastapi import APIRouter, Depends, Header

from src.services.customer import WalletService

router = APIRouter(prefix="/customers", tags=["Customers"])


@router.get("/info/")
async def get_info(
    user: Annotated[str, Header()],
    service: WalletService = Depends(),
):
    """
    Получение данных для Customer на главной странице
    """
    return await service.get_info(customer_uuid=user)


@router.get("/dashboard/")
async def get_wallet_info(
    user: Annotated[str, Header()],
    service: WalletService = Depends(),
):
    return await service.get_operations(customer_uuid=user)
