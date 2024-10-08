from aiogram.types import KeyboardButton, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

from database.crud import get_all_categories, get_all_current_tasks
from utils.constants import ORDERS


# Создание клавиатуры для использования в /start
async def base_keyboard():
    builder = ReplyKeyboardBuilder()
    for order in ORDERS:
        builder.add(KeyboardButton(text=order))
    return builder.adjust(2).as_markup(resize_keyboard=True)


# Создание клавиатуры для использования в ответах на получение категорий
async def category_keyboard(mode: str):
    builder = InlineKeyboardBuilder()
    categories = await get_all_categories()
    for category in categories:
        if mode != 'add' or category.name != 'Все':
            builder.add(InlineKeyboardButton(text=category.name, callback_data=f'{mode}_{category.name}'))

    return builder.adjust(2).as_markup()


# Создание клавиатуры для вывода заданий в виде ин-лайн-кнопок
async def tasks_keyboard(tg_id: int, category: str):
    builder = InlineKeyboardBuilder()
    tasks = await get_all_current_tasks(tg_id, category)
    for task in tasks:
        builder.add(InlineKeyboardButton(text=f'Задача: {task.name}. Описание: {task.description}.',
                                         callback_data=f'task_{task.id}'))

    return builder.adjust(1).as_markup()
