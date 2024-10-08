import datetime

from sqlalchemy import select, update, delete, and_, or_
from sqlalchemy.orm import joinedload

from database.config import async_session
from database.models import Category, Task, User
from database.services import get_category_id
from utils.utils import get_time_period


# Добавление пользователя в БД
async def set_user(tg_id: int) -> None:
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        if not user:
            session.add(User(tg_id=tg_id))
            print('User is added to db...')
            await session.commit()


# Получение списка всех категорий
async def get_all_categories() -> list[Category]:
    async with async_session() as session:
        result = await session.scalars(select(Category))
        return result.all()


# Получение списка всех задач в указанной категории
async def get_all_tasks(tg_id: int, category_name: str) -> list[Task]:
    async with async_session() as session:
        if category_name == 'Все':
            result = await session.scalars(select(Task)
                                           .where(Task.user_id == tg_id)
                                           .order_by(Task.expire_at)
                                           .options(joinedload(Task.category))
                                           )
        else:
            category_id = await get_category_id(category_name)
            result = await session.scalars(select(Task)
                                           .where(and_(Task.category_id == category_id,
                                                       Task.user_id == tg_id))
                                           .order_by(Task.expire_at)
                                           .options(joinedload(Task.category))
                                           )
        return result.all()


# Получение списка всех выполняемых задач в указанной категории
async def get_all_current_tasks(tg_id: int, category_name: str) -> list[Task]:
    async with async_session() as session:
        if category_name == 'Все':
            result = await session.scalars(select(Task)
                                           .where(and_(Task.status == 'Выполняется',
                                                       Task.user_id == tg_id))
                                           .order_by(Task.expire_at)
                                           .options(joinedload(Task.category))
                                           )
        else:
            category_id = await get_category_id(category_name)
            result = await session.scalars(select(Task)
                                           .where(and_(Task.category_id == category_id,
                                                       Task.status == 'Выполняется',
                                                       Task.user_id == tg_id))
                                           .order_by(Task.expire_at)
                                           .options(joinedload(Task.category))
                                           )
        return result.all()


# Получение задачи по указанному id
async def get_task(task_id: int) -> Task:
    async with async_session() as session:
        result = await session.scalar(select(Task)
                                      .where(Task.id == task_id)
                                      )
    return result


# Добавление задачи в БД
async def add_task(user_id: int, category_name: str, name: str, description: str) -> Task:
    category_id = await get_category_id(category_name)
    time_period = get_time_period(category_name)
    current_time = datetime.datetime.now()
    expire_date = datetime.datetime.now() + time_period if time_period else None
    task = Task(name=name,
                description=description,
                category_id=category_id,
                user_id=user_id,
                created_at=current_time,
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


# Удаление отмененных задач
async def delete_canceled_tasks() -> None:
    async with async_session() as session:
        await session.execute(delete(Task)
                              .where(Task.status == 'Снято'))
        await session.commit()


# Удаление неактивных задач
async def clean_garbage() -> None:
    async with async_session() as session:
        await session.execute(delete(Task)
                              .where(or_(Task.status == 'Снято',
                                         Task.status == 'Выполнено')))
        await session.commit()
