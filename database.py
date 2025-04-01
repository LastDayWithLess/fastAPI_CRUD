from sqlalchemy import create_engine, URL
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from config import settings
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs

async_engine = create_async_engine(
    url=settings.DATABASE_url_psycopg,
    echo=False,
    pool_size=5,
    max_overflow=10)

class Base(AsyncAttrs, DeclarativeBase):
    pass

async_session = async_sessionmaker(async_engine)

async def get_db():
    async with async_session() as session:
        yield session 