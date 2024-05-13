from pydantic import BaseModel, ConfigDict, EmailStr


class BaseCompany(BaseModel):
    email: EmailStr


class CompanyRegister(BaseCompany):
    name: str
    password: str


class Company(BaseCompany):
    model_config = ConfigDict(from_attributes=True)

    name: str
    client_id: str


class CompanyLogin(BaseCompany):
    password: str


class CompanyCLILogin(BaseModel):
    client_id: str
    client_secret: str
