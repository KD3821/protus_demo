import sqlalchemy as sa
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Company(Base):
    __tablename__ = "companies"

    id = sa.Column(sa.Integer, primary_key=True)
    email = sa.Column(sa.String, unique=True)
    name = sa.Column(sa.String, unique=True)
    hashed_password = sa.Column(sa.String)
    client_id = sa.Column(sa.String, unique=True)
    client_secret = sa.Column(sa.String)
    wh_secret = sa.Column(sa.String)
    wh_url = sa.Column(sa.String, nullable=True)

    tokens = relationship("OAuthToken", back_populates="company")
    login_sessions = relationship("LoginSession", back_populates="company")


class Customer(Base):
    __tablename__ = "customers"

    id = sa.Column(sa.Integer, primary_key=True)
    email = sa.Column(sa.String, unique=True)
    username = sa.Column(sa.String)
    hashed_password = sa.Column(sa.String)
    customer_uuid = sa.Column(sa.String)
    is_verified = sa.Column(sa.Boolean, default=True)

    tokens = relationship("OAuthToken", back_populates="customer")


class OAuthToken(Base):
    __tablename__ = "tokens"

    id = sa.Column(sa.Integer, primary_key=True)
    client_id = sa.Column(sa.String, sa.ForeignKey("companies.client_id"))
    email = sa.Column(sa.String, sa.ForeignKey("customers.email"))
    refresh = sa.Column(sa.Boolean, default=False)
    scope = sa.Column(sa.String, nullable=True)
    token = sa.Column(sa.String)
    expire_date = sa.Column(sa.DateTime)
    revoke_date = sa.Column(sa.DateTime, nullable=True)
    revoked = sa.Column(sa.Boolean, default=False)

    customer = relationship("Customer", back_populates="tokens")
    company = relationship("Company", back_populates="tokens")


class LoginSession(Base):
    __tablename__ = "login_sessions"

    id = sa.Column(sa.Integer, primary_key=True)
    client_id = sa.Column(sa.String, sa.ForeignKey("companies.client_id"))
    email = sa.Column(sa.String, nullable=True)
    expire_date = sa.Column(sa.DateTime)
    finalized_at = sa.Column(sa.DateTime, nullable=True)
    session_id = sa.Column(sa.String, unique=True)
    confirmation_id = sa.Column(sa.String, nullable=True)
    return_url = sa.Column(sa.String)

    company = relationship("Company", back_populates="login_sessions")
