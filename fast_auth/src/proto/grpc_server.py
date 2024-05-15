import asyncio

import grpc

from src.database import async_session
from src.proto.compiled import auth_pb2_grpc
from src.proto.compiled.auth_pb2 import (AuthCompanyRequest,
                                         AuthCompanyResponse, CustomerRequest,
                                         CustomerResponse, IntrospectRequest,
                                         IntrospectResponse, SessionRequest,
                                         SessionResponse)
from src.schemas.company import CompanyCLILogin
from src.schemas.customer import PaymentsCustomerRegister
from src.schemas.session import LoginSessionRequest
from src.schemas.token import TokenIntrospect
from src.services.company_service import CompanyAuthService
from src.services.customer_service import CustomerAuthService
from src.services.oauth_service import OAuthService
from src.logger import logger
from src.settings import fast_auth_settings


class AuthProtoService(auth_pb2_grpc.AuthProtoServicer):
    async def AuthenticateCompany(
        self, request: AuthCompanyRequest, context: grpc.aio.ServicerContext
    ) -> AuthCompanyResponse:

        data = {"client_id": request.client_id, "client_secret": request.client_secret}

        service = CompanyAuthService(session=async_session())

        try:
            company = await service.get_authenticated_company(CompanyCLILogin(**data))
        finally:
            await service.session.aclose()

        if company is None:
            await context.abort(
                code=grpc.StatusCode.UNAUTHENTICATED,
                details="Access Denied. Invalid Credentials",  # todo check if 'trailing metadata'
            )

        return AuthCompanyResponse(client_id=company.client_id)

    async def CreateSession(
        self, request: SessionRequest, context: grpc.aio.ServicerContext
    ) -> SessionResponse:
        logger.info(
            f"gRPC Request 'CreateSession' for CLIENT_ID: {request.client_id} | RETURN_URL: {request.return_url}"
        )

        data = {
            "client_id": request.client_id,
            "client_secret": request.client_secret,
            "return_url": request.return_url,
        }

        service = OAuthService(session=async_session())

        try:
            session_data = await service.create_login_session(
                LoginSessionRequest(**data)
            )
        finally:
            await service.session.aclose()

        return SessionResponse(
            expire_date=str(session_data.expire_date),
            session_id=session_data.session_id,
        )

    async def CreateCustomer(
        self, request: CustomerRequest, context: grpc.aio.ServicerContext
    ) -> CustomerResponse:
        data = {"email": request.email, "username": request.username}

        service = CustomerAuthService(session=async_session())

        try:
            customer = await service.register_payments_customer(
                PaymentsCustomerRegister(**data)
            )
        finally:
            await service.session.aclose()

        return CustomerResponse(customer_uuid=customer.customer_uuid)

    async def IntrospectToken(
        self, request: IntrospectRequest, context: grpc.aio.ServicerContext
    ) -> IntrospectResponse:
        data = {
            "client_id": request.client_id,
            "client_secret": request.client_secret,
            "access": request.token,
        }

        service = OAuthService(session=async_session())

        async with service.session:
            introspect_data = await service.introspect_token(TokenIntrospect(**data))

        return IntrospectResponse(
            scope=introspect_data.scope,
            revoked=introspect_data.revoked,
            checked_at=introspect_data.checked_at,
        )


async def serve() -> None:
    server = grpc.aio.server()
    auth_pb2_grpc.add_AuthProtoServicer_to_server(AuthProtoService(), server)
    server.add_insecure_port(f"{fast_auth_settings.server_host}:50051")
    await server.start()
    await server.wait_for_termination()


if __name__ == "__main__":
    asyncio.run(serve())


"""
python3 -m src.proto.grpc_server
"""
