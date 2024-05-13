from typing import Annotated

import grpc
from fastapi import APIRouter, BackgroundTasks, Depends, Header, Query, status
from fastapi.exceptions import HTTPException

from src.caching import cache_set, get_redis, redis
from src.proto.compiled.auth_pb2 import IntrospectRequest, SessionRequest
from src.proto.compiled.auth_pb2_grpc import AuthProtoStub
from src.proxy import ProxyClient
from src.schemas.auth.token import (AccessToken, TokenIntrospect,
                                    TokenIntrospectResult)
from src.schemas.oauth.session import (LoginSessionRequest,
                                       LoginSessionResponse,
                                       OAuthCustomerLogin, StartedLoginSession)
from src.settings import fast_gate_settings

router = APIRouter(prefix="/oauth", tags=["OAuth"])


@router.post("/session/")
async def login_session(
    data: LoginSessionRequest,
    idempotency_key: Annotated[str, Header()],
    rds_cache: Annotated[redis.Redis, Depends(get_redis)],
    background_tasks: BackgroundTasks,
):
    """
    [gRPC] Запрос на получение авторизационной сессии от PROTUS-django
    [gRPC] GATEWAY >> AUTH_SERVICE
    """
    cached_res = await rds_cache.get(idempotency_key)
    if cached_res:
        return cached_res
    try:
        async with grpc.aio.insecure_channel(
            f"{fast_gate_settings.auth_host}:50051"
        ) as channel:
            auth_stub = AuthProtoStub(channel)
            session_response = await auth_stub.CreateSession(
                SessionRequest(
                    client_id=data.client_id,
                    client_secret=data.client_secret,
                    return_url=data.return_url,
                )
            )
            session_res = LoginSessionResponse(
                expire_date=session_response.expire_date,
                session_id=session_response.session_id,
            )
            background_tasks.add_task(
                cache_set, key=idempotency_key, data=session_res.model_dump_json()
            )
            return session_res
    except grpc.aio.AioRpcError as rpc_error:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=rpc_error.details()
        )  # unexpected 'exception'


@router.post("/introspect/")
async def introspect_token(
    data: AccessToken,
    idempotency_key: Annotated[str, Header()],
    protus_client: Annotated[str, Header()],
    protus_secret: Annotated[str, Header()],
    rds_cache: Annotated[redis.Redis, Depends(get_redis)],
    background_tasks: BackgroundTasks,
):
    """
    [gRPC] Запрос на проверку scope AOuthToken от PROTUS-django
    """
    cached_res = await rds_cache.get(idempotency_key)
    if cached_res:
        return cached_res
    try:
        token_data = TokenIntrospect(
            client_id=protus_client, client_secret=protus_secret, access=data.access
        )
        async with grpc.aio.insecure_channel(
            f"{fast_gate_settings.auth_host}:50051"
        ) as channel:
            auth_stub = AuthProtoStub(channel)
            introspect_response = await auth_stub.IntrospectToken(
                IntrospectRequest(
                    client_id=token_data.client_id,
                    client_secret=token_data.client_secret,
                    token=token_data.access,
                )
            )
            introspect_res = TokenIntrospectResult(
                scope=introspect_response.scope,
                revoked=introspect_response.revoked,
                checked_at=introspect_response.checked_at,
            )
            background_tasks.add_task(
                cache_set,
                key=idempotency_key,
                data=introspect_res.model_dump_json(),
                ex=5,
            )  # 5s
            return introspect_res
    except grpc.aio.AioRpcError as rpc_error:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=rpc_error.details()
        )


@router.get("/session-info/", response_model=StartedLoginSession)
async def login_session_details(
    sid: str = Query(),
    client: ProxyClient = Depends(),
):
    """
    Получение данных компании, запрашивающей сессию авторизации
    """
    return await client.proxy_post_request(
        host=client.AUTH_HOST,
        port=client.AUTH_PORT,
        path="login-session-info",
        data={"session_id": sid},
        user_type="oauth-widget",  # will need js-widget in future
    )


@router.post("/login/")
async def oauth_login(
    data: OAuthCustomerLogin,
    client: ProxyClient = Depends(),
):
    """
    Вход в приложение КОМПАНИИ с логином и паролем для PROTUS
    """
    return await client.proxy_post_request(
        host=client.AUTH_HOST,
        port=client.AUTH_PORT,
        path="login",
        data=data,
        user_type="oauth-widget",  # will need js-widget in future
    )
