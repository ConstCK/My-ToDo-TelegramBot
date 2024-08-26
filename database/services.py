from sqlalchemy import select, and_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql.functions import count

from database.config import engine, Base, async_session
from database.models import Category, Task


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


# Получение id категории по ее названию
async def get_category_id(category_name: str):
    async with async_session() as session:
        result = await session.scalar(select(Category).where(Category.name == category_name))
        return result.id


# Получение количества выполняемых заданий в указанной категории
async def get_tasks_number(category_name: str, tg_id: int) -> int:
    category_id = await get_category_id(category_name)
    async with async_session() as session:
        result = await session.execute(
            select(count(Task.id)).select_from(Task).where(and_(Task.category_id == category_id,
                                                                Task.user_id == tg_id)))

        return result.scalar()
