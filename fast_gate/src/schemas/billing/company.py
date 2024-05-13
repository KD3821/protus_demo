from pydantic import BaseModel


class ProviderInfo(BaseModel):
    name: str
    client_id: str
    client_secret: str
