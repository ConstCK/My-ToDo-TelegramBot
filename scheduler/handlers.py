from aiogram.enums import ParseMode
from aiogram.types import Message

from database.crud import get_task


# Запланированное сообщение об истечении времени на выполнение задачи

async def task_reminder(message: Message, task_id: int):
    result = await get_task(task_id)
    if result.status == 'Выполняется':
        await message.answer(
            text=f'Срок выполнения задачи <b>{result.name}</b> истекает.\n'
                 f'Не забудьте завершить ее...',
            parse_mode=ParseMode.HTML
        )
