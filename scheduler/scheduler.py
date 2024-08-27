from apscheduler.schedulers.asyncio import AsyncIOScheduler

from scheduler.config import job_stores

# Создание объекта планировщика
scheduler = AsyncIOScheduler(timezone='Europe/Moscow',

                             )


