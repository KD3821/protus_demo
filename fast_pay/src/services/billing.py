import random
import string
from datetime import datetime

from fastapi import Depends
from sqlalchemy import and_, select

from src import models
from src.database import async_session, get_session
from src.schemas.account import Account
from src.schemas.invoice import Invoice, InvoiceCreate
from src.schemas.service import Service


class BillingService:
    def __init__(self, session: async_session = Depends(get_session)):
        self.session = session

    async def get_service(self, client_id, service_id) -> Service:
        query = select(models.Service).where(
            and_(
                models.Service.client_id == client_id,
                models.Service.service_id == service_id,
            )
        )

        res = await self.session.execute(query)
        service = res.scalar()

        return service

    async def get_account(self, client_id, account_number) -> Account:
        query = select(models.Account).where(
            and_(
                models.Account.client_id == client_id,
                models.Account.account_number == account_number,
            )
        )

        res = await self.session.execute(query)
        account = res.scalar()

        return account

    async def issue_invoice(self, data: InvoiceCreate) -> Invoice:
        service = await self.get_service(data.client_id, data.service_id)

        account = await self.get_account(data.client_id, data.account_number)

        invoice_number_exists = True

        while invoice_number_exists:
            invoice_number_exists = False

            new_invoice_number = "".join(
                random.choice(string.ascii_uppercase + string.digits) for _ in range(6)
            )

            query = select(models.Invoice).where(
                models.Invoice.invoice_number == new_invoice_number
            )

            res = await self.session.execute(query)

            invoice_same_number = res.scalar()

            if invoice_same_number:
                invoice_number_exists = True

        now = datetime.utcnow()

        new_invoice = models.Invoice(
            account_number=account.account_number,
            invoice_number=new_invoice_number,  # noqa
            issued_at=now,
            service_id=service.service_id,
            service_name=service.name,
            amount=service.price,
        )

        self.session.add(new_invoice)
        await self.session.commit()

        return new_invoice
