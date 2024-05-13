from datetime import datetime
from decimal import Decimal

import shortuuid
from fastapi import Depends
from sqlalchemy import and_, select

from src import models
from src.database import async_session, get_session
from src.logger import logger
from src.proto.handlers.customers import get_customer_uuid
from src.schemas.account import Account, AccountCreate, AccountingCreate


class AccountService:
    def __init__(self, session: async_session = Depends(get_session)):
        self.session = session

    async def create_account(self, client_id: str, owner: str) -> Account:
        account_number_exists = True

        while account_number_exists:
            account_number_exists = False

            new_account_number = shortuuid.uuid()

            query = select(models.Account).where(
                models.Account.account_number == new_account_number
            )

            res = await self.session.execute(query)

            account_same_number = res.scalar()

            if account_same_number:
                account_number_exists = True

        account = models.Account(
            client_id=client_id,
            owner=owner,
            account_number=new_account_number,  # noqa
            registered_at=datetime.utcnow(),
            debit=Decimal("0.00"),
            credit=Decimal("0.00"),
            balance=Decimal("0.00"),
        )

        self.session.add(account)
        await self.session.commit()

        logger.info(
            f"PROTUS-CLI: Account created * "
            f"[id: {account.id} | client_id: {client_id} | email: {owner} | account_number: {new_account_number}]"
        )

        return account

    async def get_or_create_account(self, data: AccountCreate) -> Account:
        query = select(models.Account).where(
            and_(
                models.Account.client_id == data.client_id,
                models.Account.owner == data.owner,
            )
        )

        res = await self.session.execute(query)

        account = res.scalar()

        if account is None:
            account = await self.create_account(data.client_id, data.owner)

        return account

    async def create_customer_accounting(self, data: AccountingCreate) -> Account:
        new_customer_uuid = await get_customer_uuid(data.email, data.username)

        new_wallet = models.Wallet(
            email=data.email,
            username=data.username,
            customer_uuid=new_customer_uuid,
            debit=Decimal("0.00"),
            credit=Decimal("0.00"),
            balance=Decimal("0.00"),
        )

        self.session.add(new_wallet)
        await self.session.commit()

        new_account = await self.create_account(data.client_id, data.email)

        return new_account
