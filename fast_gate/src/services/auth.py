from typing import Annotated

import grpc
from fastapi import Depends, Header, status
from fastapi.exceptions import HTTPException
from jose import JWTError, jwt

from src.caching import get_redis, redis
from src.proto.compiled.auth_pb2 import AuthCompanyRequest
from src.proto.compiled.auth_pb2_grpc import AuthProtoStub
from src.settings import fast_gate_settings


def custom_auth_scheme(authorization: Annotated[str, Header()]) -> str:
    token_exception = HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Access Denied",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if not authorization:
        raise token_exception
    scheme, token = authorization.split(" ")
    if scheme != "Bearer" or not token:
        raise token_exception
    return token


def get_current_user(token: Annotated[str, Depends(custom_auth_scheme)]) -> str:
    return AuthService.validate_token(token=token)


async def get_cached_response(
    idempotency_key: Annotated[str, Header()],
    rds_cache: Annotated[redis.Redis, Depends(get_redis)],
):
    return await rds_cache.get(idempotency_key)


class AuthService:
    @staticmethod
    async def validate_company_credentials(client_id: str, client_secret: str):
        try:
            async with grpc.aio.insecure_channel(
                f"{fast_gate_settings.auth_host}:50051"
            ) as channel:
                auth_stub = AuthProtoStub(channel)
                auth_company_response = await auth_stub.AuthenticateCompany(
                    AuthCompanyRequest(client_id=client_id, client_secret=client_secret)
                )
                return auth_company_response.client_id
        except grpc.aio.AioRpcError as grp_error:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail=grp_error.details()
            )

    @classmethod
    def validate_token(cls, token: str) -> str:
        token_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(
                token,
                fast_gate_settings.jwt_secret,
                algorithms=[fast_gate_settings.jwt_algorithm],
            )
        except JWTError:
            raise token_exception

        subject_id_data = payload.get("sub")

        return subject_id_data


class CompanyAuthChecker:
    """
    Dependency Injection для авторизации запросов к API Gateway по данным заголовков Protus-Client, Protus-Secret
    Отправляет [gRPC] запрос к AUTH сервису если нет кэшированного ответа для запроса с данным ключом идемпотентности
    """

    def __init__(self, service=AuthService):
        self.service = service

    async def check_cache_or_credentials(
        self,
        protus_client: Annotated[str, Header()],
        protus_secret: Annotated[str, Header()],
        cached_res: Annotated[str, Depends(get_cached_response)],
    ):
        client_id = None
        if cached_res is None:
            client_id = await self.service.validate_company_credentials(
                client_id=protus_client, client_secret=protus_secret
            )
        return cached_res, client_id
