import asyncio
import logging

from config import dp
from database.services import create_tables, add_initial_categories

from handlers.main_handlers import router as main_router
from handlers.callback_handlers import router as callback_router
from handlers.text_handlers import router as text_router
from handlers.chain_handlers import router as chain_router
from scheduler.handlers import bot
from scheduler.scheduler import scheduler

# Добавление маршрута с обработчиками к диспетчеру
dp.include_routers(main_router,
                   callback_router,
                   text_router,
                   chain_router,
                   )


async def main():
    # запуск функции с созданием всех таблиц в БД
    await create_tables()
    # Добавление стартовых данных в БД
    await add_initial_categories()
    # Удаление всех необработанных сообщений после отключения бота
    await bot.delete_webhook(drop_pending_updates=True)
    # Запуск планировщика задач по расписанию
    scheduler.start()
    # Запуск обработчика всех событий
    await dp.start_polling(bot)


if __name__ == '__main__':
    # For development only (too slow for production)
    # logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('exiting program...')
