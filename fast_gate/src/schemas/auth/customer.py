from pydantic import BaseModel, EmailStr


class BaseCustomer(BaseModel):
    email: EmailStr


class CustomerRegister(BaseCustomer):
    username: str
    password: str


class Customer(BaseCustomer):
    username: str
    customer_uuid: str


class CustomerLogin(BaseCustomer):
    password: str
