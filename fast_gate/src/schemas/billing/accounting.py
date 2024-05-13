from pydantic import BaseModel, EmailStr


class AccountingCreate(BaseModel):
    client_id: str
    client_secret: str
    email: EmailStr
    username: str
