import os

from aiogram import Bot, Dispatcher
from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    bot_token: SecretStr = os.getenv('BOT_TOKEN')
    db_url: str = os.getenv('DATABASE_URL')

    model_config = SettingsConfigDict(
        env_file='.env', env_file_encoding='utf-8', extra='allow')


settings = Settings()

# Создание бота
bot = Bot(token=settings.bot_token.get_secret_value())

# Создание диспетчера для обработки событий
dp = Dispatcher()
