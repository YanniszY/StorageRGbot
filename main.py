import asyncio
from aiogram import Bot, Dispatcher
from config.config import BOT_TOKEN
from handlers.handlers import router
from database.db import init_db

async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    dp.include_router(router)

    init_db()  # Инициализация базы данных

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
