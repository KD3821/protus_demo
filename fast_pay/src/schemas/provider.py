from pydantic import BaseModel, EmailStr


class BaseProvider(BaseModel):
    client_id: str


class ProviderCreate(BaseProvider):
    email: EmailStr
    name: str
    client_secret: str
    wh_secret: str


class ProviderInfo(BaseProvider):
    name: str
    client_secret: str


class ProviderByBroker(BaseModel):
    id: int
    email: EmailStr
    name: str
