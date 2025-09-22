from os import getenv

from sqlalchemy.orm import Mapped, sessionmaker, DeclarativeBase, mapped_column
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from dotenv import load_dotenv


load_dotenv()


DB_HOST = getenv("DB_HOST")
DB_PORT = getenv("DB_PORT")
DB_NAME = getenv("DB_NAME")
DB_USER = getenv("DB_USER")
DB_PASSWORD = getenv("DB_PASSWORD")

DATABASE_URL = (
    f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True)


class AsyncDB:
    ENGINE = create_async_engine(DATABASE_URL)
    Session = sessionmaker(bind=ENGINE, class_=AsyncSession)

    @classmethod
    async def up(cls):
        async with cls.ENGINE.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    @classmethod
    async def down(cls):
        async with cls.ENGINE.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)

    @classmethod
    async def rebuild(cls):
        async with cls.ENGINE.begin() as conn:
            await cls.down()
            await cls.up()

    @classmethod
    async def get_session(cls):
        async with cls.Session.begin() as session:
            yield session



from .models import Master, Order, ReferralLink, Service, User