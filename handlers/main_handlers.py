from aiogram import Router
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

from database.crud import set_user
from keyboards.keyboards import base_keyboard

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await set_user(message.from_user.id)
    await message.answer(text=f'Добро пожаловать в планировщик задач {message.from_user.first_name}\n'
                              f'Используйте кнопки ниже для навигации по планировщику задач...',
                         reply_markup=await base_keyboard())


@router.message(Command('help'))
async def cmd_start(message: Message):
    await message.answer(text='Используйте команду <b>/start</b> для запуска...', parse_mode=ParseMode.HTML)



