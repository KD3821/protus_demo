import sqlalchemy as sa
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Provider(Base):
    __tablename__ = "providers"

    id = sa.Column(sa.Integer, primary_key=True)
    email = sa.Column(sa.String, unique=True)
    name = sa.Column(sa.String)
    client_id = sa.Column(sa.String, unique=True)
    client_secret = sa.Column(sa.String)
    wh_secret = sa.Column(sa.String)
    wh_url = sa.Column(sa.String, nullable=True)

    accounts = relationship("Account", back_populates="provider")
    services = relationship("Service", back_populates="provider")


class Wallet(Base):
    __tablename__ = "wallets"

    id = sa.Column(sa.Integer, primary_key=True)
    email = sa.Column(sa.String, unique=True)
    username = sa.Column(sa.String)
    customer_uuid = sa.Column(sa.String, unique=True)
    debit = sa.Column(sa.Numeric(10, 2))
    credit = sa.Column(sa.Numeric(10, 2))
    balance = sa.Column(sa.Numeric(10, 2))

    accounts = relationship("Account", back_populates="wallet")


class Account(Base):
    __tablename__ = "accounts"

    id = sa.Column(sa.Integer, primary_key=True)
    account_number = sa.Column(sa.String, unique=True)
    client_id = sa.Column(sa.String, sa.ForeignKey("providers.client_id"))
    owner = sa.Column(sa.String, sa.ForeignKey("wallets.email"))
    registered_at = sa.Column(sa.DateTime)
    debit = sa.Column(sa.Numeric(10, 2))
    credit = sa.Column(sa.Numeric(10, 2))
    balance = sa.Column(sa.Numeric(10, 2))

    wallet = relationship("Wallet", back_populates="accounts")
    provider = relationship("Provider", back_populates="accounts")
    invoices = relationship("Invoice", back_populates="account")
    operations = relationship("Operation", back_populates="account")


class Service(Base):
    __tablename__ = "services"

    id = sa.Column(sa.Integer, primary_key=True)
    service_id = sa.Column(sa.String, unique=True)
    client_id = sa.Column(sa.String, sa.ForeignKey("providers.client_id"))
    name = sa.Column(sa.String)
    is_recurrent = sa.Column(sa.Boolean, default=False)
    recurring_interval = sa.Column(sa.Integer, nullable=True)
    price = sa.Column(sa.Numeric(8, 2))

    provider = relationship("Provider", back_populates="services")
    invoices = relationship("Invoice", back_populates="service")
    operations = relationship("Operation", back_populates="service")


class Invoice(Base):
    __tablename__ = "invoices"

    id = sa.Column(sa.Integer, primary_key=True)
    invoice_number = sa.Column(sa.String, unique=True)
    account_number = sa.Column(sa.String, sa.ForeignKey("accounts.account_number"))
    service_id = sa.Column(sa.String, sa.ForeignKey("services.service_id"))
    service_name = sa.Column(sa.String)
    amount = sa.Column(sa.Numeric(8, 2))
    issued_at = sa.Column(sa.DateTime)
    finalized_at = sa.Column(sa.DateTime, nullable=True)
    paas_note = sa.Column(sa.String, nullable=True)

    account = relationship("Account", back_populates="invoices")
    service = relationship("Service", back_populates="invoices")


class Operation(Base):
    __tablename__ = "operations"

    id = sa.Column(sa.Integer, primary_key=True)
    reference_code = sa.Column(sa.String, unique=True)
    account_number = sa.Column(sa.String, sa.ForeignKey("accounts.account_number"))
    service_id = sa.Column(sa.String, sa.ForeignKey("services.service_id"))
    invoice_number = sa.Column(sa.String, unique=True)
    date = sa.Column(sa.DateTime)
    amount = sa.Column(sa.Numeric(8, 2))
    remaining_balance = sa.Column(sa.Numeric(10, 2))
    payload = sa.Column(sa.JSON, nullable=True)

    account = relationship("Account", back_populates="operations")
    service = relationship("Service", back_populates="operations")
