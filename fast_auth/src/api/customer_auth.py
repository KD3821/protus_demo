from fastapi import APIRouter, Depends

from src.schemas.customer import Customer, CustomerLogin, CustomerRegister
from src.schemas.token import AccessToken, RefreshToken, Tokens
from src.services.customer_service import CustomerAuthService

router = APIRouter(prefix="/customers", tags=["Customers"])


@router.post("/register/", response_model=Customer)
async def register_customer(
    register_data: CustomerRegister, service: CustomerAuthService = Depends()
):
    """
    Register Customer to get client_id and client_secret
    """
    return await service.register_customer(register_data)


@router.post("/login/", response_model=Tokens)
async def login_customer(
    login_data: CustomerLogin, service: CustomerAuthService = Depends()
):
    """
    Login into Service with Customer email and password
    """
    return await service.login(login_data)


@router.post("/refresh/", response_model=AccessToken)
async def refresh(
    refresh_token: RefreshToken, service: CustomerAuthService = Depends()
):
    """
    Obtain fresh Access Token
    """
    return await service.refresh_token(refresh_token)
