from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)

from .settings import fast_pay_settings

engine = create_async_engine(
    fast_pay_settings.pg_dsn.unicode_string(), future=True, echo=False
)

async_session = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def get_session() -> async_session:
    async with async_session() as session:
        yield session


def create_tables():
    db_engine = create_engine(fast_pay_settings.pg_dsn.unicode_string())
    from .models import Base
    Base.metadata.create_all(db_engine)


create_tables()
