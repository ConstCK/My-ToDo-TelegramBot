from aiogram import Router, F
from aiogram.types import Message


from keyboards.keyboards import category_keyboard
from database.crud import clean_garbage, delete_canceled_tasks

router = Router()


# Обработка сообщений просмотра задач
@router.message(F.text.startswith('Посмотреть'))
async def cmd_start(message: Message):
    await message.answer(text='Выберите категорию для просмотра задач',
                         reply_markup=await category_keyboard('watch'))


# Обработка сообщений добавления задач
@router.message(F.text.startswith('Добавить'))
async def cmd_start(message: Message):
    await message.answer(text='Выберите категорию для добавления задач',
                         reply_markup=await category_keyboard('add'))


# Обработка сообщений выполнения задач
@router.message(F.text.startswith('Завершить'))
async def cmd_start(message: Message):
    await message.answer(text='Выберите категорию для завершения задач',
                         reply_markup=await category_keyboard('complete'))


# Обработка сообщений отмены задач
@router.message(F.text.startswith('Отменить'))
async def cmd_start(message: Message):
    await message.answer(text='Выберите категорию для отмены задач',
                         reply_markup=await category_keyboard('cancel'))


# Обработка сообщений удаления отмененных задач
@router.message(F.text.startswith('Удалить'))
async def cmd_start(message: Message):
    await message.answer(text='Очистка приложения от отмененных задач...')
    await delete_canceled_tasks()
    await message.answer(text='Очистка прошла успешно...')


# Обработка сообщений удаления завершенных и отмененных задач
@router.message(F.text.startswith('Очистить'))
async def cmd_start(message: Message):
    await message.answer(text='Очистка приложения от отмененных и выполненных задач...')
    await clean_garbage()
    await message.answer(text='Очистка прошла успешно...')
