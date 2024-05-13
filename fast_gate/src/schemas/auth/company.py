from pydantic import BaseModel, EmailStr


class BaseCompany(BaseModel):
    email: EmailStr


class CompanyRegister(BaseCompany):
    name: str
    password: str


class Company(BaseCompany):
    name: str
    client_id: str


class CompanyLogin(BaseCompany):
    password: str
