from typing import List

from fastapi import Depends
from sqlalchemy import select

from src import models
from src.database import async_session, get_session
from src.logger import logger
from src.schemas.account import Account, AccountInfoCompany
from src.schemas.provider import ProviderInfo
from src.schemas.service import Service, ServiceInfo


class ProviderService:
    def __init__(self, session: async_session = Depends(get_session)):
        self.session = session

    async def get_services(self, client_id: str) -> List[Service]:
        query = select(models.Service).where(models.Service.client_id == client_id)

        res = await self.session.execute(query)

        services = res.scalars()

        return services

    async def get_accounts(self, client_id: str) -> List[Account]:
        query = select(models.Account).where(models.Account.client_id == client_id)

        res = await self.session.execute(query)

        return res.scalars()

    async def get_provider(self, client_id: str) -> ProviderInfo:

        query = select(models.Provider).where(models.Provider.client_id == client_id)

        res = await self.session.execute(query)

        return res.scalar()

    async def get_info(self, client_id: str) -> dict:
        provider = await self.get_provider(client_id)

        accounts = await self.get_accounts(client_id)

        provider_info = ProviderInfo(
            name=provider.name,
            client_id=provider.client_id,
            client_secret=provider.client_secret,
        )

        account_list = [
            AccountInfoCompany(
                account_number=acc.account_number,
                owner=acc.owner,
                registered_at=acc.registered_at,
                balance=acc.balance,
            )
            for acc in accounts
        ]

        logger.info(
            f"[Company info] email: {provider.email} | name: {provider.name} | client_id: {provider.client_id}"
        )

        return {"provider": provider_info, "accounts": account_list}

    async def get_dashboard(self, client_id: str) -> dict:
        provider = await self.get_provider(client_id)

        services = await self.get_services(client_id)

        provider_info = ProviderInfo(
            name=provider.name,
            client_id=provider.client_id,
            client_secret=provider.client_secret,
        )

        service_list = [
            ServiceInfo(service_id=serv.service_id, name=serv.name, price=serv.price)
            for serv in services
        ]

        logger.info(
            f"[Company Dashboard] email: {provider.email} | name: {provider.name} | client_id: {provider.client_id}"
        )

        return {"provider": provider_info, "services": service_list}
