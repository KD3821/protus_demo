import grpc

from src.proto.compiled.payments_pb2 import AccountRequest
from src.proto.compiled.payments_pb2_grpc import PaymentsProtoStub
from src.settings import fast_auth_settings


async def get_account_number(client_id, email) -> str:
    async with grpc.aio.insecure_channel(
        f"{fast_auth_settings.payments_host}:50052"
    ) as channel:  # changed from 50051
        payments_stub = PaymentsProtoStub(channel)
        account_response = await payments_stub.CreateAccount(
            AccountRequest(client_id=client_id, owner=email)
        )
        return account_response.account_number
