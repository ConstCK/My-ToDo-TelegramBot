from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase

from config import settings

# Создание движка для связи с БД
engine = create_async_engine(url=settings.db_url, future=True, echo=False)

# Создание асинхронной сессии
async_session = async_sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=False)


# Родительский класс для создания таблиц
class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True
