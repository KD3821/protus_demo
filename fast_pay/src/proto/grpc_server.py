import asyncio

import grpc

from src.database import async_session
from src.proto.compiled import payments_pb2_grpc
from src.proto.compiled.payments_pb2 import (AccountingRequest, AccountRequest,
                                             AccountResponse, ChargeRequest,
                                             ChargeResponse)
from src.schemas.account import AccountCreate, AccountingCreate
from src.schemas.invoice import InvoiceCreate
from src.services.accounting import AccountService
from src.services.billing import BillingService
from src.settings import fast_pay_settings


class PaymentsProtoService(payments_pb2_grpc.PaymentsProtoServicer):
    async def CreateAccount(
        self, request: AccountRequest, context: grpc.aio.ServicerContext
    ) -> AccountResponse:

        data = {"client_id": request.client_id, "owner": request.owner}

        service = AccountService(session=async_session())

        async with service.session:
            account_data = await service.get_or_create_account(AccountCreate(**data))

        return AccountResponse(account_number=account_data.account_number)

    async def CreateAccounting(
        self, request: AccountingRequest, context: grpc.aio.ServicerContext
    ) -> AccountResponse:

        data = {
            "client_id": request.client_id,
            "email": request.email,
            "username": request.username,
        }

        service = AccountService(session=async_session())

        async with service.session:
            accounting_data = await service.create_customer_accounting(
                AccountingCreate(**data)
            )

        return AccountResponse(account_number=accounting_data.account_number)

    async def ChargeAccount(
        self, request: ChargeRequest, context: grpc.aio.ServicerContext
    ):
        data = {
            "client_id": request.client_id,
            "service_id": request.service_id,
            "account_number": request.account_number,
        }

        service = BillingService(session=async_session())

        async with service.session:
            invoice_data = await service.issue_invoice(InvoiceCreate(**data))

        return ChargeResponse(
            service_id=invoice_data.service_id,
            service_name=invoice_data.service_name,
            account_number=invoice_data.account_number,
            invoice_number=invoice_data.invoice_number,
            issued_at=int(invoice_data.issued_at.timestamp()),
            amount=float(invoice_data.amount),
        )


async def serve() -> None:
    server = grpc.aio.server()
    payments_pb2_grpc.add_PaymentsProtoServicer_to_server(
        PaymentsProtoService(), server
    )
    server.add_insecure_port(
        f"{fast_pay_settings.server_host}:50052"
    )  # change from 50051: taken by auth_grpc_server
    await server.start()
    await server.wait_for_termination()


if __name__ == "__main__":
    asyncio.run(serve())


"""
python3 -m src.proto.grpc_server
"""
