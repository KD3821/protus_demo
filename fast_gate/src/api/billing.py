from typing import Annotated

import grpc
from fastapi import APIRouter, BackgroundTasks, Depends, Header, status
from fastapi.exceptions import HTTPException

from src.broker import broker_handler
from src.caching import cache_set
from src.proto.compiled.payments_pb2 import AccountingRequest, ChargeRequest
from src.proto.compiled.payments_pb2_grpc import PaymentsProtoStub
from src.proxy import ProxyClient
from src.schemas.billing.accounting import AccountingCreate
from src.schemas.billing.payment import PaymentCreate, PaymentCreateResponse
from src.services.auth import CompanyAuthChecker, get_current_user
from src.settings import fast_gate_settings

router = APIRouter(prefix="/billing", tags=["Billing"])

CurrentUser = Annotated[str, Depends(get_current_user)]

company_checker = CompanyAuthChecker()


@router.get("/info/")
async def info(
    user: CurrentUser,
    user_type: Annotated[str, Header()],
    client: ProxyClient = Depends(),
):
    """
    Главный экран - Customer: кошелек + аккаунты в сервисах-партнерах | Company: client_secret + аккаунты пользователей
    GATEWAY >> BILLING_SERVICE
    """
    return await client.proxy_get_request(
        host=client.PAYMENTS_HOST,
        port=client.PAYMENTS_PORT,
        path="info",
        user_type=user_type,
        user=user,
    )


@router.get("/dashboard/")
async def info(
    user: CurrentUser,
    user_type: Annotated[str, Header()],
    client: ProxyClient = Depends(),
):
    """
    Экран дашборда - для Company - набор услуг, для Customer - список операций кошелька
    GATEWAY >> BILLING_SERVICE
    """
    return await client.proxy_get_request(
        host=client.PAYMENTS_HOST,
        port=client.PAYMENTS_PORT,
        path="dashboard",
        user_type=user_type,
        user=user,
    )


@router.post("/new-account/")
async def assign_account(
    data: AccountingCreate,
    idempotency_key: Annotated[str, Header()],
    cached_or_client_id: Annotated[
        str, Depends(company_checker.check_cache_or_credentials)
    ],  # no cache > perform auth
    background_tasks: BackgroundTasks,
):
    """
    [gRPC] Запрос на создание аккаунта для пользователя от PROTUS-django
    [gRPC] GATEWAY >> PAYMENTS_SERVICE
    """
    cached_res, checked_client_id = cached_or_client_id

    if cached_res:
        return cached_res

    async with grpc.aio.insecure_channel(
        f"{fast_gate_settings.payments_host}:50052"
    ) as channel:  # change 50051
        payments_stub = PaymentsProtoStub(channel)
        accounting_response = await payments_stub.CreateAccounting(
            AccountingRequest(
                client_id=checked_client_id, email=data.email, username=data.username
            )
        )
        background_tasks.add_task(
            cache_set, key=idempotency_key, data=accounting_response.account_number
        )
        return accounting_response.account_number


@router.post("/charge/")
async def charge_account(
    data: PaymentCreate,
    idempotency_key: Annotated[str, Header()],
    cached_or_client_id: Annotated[
        str, Depends(company_checker.check_cache_or_credentials)
    ],
    background_tasks: BackgroundTasks,
):
    """
    [gRPC] Запрос на списание средств с кошелька пользователя от PROTUS-django
    [gRPC] GATEWAY >> PAYMENTS_SERVICE
    """
    cached_res, checked_client_id = cached_or_client_id
    if cached_res:
        return cached_res
    try:
        async with grpc.aio.insecure_channel(
            f"{fast_gate_settings.payments_host}:50052"
        ) as channel:  # change 50051
            payments_stub = PaymentsProtoStub(channel)
            charge_response = await payments_stub.ChargeAccount(
                ChargeRequest(
                    client_id=checked_client_id,
                    service_id=data.service_id,
                    account_number=data.user_uuid,
                )
            )
            charge_res = PaymentCreateResponse(
                service_id=charge_response.service_id,
                user_uuid=charge_response.account_number,
                invoice_number=charge_response.invoice_number,
                issued_at=charge_response.issued_at,
                service_name=charge_response.service_name,
                amount=charge_response.amount,
            )

            broker_data = {
                "callback": "Wallet.pay_invoice_from_broker",  # hard coded
                "invoice_number": charge_res.invoice_number,
                "payload": data.payload,
            }

            background_tasks.add_task(
                broker_handler.process_request,
                service_name="payments",
                data=broker_data,
            )
            background_tasks.add_task(
                cache_set,
                key=idempotency_key,
                data=charge_res.model_dump_json(),
                ex=3600,
            )  # 1h

            return charge_res

    except grpc.aio.AioRpcError as rpc_error:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=rpc_error.details()
        )
