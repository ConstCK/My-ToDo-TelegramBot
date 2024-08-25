from aiogram import Router, F
from aiogram.types import Message


from keyboards.keyboards import category_keyboard


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



