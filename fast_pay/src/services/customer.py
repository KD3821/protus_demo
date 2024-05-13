from typing import List

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from src import models
from src.database import async_session, get_session
from src.logger import logger
from src.schemas.account import Account, AccountInfoCustomer
from src.schemas.operation import OperationService
from src.schemas.wallet import Wallet, WalletInfo


class WalletService:
    def __init__(self, session: async_session = Depends(get_session)):
        self.session = session

    async def get_accounts(self, email: str) -> List[Account]:
        query = (
            select(models.Account)
            .where(models.Account.owner == email)
            .options(joinedload(models.Account.provider))
        )

        res = await self.session.execute(query)

        accounts = res.scalars()

        return accounts

    async def get_wallet(self, customer_uuid: str) -> Wallet:
        query = select(models.Wallet).where(
            models.Wallet.customer_uuid == customer_uuid
        )

        res = await self.session.execute(query)

        return res.scalar()

    async def get_info(self, customer_uuid: str) -> dict:

        wallet = await self.get_wallet(customer_uuid)

        accounts = await self.get_accounts(wallet.email)

        wallet_info = WalletInfo(
            username=wallet.username,
            customer_uuid=wallet.customer_uuid,
            balance=wallet.balance,
        )

        account_list = [
            AccountInfoCustomer(
                company_name=acc.provider.name,
                account_number=acc.account_number,
                registered_at=acc.registered_at,
                balance=acc.balance,
            )
            for acc in accounts
        ]

        logger.info(
            f"[Customer info] email: {wallet.email} | customer_uuid: {customer_uuid}"
        )

        return {"wallet": wallet_info, "accounts": account_list}

    async def get_operations(self, customer_uuid) -> dict:
        wallet = await self.get_wallet(customer_uuid)

        wallet_info = WalletInfo(
            username=wallet.username,
            customer_uuid=wallet.customer_uuid,
            balance=wallet.balance,
        )

        query = (
            select(models.Account)
            .where(models.Account.owner == wallet.email)
            .options(
                joinedload(models.Account.operations)
                .joinedload(models.Operation.service)
                .joinedload(models.Service.provider)
            )
        )

        res = await self.session.execute(query)

        accounts = res.scalars().unique()

        account_operations = [account.operations for account in accounts]

        operations = list()

        for operations_list in account_operations:
            for op in operations_list:
                operations.append(
                    OperationService(
                        date=op.date,
                        service_name=op.service.name,
                        provider_name=op.service.provider.name,
                        reference_code=op.reference_code,
                        invoice_number=op.invoice_number,
                        amount=op.amount,
                        remaining_balance=op.remaining_balance,
                    )
                )

        return {"wallet": wallet_info, "operations": operations}
