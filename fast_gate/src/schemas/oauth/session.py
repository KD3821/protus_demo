from datetime import datetime
from typing import List

from pydantic import BaseModel, EmailStr


class OAuthTokens(BaseModel):
    access: str
    refresh: str


class LoginSessionRequest(BaseModel):
    client_id: str
    client_secret: str
    return_url: str


class LoginSessionResponse(BaseModel):
    expire_date: datetime
    session_id: str


class StartedLoginSession(BaseModel):
    company_name: str
    return_url: str


class OAuthCustomerLogin(BaseModel):
    email: EmailStr
    password: str
    session_id: str
    scope: List[str]
