from fastapi import APIRouter, Depends

from src.schemas.company import Company, CompanyLogin, CompanyRegister
from src.schemas.token import AccessToken, RefreshToken, Tokens
from src.services.company_service import CompanyAuthService

router = APIRouter(prefix="/companies", tags=["Companies"])


@router.post("/register/", response_model=Company)
async def create_company(
    register_data: CompanyRegister, service: CompanyAuthService = Depends()
):
    """
    Register Company to get client_id and client_secret
    """
    return await service.register_company(register_data)


@router.post("/login/", response_model=Tokens)
async def login_company(
    login_data: CompanyLogin, service: CompanyAuthService = Depends()
):
    """
    Login into Service with company email and password
    """
    return await service.login(login_data)


@router.post("/refresh/", response_model=AccessToken)
async def refresh(refresh_token: RefreshToken, service: CompanyAuthService = Depends()):
    """
    Obtain fresh Access Token
    """
    return await service.refresh_token(refresh_token)
