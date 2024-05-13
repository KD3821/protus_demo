from fastapi import APIRouter, Depends

from src.schemas.session import (CompletedLoginSession, LoginSessionID,
                                 OAuthCustomerLogin, StartedLoginSession)
from src.services.oauth_service import OAuthService

router = APIRouter(prefix="/oauth-widget", tags=["Commands"])


@router.post("/login-session-info/", response_model=StartedLoginSession)
async def start_oauth_session(
    session_data: LoginSessionID, service: OAuthService = Depends()
):
    """
    Инициализация Аутентификационной сессии для Пользователя
    """
    return await service.start_oauth_session(session_data)


@router.post("/login/", response_model=CompletedLoginSession)
async def login_oauth_user(
    login_data: OAuthCustomerLogin, service: OAuthService = Depends()
):
    """
    Финализация Аутентификационной сессии для пользователя
    """
    return await service.finalize_oauth_session(login_data)
