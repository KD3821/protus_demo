from datetime import datetime
from typing import List

from pydantic import BaseModel, EmailStr


class OAuthToken(BaseModel):
    access: str


class LoginSessionRequest(BaseModel):
    client_id: str
    client_secret: str
    return_url: str


class LoginSessionResponse(BaseModel):
    expire_date: datetime
    session_id: str


class LoginSessionID(BaseModel):
    session_id: str


class OAuthCustomerLogin(BaseModel):
    email: EmailStr
    password: str
    session_id: str
    scope: List[str]


class StartedLoginSession(BaseModel):
    company_name: str
    return_url: str


class CompletedLoginSession(BaseModel):
    return_url: str
