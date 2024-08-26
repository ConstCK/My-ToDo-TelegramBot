import datetime

from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery


from database.crud import add_task, change_status
from scheduler.handlers import task_reminder
from keyboards.keyboards import base_keyboard, tasks_keyboard
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
             f'Введите задачу и описание через знак "-"', parse_mode=ParseMode.HTML
    )
    await callback.answer(text='Выполнение запроса...')
    await state.update_data(category_name=callback.data.split('_')[1])
    await state.set_state(TaskStages.add_task)


# Обработка очереди сообщений (добавление задачи)
@router.message(F.text, StateFilter(TaskStages.add_task))
async def create_task(message: Message, state: FSMContext):
    task_data = validate_task(message.text)
    if task_data:
        data_storage = await state.get_data()
        task = await add_task(category_name=data_storage['category_name'],
                              user_id=message.from_user.id,
                              name=task_data[0],
                              description=task_data[1])

        await message.answer(text=f'Добавлена задача {task.name} в {task.created_at}',
                             reply_markup=await base_keyboard())

        # args= аргумент передаваемый в функцию-обработчик запланированной задачи func=
        scheduler.add_job(func=task_reminder,
                          name='expired_tasks',
                          trigger='date',
                          run_date=task.expire_at - datetime.timedelta(minutes=10),
                          args=(message, task.id))
    else:
        await message.answer(text='Ошибка при вводе задачи',
                             reply_markup=await base_keyboard())
    await state.clear()


# Обработка запроса на завершение задач
@router.callback_query(F.data.startswith('complete'))
async def select_tasks_for_complete(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.answer(text=f'Выбрана категория <b>{callback.data.split('_')[1]}</b>\n'
                                       f'Выберите задачу для завершения...',
                                  reply_markup=await tasks_keyboard(callback.data.split('_')[1]),
                                  parse_mode=ParseMode.HTML)
    await callback.answer(text='Выполнение запроса...')
    await state.update_data(mode='complete')
    await state.set_state(TaskStages.complete_task)


# Обработка запроса на отмену задач
@router.callback_query(F.data.startswith('cancel'))
async def select_tasks_for_complete(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.answer(text=f'Выбрана категория <b>{callback.data.split('_')[1]}</b>\n'
                                       f'Выберите задачу для отмены...',
                                  reply_markup=await tasks_keyboard(callback.data.split('_')[1]),
                                  parse_mode=ParseMode.HTML)
    await callback.answer(text='Выполнение запроса...')
    await state.update_data(mode='cancel')
    await state.set_state(TaskStages.complete_task)


# Обработка очереди сообщений (завершение задачи)
@router.callback_query(StateFilter(TaskStages.complete_task))
async def create_task(callback: CallbackQuery, state: FSMContext):
    data_storage = await state.get_data()
    result = await change_status(callback.data.split('_')[1], data_storage['mode'])
    await callback.answer(text='Выполнение запроса...')
    if result:
        await callback.message.answer(text='Задача успешно завершена')
    else:
        await callback.message.answer(text='Не удалось завершить задачу.\n'
                                           'Попробуйте еще раз')
    await state.clear()


# Обработка запроса на отмену задач
@router.callback_query(F.data.startswith('cancel'), StateFilter(None))
async def select_tasks_for_complete(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text=f'Выбрана категория <b>{callback.data.split('_')[1]}</b>\n'
                                       f'Выберите задачу для отмены...',
                                  reply_markup=await tasks_keyboard(callback.data.split('_')[1]),
                                  parse_mode=ParseMode.HTML)
    await callback.answer(text='Выполнение запроса...')
    await state.update_data(mode='cancel')
    await state.set_state(TaskStages.complete_task)
