import grpc

from src.proto.compiled.auth_pb2 import CustomerRequest
from src.proto.compiled.auth_pb2_grpc import AuthProtoStub
from src.settings import fast_pay_settings


async def get_customer_uuid(email, username) -> str:
    async with grpc.aio.insecure_channel(
        f"{fast_pay_settings.auth_host}:50051"
    ) as channel:
        auth_stub = AuthProtoStub(channel)
        customer_response = await auth_stub.CreateCustomer(
            CustomerRequest(email=email, username=username)
        )
        return customer_response.customer_uuid
