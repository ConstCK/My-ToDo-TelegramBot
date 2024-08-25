from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext

from aiogram.types import CallbackQuery
from database.crud import get_all_tasks
from utils.utils import get_status_mark

router = Router()


# Обработка запроса на просмотр всех задач
@router.callback_query(F.data.startswith('watch'))
async def show_tasks(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.answer(text=f'Выбрана категория <b>{callback.data.split('_')[1]}</b>.',
                                  parse_mode=ParseMode.HTML)
    await callback.answer(text='Выполнение запроса...')
    tasks = await get_all_tasks(callback.data.split('_')[1])
    if tasks:
        for i, task in enumerate(tasks):
            expire_date = 'не указано' if not task.expire_at else task.expire_at.strftime('%d-%m-%Y')
            status_mark = get_status_mark(task.status)
            await callback.message.answer(
                text=f'{status_mark} Задача № {i + 1}: <b><u>{task.name}</u></b> из категории <b>{task.category.name}</b>\n'
                     f'Подробности: {task.description}.\n'
                     f'Статус:<b>{task.status}</b>, активно до <b>{expire_date}</b>.',
                parse_mode=ParseMode.HTML
            )
    else:
        await callback.message.answer(text='Пока нет задач в данной категории...')



