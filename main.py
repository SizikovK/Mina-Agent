import asyncio
import logging
from aiogram import Bot, Dispatcher
import os
from dotenv import load_dotenv

from handlers.basic_handlers import router as basic_router
from handlers.media_handlers import router as media_router


load_dotenv()

API_TOKEN = os.getenv("BOT")
logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

async def main():
    dp.include_router(basic_router)
    dp.include_router(media_router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())