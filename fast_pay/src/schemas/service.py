from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class BaseService(BaseModel):
    client_id: str


class Service(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int


class ServiceInfo(BaseModel):
    service_id: str
    name: str
    price: Decimal
