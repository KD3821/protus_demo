import random
import string
from datetime import datetime
from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.orm import joinedload

from src import models
from src.database import async_session
from src.logger import logger
from src.schemas.account import Account
from src.schemas.invoice import Invoice, InvoiceUpdate
from src.schemas.wallet import Wallet, WalletByBroker, WalletCreate
from src.triggers import trigger_webhook


class WalletCallbackHandler:
    def __init__(self):
        self.session = async_session()

    async def get_wallet(self, owner: str) -> Wallet:
        async with self.session:
            query = select(models.Wallet).where(models.Wallet.email == owner)

            res = await self.session.execute(query)

            return res.scalar()

    async def get_account(self, account_number: str) -> Account:
        async with self.session:

            query = (
                select(models.Account)
                .where(models.Account.account_number == account_number)
                .options(joinedload(models.Account.provider))
            )

            res = await self.session.execute(query)

            return res.scalar()

    async def get_invoice(self, invoice_number: str) -> Invoice:
        async with self.session:
            query = select(models.Invoice).where(
                models.Invoice.invoice_number == invoice_number
            )

            res = await self.session.execute(query)

            return res.scalar()

    async def pay_invoice_from_broker(self, invoice_update: dict):
        valid_data = InvoiceUpdate.model_validate(invoice_update)
        invoice_number = valid_data.invoice_number

        invoice = await self.get_invoice(invoice_number)
        account = await self.get_account(invoice.account_number)
        wallet = await self.get_wallet(account.owner)

        new_wallet_balance = wallet.balance - invoice.amount
        new_account_balance = account.balance + invoice.amount

        wallet.balance = new_wallet_balance
        account.balance = new_account_balance

        reference_code = str(invoice.id) + "".join(
            random.choice(string.ascii_uppercase + string.digits) for _ in range(8)
        )
        now = datetime.utcnow()

        async with self.session:
            operation = models.Operation(
                reference_code=reference_code,
                invoice_number=invoice.invoice_number,
                account_number=account.account_number,
                service_id=invoice.service_id,
                date=now,
                amount=invoice.amount,
                remaining_balance=new_wallet_balance,
                payload=valid_data.payload,
            )

            self.session.add_all([operation, wallet, account])
            await self.session.commit()

        res = await trigger_webhook(
            url=account.provider.wh_url,
            data={
                "invoice_number": invoice_number,
                "reference_code": reference_code,
                "finalized_at": int(now.timestamp()),
                "payload": valid_data.payload,
            },
            wh_secret=account.provider.wh_secret,
            user_type="payment-final",
        )

        if res.status_code == 200:
            await self.finalize_invoice(invoice_number, reference_code, now)
            logger.info(
                f"PROTUS-CLI: Invoice finalized * "
                f"[invoice_number: {invoice_number} | ref_code: {reference_code} | finalized_at: {now}]"
            )

    async def finalize_invoice(
        self, invoice_number: str, reference_code: str, finalize_at: datetime
    ):
        invoice = await self.get_invoice(invoice_number)

        async with self.session:
            invoice.finalized_at = finalize_at
            invoice.paas_note = f"PAID: {reference_code}"

            self.session.add(invoice)
            await self.session.commit()

    async def create_from_broker(self, create_data: dict) -> str:
        valid_data = WalletCreate.model_validate(create_data)

        async with self.session:
            query = select(models.Wallet).where(
                models.Wallet.customer_uuid == valid_data.customer_uuid
            )

            res = await self.session.execute(query)

            wallet_exists = res.scalar()

            if wallet_exists:
                exists = WalletByBroker(
                    id=wallet_exists.id,
                    email=wallet_exists.email,
                    customer_uuid=wallet_exists.customer_uuid,
                    balance=wallet_exists.balance,
                )
                return exists.model_dump_json()

            wallet = models.Wallet(
                email=valid_data.email,
                username=valid_data.username,
                customer_uuid=valid_data.customer_uuid,
                debit=Decimal("0.00"),
                credit=Decimal("0.00"),
                balance=Decimal("0.00"),
            )

            self.session.add(wallet)
            await self.session.commit()

            wallet_created = WalletByBroker(
                id=wallet.id,
                email=wallet.email,
                customer_uuid=wallet.customer_uuid,
                balance=wallet.balance,
            )
            return wallet_created.model_dump_json()
