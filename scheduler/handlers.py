from aiogram.enums import ParseMode

from config import bot
from database.crud import get_task


# Запланированное сообщение об истечении времени на выполнение задачи
async def task_reminder(chat_id: int, task_id: int):
    result = await get_task(task_id)
    if result and result.status == 'Выполняется':
        await bot.send_message(chat_id=chat_id,
                               text=f'Срок выполнения задачи <b>"{result.name}"</b> истекает через 10 минут.\n'
                                    f'Не забудьте завершить ее...', parse_mode=ParseMode.HTML)
