import datetime

from sqlalchemy import select, update, delete, and_
from sqlalchemy.orm import joinedload

from database.config import async_session
from database.models import Category, Task, User
from utils.utils import get_time_period


# Добавление пользователя в БД
async def set_user(tg_id: int) -> None:
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            session.add(User(tg_id=tg_id))
            print('User is added to db...')
            await session.commit()


# Получение id категории по ее названию
async def get_category_id(category_name: str):
    async with async_session() as session:
        result = await session.scalar(select(Category).where(Category.name == category_name))
        print(result)
        return result.id


# Получение списка всех категорий
async def get_all_categories() -> list[Category]:
    async with async_session() as session:
        result = await session.scalars(select(Category))
        return result.all()


# Получение списка всех задач в указанной категории
async def get_all_tasks(category_name: str) -> list[Task]:
    async with async_session() as session:
        if category_name == 'Все':
            result = await session.scalars(select(Task)
                                           .order_by(Task.expire_at)
                                           .options(joinedload(Task.category))
                                           )
        else:
            category_id = await get_category_id(category_name)
            result = await session.scalars(select(Task)
                                           .where(Task.category_id == category_id)
                                           .order_by(Task.expire_at)
                                           .options(joinedload(Task.category))
                                           )

        return result.all()


# Получение списка всех выполняемых задач в указанной категории
async def get_all_current_tasks(category_name: str) -> list[Task]:
    async with async_session() as session:
        if category_name == 'Все':
            result = await session.scalars(select(Task)
                                           .where(Task.status == 'Выполняется')
                                           .order_by(Task.expire_at)
                                           .options(joinedload(Task.category))
                                           )
        else:
            category_id = await get_category_id(category_name)
            result = await session.scalars(select(Task)
                                           .where(and_(Task.category_id == category_id,
                                                       Task.status == 'Выполняется'))
                                           .order_by(Task.expire_at)
                                           .options(joinedload(Task.category))
                                           )
        return result.all()


# Добавление задачи в БД
async def add_task(user_id: int, category_name: str, name: str, description: str) -> Task:
    category_id = await get_category_id(category_name)
    time_period = get_time_period(category_name)
    expire_date = datetime.datetime.now() + time_period if time_period else None
    task = Task(name=name,
                description=description,
                category_id=category_id,
                user_id=user_id,
                expire_at=expire_date)
    async with async_session() as session:
        session.add(task)
        await session.commit()

        return task


# Смена статуса задачи
async def change_status(task_id: str, mode: str) -> bool:
    if mode == 'complete':
        task_status = 'Выполнено'
    elif mode == 'cancel':
        task_status = 'Снято'
    else:
        return False
    async with async_session() as session:
        try:
            await session.execute(update(Task)
                                  .where(Task.id == task_id)
                                  .values(status=task_status))
            await session.commit()
            return True
        except Exception as err:
            print(f'error {err}')
            await session.rollback()


# Удаление указанных задач
async def delete_tasks() -> None:
    async with async_session() as session:
        result = await session.execute(delete(Task)
                                       .where(Task.status == 'Снято'))
        print('result------', result)
        await session.commit()
