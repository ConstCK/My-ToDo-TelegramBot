import datetime

from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from database.crud import add_task, change_status
from database.services import get_tasks_number

from keyboards.keyboards import base_keyboard, tasks_keyboard
from scheduler.handlers import task_reminder

from scheduler.scheduler import scheduler
from states.states import TaskStages
from utils.utils import validate_task

router = Router()


# Обработка очереди сообщений (ввод задачи)
@router.callback_query(F.data.startswith('add'))
async def select_task_category(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.answer(
        text=f'Выбрана категория <b>{callback.data.split('_')[1]}</b> для добавления задачи\n'
             f'Введите название задачи и описание через знак "-"'
        , parse_mode=ParseMode.HTML,
    )
    await callback.answer(text='Выполнение запроса...')
    await state.update_data(category_name=callback.data.split('_')[1])
    await state.set_state(TaskStages.adding_task)


# Обработка очереди сообщений (добавление задачи)
@router.message(F.text, StateFilter(TaskStages.adding_task))
async def create_task(message: Message, state: FSMContext):
    task_data = validate_task(message.text)
    if task_data:
        data_storage = await state.get_data()
        task = await add_task(category_name=data_storage['category_name'],
                              user_id=message.from_user.id,
                              name=task_data[0],
                              description=task_data[1])

        await message.answer(text=f'Добавлена задача {task.name} в {task.created_at.strftime('%d-%m-%Y %H:%M')}',
                             reply_markup=await base_keyboard())

        # args= аргумент передаваемый в функцию-обработчик запланированной задачи func=
        if task.expire_at:
            scheduler.add_job(func=task_reminder,
                              kwargs=({
                                  'task_id': task.id,
                                  'message': message
                              }),
                              name='expired_tasks',
                              trigger='date',
                              run_date=task.expire_at - datetime.timedelta(minutes=10),
                              )
            scheduler.print_jobs()
    else:
        await message.answer(text='Ошибка при вводе задачи',
                             reply_markup=await base_keyboard())


# Обработка запроса на завершение задач
@router.callback_query(F.data.startswith('complete'))
async def select_tasks_for_complete(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    task_number = await get_tasks_number(callback.data.split('_')[1], callback.from_user.id)
    if task_number:
        await callback.message.answer(text=f'Выбрана категория <b>{callback.data.split('_')[1]}</b>\n'
                                           f'Выберите задачу для завершения...',
                                      reply_markup=await tasks_keyboard(callback.from_user.id,
                                                                        callback.data.split('_')[1]),
                                      parse_mode=ParseMode.HTML)
        await callback.answer(text='Выполнение запроса...')
        await state.update_data(mode='complete')
        await state.set_state(TaskStages.completing_task)
    else:
        await callback.message.answer(
            text=f'В категории <b>{callback.data.split('_')[1]}</b> нет задач для завершения.',
            parse_mode=ParseMode.HTML)
        await callback.answer(text='Выполнение запроса...')


# Обработка запроса на отмену задач
@router.callback_query(F.data.startswith('cancel'))
async def select_tasks_for_complete(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    task_number = await get_tasks_number(callback.data.split('_')[1], callback.from_user.id)
    if task_number:
        await callback.message.answer(text=f'Выбрана категория <b>{callback.data.split('_')[1]}</b>\n'
                                           f'Выберите задачу для отмены...',
                                      reply_markup=await tasks_keyboard(callback.from_user.id,
                                                                        callback.data.split('_')[1]),
                                      parse_mode=ParseMode.HTML)
        await callback.answer(text='Выполнение запроса...')
        await state.update_data(mode='cancel')
        await state.set_state(TaskStages.completing_task)
    else:
        await callback.message.answer(
            text=f'В категории <b>{callback.data.split('_')[1]}</b> нет задач для отмены.',
            parse_mode=ParseMode.HTML)
        await callback.answer(text='Выполнение запроса...')


# Обработка очереди сообщений (завершение задачи)
@router.callback_query(StateFilter(TaskStages.completing_task))
async def create_task(callback: CallbackQuery, state: FSMContext):
    data_storage = await state.get_data()
    if data_storage['mode'] == 'complete':
        success_text = 'завершена'
        fail_text = 'завершить'
    else:
        success_text = 'отменена'
        fail_text = 'отменить'

    result = await change_status(callback.data.split('_')[1], data_storage['mode'])
    await callback.answer(text='Выполнение запроса...')
    if result:
        await callback.message.answer(text=f'Задача успешно {success_text}')
    else:
        await callback.message.answer(text=f'Не удалось {fail_text} задачу.\n'
                                           f'Попробуйте еще раз')
