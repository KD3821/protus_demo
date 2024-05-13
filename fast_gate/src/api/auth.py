from typing import Annotated

from fastapi import APIRouter, Depends, Header

from src.proxy import ProxyClient
from src.schemas.auth.company import Company, CompanyLogin, CompanyRegister
from src.schemas.auth.customer import Customer, CustomerLogin, CustomerRegister
from src.schemas.auth.token import AccessToken, RefreshToken, Tokens

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register/", response_model=Company | Customer)
async def register(
    data: CompanyRegister | CustomerRegister,
    user_type: Annotated[str, Header()],
    client: ProxyClient = Depends(),
):
    """
    Регистрация пользователя как ФИЗ.ЛИЦО или КОМПАНИЯ
    GATEWAY >> AUTH_SERVICE
    ( + для КОМПАНИИ: broker[регистрация PROVIDER] --> BILLING_SERVICE )
    """
    return await client.proxy_post_request(
        host=client.AUTH_HOST,
        port=client.AUTH_PORT,
        path="register",
        data=data,
        user_type=user_type,
    )


@router.post("/login/", response_model=Tokens)
async def login(
    data: CompanyLogin | CustomerLogin,
    user_type: Annotated[str, Header()],
    client: ProxyClient = Depends(),
):
    """
    Вход в личный кабинет как ФИЗ.ЛИЦО или КОМПАНИЯ.
    GATEWAY >> AUTH_SERVICE
    """
    return await client.proxy_post_request(
        host=client.AUTH_HOST,
        port=client.AUTH_PORT,
        path="login",
        data=data,
        user_type=user_type,
    )


@router.post("/refresh/", response_model=AccessToken)
async def login(
    data: RefreshToken,
    user_type: Annotated[str, Header()],
    client: ProxyClient = Depends(),
):
    """
    Обновление AccessToken.
    GATEWAY >> AUTH_SERVICE
    """
    return await client.proxy_post_request(
        host=client.AUTH_HOST,
        port=client.AUTH_PORT,
        path="refresh",
        data=data,
        user_type=user_type,
    )
