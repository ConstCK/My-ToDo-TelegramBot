from sqlalchemy.exc import IntegrityError

from database.config import engine, Base, async_session
from database.models import Category


# Создание всех таблиц в БД
async def create_tables():
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)


# Добавление базовых категорий в БД
async def add_initial_categories():
    async with async_session() as session:
        try:
            categories = [Category(name='Ежедневные'),
                          Category(name='На неделю'),
                          Category(name='На месяц'),
                          Category(name='На год'),
                          Category(name='Важные!'),
                          Category(name='Все')]
            session.add_all(categories)
            await session.commit()
        except IntegrityError:
            print(f'Categories are already exist...')
