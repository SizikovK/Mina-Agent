import asyncio
import logging
from aiogram import Bot, Dispatcher
import os
from dotenv import load_dotenv

from handlers.basic_handlers import router as basic_router
from handlers.media_handlers import router as media_router
from middlewares.spam_middleware import SpamMiddleware

from database.database import init_db

load_dotenv()
API_TOKEN = os.getenv("BOT_API_KEY")
logging.basicConfig(level=logging.INFO)

async def on_startup():
    logging.info("Проверка/создание бд")
    init_db()

async def main():
    dp = Dispatcher()

    dp.startup.register(on_startup)

    dp.include_router(basic_router)
    dp.include_router(media_router)

    dp.message.middleware(SpamMiddleware())

    bot = Bot(token=API_TOKEN)

    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())