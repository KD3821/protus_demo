from pydantic import BaseModel, ConfigDict, EmailStr


class BaseCustomer(BaseModel):
    email: EmailStr


class CustomerRegister(BaseCustomer):
    username: str
    password: str


class Customer(BaseCustomer):
    model_config = ConfigDict(from_attributes=True)

    username: str
    customer_uuid: str


class CustomerLogin(BaseCustomer):
    password: str


class PaymentsCustomerRegister(BaseCustomer):
    username: str
